import argparse

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


DEFAULT_PROMPT = """질문:
파인튜닝이 뭐야?

핵심 사실:
- 파인튜닝은 이미 학습된 모델을 추가 데이터로 조정하는 방법이다.
- 특정 작업, 말투, 형식에 더 잘 맞게 만드는 데 쓴다.

원하는 말투/형식:
자연스러운 냥체
존댓말 금지
질문에 직접 답하기
1~2문장 기본, 최대 3문장
관련 없는 예시 내용 끌어오기 금지
핵심 사실에 없는 내용 추가 금지

위 핵심 사실만 사용해서 학습 데이터로 쓸 답변을 만들어줘."""


SYSTEM_PROMPT = """너는 학습 데이터 제작 도우미다.
사용자가 제공한 핵심 사실만 사용해서 답변 초안을 만든다.
핵심 사실에 없는 정보는 추가하지 않는다.
모든 답변은 한국어로만 작성한다.
자연스러운 냥체로 답한다.
존댓말은 사용하지 않는다.
질문에 직접 답한다.
1~2문장 기본, 최대 3문장으로 답한다."""


def build_inputs(tokenizer, prompt):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return tokenizer(text, return_tensors="pt")


def generate(model, tokenizer, prompt, max_new_tokens):
    inputs = build_inputs(tokenizer, prompt)
    inputs = {key: value.to(model.device) for key, value in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = output[0][inputs["input_ids"].shape[-1] :]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def load_base(model_name):
    has_cuda = torch.cuda.is_available()
    dtype = torch.float16 if has_cuda else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=dtype,
        device_map="auto" if has_cuda else None,
        trust_remote_code=True,
        local_files_only=True,
    )
    return model, tokenizer


def main():
    parser = argparse.ArgumentParser(description="Compare base model and LoRA adapter output.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter", default="training/output/qwen2.5-0.5b-nabi-lora")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--max-new-tokens", type=int, default=80)
    args = parser.parse_args()

    base_model, tokenizer = load_base(args.model)
    base_answer = generate(base_model, tokenizer, args.prompt, args.max_new_tokens)

    lora_model = PeftModel.from_pretrained(base_model, args.adapter)
    lora_answer = generate(lora_model, tokenizer, args.prompt, args.max_new_tokens)

    print("[base]")
    print(base_answer)
    print()
    print("[lora]")
    print(lora_answer)


if __name__ == "__main__":
    main()
