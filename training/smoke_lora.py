import argparse
import json
from pathlib import Path

from peft import LoraConfig, TaskType, get_peft_model
from transformers import GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments

import torch


class ByteDataset(torch.utils.data.Dataset):
    def __init__(self, path, max_length):
        self.examples = []
        self.max_length = max_length

        with Path(path).open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                messages = item["messages"]
                text = (
                    f"<system>{messages[0]['content']}</system>"
                    f"<user>{messages[1]['content']}</user>"
                    f"<assistant>{messages[2]['content']}</assistant>"
                )
                ids = [byte + 1 for byte in text.encode("utf-8")[: max_length - 1]]
                ids.append(0)
                self.examples.append(ids)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        ids = self.examples[index]
        return {
            "input_ids": ids,
            "attention_mask": [1] * len(ids),
            "labels": ids.copy(),
        }


class ByteCollator:
    def __call__(self, features):
        max_length = max(len(feature["input_ids"]) for feature in features)
        batch = {"input_ids": [], "attention_mask": [], "labels": []}

        for feature in features:
            pad_length = max_length - len(feature["input_ids"])
            batch["input_ids"].append(feature["input_ids"] + [0] * pad_length)
            batch["attention_mask"].append(feature["attention_mask"] + [0] * pad_length)
            batch["labels"].append(feature["labels"] + [-100] * pad_length)

        return {key: torch.tensor(value, dtype=torch.long) for key, value in batch.items()}


def main():
    parser = argparse.ArgumentParser(description="Run a local tiny LoRA smoke test without model downloads.")
    parser.add_argument("--data", default="training/data/ai-maker-dataset.jsonl")
    parser.add_argument("--output", default="training/output/smoke-lora")
    parser.add_argument("--max-steps", type=int, default=3)
    parser.add_argument("--max-length", type=int, default=256)
    args = parser.parse_args()

    config = GPT2Config(
        vocab_size=257,
        n_positions=args.max_length,
        n_embd=64,
        n_layer=2,
        n_head=2,
        bos_token_id=0,
        eos_token_id=0,
        pad_token_id=0,
    )
    model = GPT2LMHeadModel(config)
    model = get_peft_model(
        model,
        LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=4,
            lora_alpha=8,
            lora_dropout=0.05,
            target_modules=["c_attn"],
        ),
    )
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=args.output,
        max_steps=args.max_steps,
        per_device_train_batch_size=1,
        logging_steps=1,
        save_steps=args.max_steps,
        save_total_limit=1,
        report_to=[],
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ByteDataset(args.data, args.max_length),
        data_collator=ByteCollator(),
    )
    trainer.train()
    trainer.save_model(args.output)
    print(f"Saved smoke-test LoRA adapter to {args.output}")


if __name__ == "__main__":
    main()
