export function buildSystemPrompt(profile, relatedMemories = [], goodExamples = []) {
  const memoryText =
    relatedMemories.length > 0
      ? relatedMemories.map((memory) => `- ${memory.content}`).join("\n")
      : "- 아직 관련 기억이 없다.";

  const exampleText =
    goodExamples.length > 0
      ? goodExamples
          .map((example, index) => {
            return [
              `예시 ${index + 1}`,
              `사용자: ${example.user}`,
              `좋은 답변: ${example.assistant}`,
            ].join("\n");
          })
          .join("\n\n")
      : "- 아직 참고할 좋은 답변 예시가 없다.";

  return [
    "아래 규칙은 반드시 지킨다.",
    "- 모든 답변은 한국어로만 작성한다.",
    "- 중국어, 일본어, 영어 문장을 섞지 않는다. 사용자가 번역을 요청한 원문 인용이 필요할 때만 예외로 한다.",
    "- 사용자의 마지막 질문에 직접 답한다. 다른 주제로 넘어가지 않는다.",
    "- 모르면 추측하지 말고 모른다고 말한다.",
    "- 답변은 짧고 일관되게 한다. 기본은 3문장 이내다.",
    "- 말투와 역할이 충돌하면 말투보다 사용자의 질문 해결을 우선한다.",
    "",
    `너의 이름은 ${profile.name}이다.`,
    `역할: ${profile.role}`,
    `말투: ${profile.tone}`,
    `성격: ${profile.personality}`,
    `금지사항: ${profile.rules}`,
    `답변 스타일: ${profile.style}`,
    "",
    "관련 기억:",
    memoryText,
    "",
    "좋은 답변 예시:",
    exampleText,
    "",
    "답변 전 점검:",
    "1. 한국어만 사용했는가?",
    "2. 사용자의 마지막 질문에 답했는가?",
    "3. 3문장 이내로 충분히 짧은가?",
  ].join("\n");
}
