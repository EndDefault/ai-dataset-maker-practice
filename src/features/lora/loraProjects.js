const defaultChecklist = [
  "출력 형식을 지켰는가",
  "금지사항을 어기지 않았는가",
  "불필요한 설명을 추가하지 않았는가",
];

export function createLoraProject(overrides = {}) {
  const now = new Date().toISOString();

  return {
    id: crypto.randomUUID(),
    name: "새 LoRA 프로젝트",
    purpose: "정해진 템플릿에 맞는 학습 데이터셋을 만든다.",
    baseModel: "Qwen/Qwen2.5-0.5B-Instruct",
    targetCount: 50,
    status: "draft",
    createdAt: now,
    updatedAt: now,
    ...overrides,
  };
}

export function createLoraTemplate(projectId, overrides = {}) {
  const now = new Date().toISOString();

  return {
    id: crypto.randomUUID(),
    projectId,
    name: "기본 템플릿",
    systemPrompt: "너는 LoRA 학습 데이터 제작 도우미다.",
    userFormat: "질문:\n{{question}}\n\n핵심 사실:\n{{facts}}\n\n위 핵심 사실만 사용해서 답변해줘.",
    outputFormat: "1~2문장으로 직접 답한다.",
    forbidden: "핵심 사실에 없는 내용 추가 금지",
    checklist: defaultChecklist.join("\n"),
    exampleSeed: "",
    createdAt: now,
    updatedAt: now,
    ...overrides,
  };
}

export function updateLoraProject(project, updates) {
  return {
    ...project,
    ...updates,
    targetCount: Number(updates.targetCount || project.targetCount || 1),
    updatedAt: new Date().toISOString(),
  };
}

export function updateLoraTemplate(template, updates) {
  return {
    ...template,
    ...updates,
    updatedAt: new Date().toISOString(),
  };
}

export function getProjectDataset(dataset, projectId) {
  return dataset.filter((item) => item.loraProjectId === projectId);
}
