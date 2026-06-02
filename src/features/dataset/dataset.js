export function createDatasetItem(profile, userMessage, assistantMessage) {
  return {
    id: crypto.randomUUID(),
    profileId: profile.id,
    profileName: profile.name,
    createdAt: new Date().toISOString(),
    messages: [
      {
        role: "system",
        content: assistantMessage.systemPrompt,
      },
      {
        role: "user",
        content: userMessage.content,
      },
      {
        role: "assistant",
        content: assistantMessage.content,
      },
    ],
  };
}

export function createDatasetItemFromParts(profile, systemPrompt, userInput, assistantOutput) {
  return {
    id: crypto.randomUUID(),
    profileId: profile.id,
    profileName: profile.name,
    createdAt: new Date().toISOString(),
    source: "maker",
    messages: [
      {
        role: "system",
        content: systemPrompt,
      },
      {
        role: "user",
        content: userInput,
      },
      {
        role: "assistant",
        content: assistantOutput,
      },
    ],
  };
}

export function createDatasetItemFromTemplate(project, template, userInput, assistantOutput) {
  return {
    id: crypto.randomUUID(),
    profileId: null,
    profileName: project.name,
    loraProjectId: project.id,
    loraTemplateId: template.id,
    loraProjectName: project.name,
    reviewStatus: "draft",
    source: "lora-template",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    evaluation: null,
    messages: [
      {
        role: "system",
        content: template.systemPrompt,
      },
      {
        role: "user",
        content: userInput,
      },
      {
        role: "assistant",
        content: assistantOutput,
      },
    ],
  };
}

export function createFailureItem(profile, userMessage, assistantMessage, reason) {
  return {
    id: crypto.randomUUID(),
    profileId: profile.id,
    profileName: profile.name,
    reason,
    userInput: userMessage.content,
    badOutput: assistantMessage.content,
    provider: assistantMessage.provider,
    model: assistantMessage.model,
    createdAt: new Date().toISOString(),
  };
}

export function toJsonl(dataset) {
  return dataset.map((item) => JSON.stringify({ messages: item.messages })).join("\n");
}
