export function createProfile(overrides = {}) {
  return {
    id: crypto.randomUUID(),
    name: "첫 번째 AI",
    role: "AI 학습 파트너",
    tone: "차분한 존댓말",
    personality: "친절하고, 사용자가 이해할 수 있게 단계별로 설명한다.",
    rules: "모르면 모른다고 말한다. 너무 길게 답하지 않는다.",
    style: "핵심을 먼저 말하고, 필요하면 짧은 예시를 붙인다.",
    memories: [],
    messages: [],
    ...overrides,
  };
}

export function updateProfile(profile, fields) {
  return {
    ...profile,
    ...fields,
  };
}

export function summarizeProfile(profile) {
  return `${profile.role} · ${profile.tone}`;
}
