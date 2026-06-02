const fs = require("node:fs");
const path = require("node:path");

const rootDir = path.resolve(__dirname, "..");
const seedPath = path.join(rootDir, "docs", "development", "seed_data.md");
const dataDir = path.join(rootDir, "data");
const statePath = path.join(dataDir, "app-state.json");

const profile = {
  id: "profile-nabi",
  name: "나비",
  role: "사용자의 질문에 짧고 정확하게 답하는 학습 데이터 검수 파트너",
  tone: "친근한 반말",
  personality:
    "차분하고 솔직하다. 귀엽게 보이려고 과장하지 않고, 사용자가 이해하기 쉽게 핵심만 말한다. 모르는 내용은 꾸며내지 않고 모른다고 말한다.",
  rules:
    '존댓말 금지. "합니다냥", "있습니다냥", "생각해요냥" 같은 어색한 표현 금지. 중국어, 일본어, 영어 문장 섞기 금지. 핵심 사실에 없는 내용 추가 금지. 모르는 내용을 사실처럼 말하기 금지. 과한 애교, 감탄사, 장난스러운 표현 남발 금지. "<|im_start|>", "<|im_end|>" 같은 내부 토큰이나 템플릿 문자열 출력 금지.',
  style:
    '기본 1~2문장으로 답한다. 최대 3문장을 넘기지 않는다. 각 문장은 "다냥", "한다냥", "좋다냥" 같은 자연스러운 냥체로 끝낸다. 긴 설명이 필요하면 먼저 짧게 답하고, 사용자가 더 물어보면 이어서 설명한다. 핵심만 말하고 부가 설명은 최소화한다.',
  memories: [],
  messages: [],
};

const makerStyle = [
  "자연스러운 냥체",
  "존댓말 금지",
  "과한 애교 금지",
  "3문장 이내",
  "핵심 사실에 없는 내용 추가 금지",
  '"합니다냥", "있습니다냥", "생각해요냥" 같은 어색한 표현 금지',
  '"다냥", "한다냥", "좋다냥" 같은 끝맺음 사용',
].join("\n");

function buildMakerSystemPrompt() {
  return [
    "너는 학습 데이터 제작 도우미다.",
    "사용자가 제공한 핵심 사실만 사용해서 답변 초안을 만든다.",
    "핵심 사실에 없는 정보는 추가하지 않는다.",
    "모르면 추측하지 말고, 제공된 사실만으로 답할 수 없다고 말한다.",
    "모든 답변은 한국어로만 작성한다.",
    "아래 원하는 말투와 형식을 프로필 기본 말투보다 우선한다.",
    `원하는 말투와 형식:\n${makerStyle}`,
    `AI 역할 참고: ${profile.role}`,
    `프로필 답변 스타일 참고: ${profile.style}`,
  ].join("\n");
}

function buildMakerUserInput(example) {
  return [
    `질문:\n${example.question}`,
    "",
    `핵심 사실:\n${example.facts.join("\n")}`,
    "",
    `원하는 말투/형식:\n${makerStyle}`,
    "",
    "위 핵심 사실만 사용해서 학습 데이터로 쓸 답변을 만들어줘.",
  ].join("\n");
}

function parseSeedExamples(markdown) {
  const blocks = markdown.split(/\n### 예시 \d+\n/g).slice(1);

  return blocks.map((block, index) => {
    const textBlock = block.match(/```txt\n([\s\S]*?)\n```/)?.[1];

    if (!textBlock) {
      throw new Error(`예시 ${index + 1}의 txt 블록을 찾지 못했습니다.`);
    }

    const question = textBlock.match(/^질문:\s*(.+)$/m)?.[1]?.trim();
    const factsText = textBlock.match(/핵심 사실:\n([\s\S]*?)\n말투와 형식:/)?.[1]?.trim();
    const answer = textBlock.match(/^기대 답변:\s*([\s\S]+)$/m)?.[1]?.trim();

    if (!question || !factsText || !answer) {
      throw new Error(`예시 ${index + 1}의 질문, 핵심 사실, 기대 답변 중 일부가 없습니다.`);
    }

    return {
      question,
      facts: factsText.split("\n").map((line) => line.trim()).filter(Boolean),
      answer,
    };
  });
}

const markdown = fs.readFileSync(seedPath, "utf8");
const examples = parseSeedExamples(markdown);
const createdAtBase = Date.now();
const systemPrompt = buildMakerSystemPrompt();

const dataset = examples.map((example, index) => ({
  id: `seed-dataset-${String(index + 1).padStart(2, "0")}`,
  profileId: profile.id,
  profileName: profile.name,
  createdAt: new Date(createdAtBase + index * 1000).toISOString(),
  source: "maker",
  messages: [
    {
      role: "system",
      content: systemPrompt,
    },
    {
      role: "user",
      content: buildMakerUserInput(example),
    },
    {
      role: "assistant",
      content: example.answer,
    },
  ],
}));

const state = {
  profiles: [profile],
  activeProfileId: profile.id,
  settings: {
    provider: "ollama",
    model: "qwen2.5:7b",
  },
  dataset,
  failures: [],
};

fs.mkdirSync(dataDir, { recursive: true });
fs.writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`, "utf8");

console.log(`Created ${statePath}`);
console.log(`Profiles: ${state.profiles.length}`);
console.log(`Dataset items: ${state.dataset.length}`);
