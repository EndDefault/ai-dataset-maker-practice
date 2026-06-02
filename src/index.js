import { buildSystemPrompt } from "./core/promptBuilder.js";
import { clearState, downloadTextFile, loadState, saveState } from "./core/storage.js";
import { appendChatTurn } from "./features/chat/chat.js";
import { createDatasetItem, createDatasetItemFromParts, createFailureItem, toJsonl } from "./features/dataset/dataset.js";
import { addMemory, removeMemory } from "./features/memories/memories.js";
import { createProfile, summarizeProfile, updateProfile } from "./features/profiles/profiles.js";

const fallbackProfile = createProfile();
const defaultSettings = {
  provider: "ollama",
  model: "qwen2.5:7b",
};
const modelDefaults = {
  ollama: "qwen2.5:7b",
  practice: "practice",
  openai: "gpt-4.1-mini",
};

let state = normalizeState(loadState() ?? {
  profiles: [fallbackProfile],
  activeProfileId: fallbackProfile.id,
  dataset: [],
  failures: [],
});

const elements = {
  newProfileButton: document.querySelector("#newProfileButton"),
  profileList: document.querySelector("#profileList"),
  activeProfileName: document.querySelector("#activeProfileName"),
  profileSummary: document.querySelector("#profileSummary"),
  messageList: document.querySelector("#messageList"),
  chatForm: document.querySelector("#chatForm"),
  chatInput: document.querySelector("#chatInput"),
  profileForm: document.querySelector("#profileForm"),
  providerInput: document.querySelector("#providerInput"),
  modelInput: document.querySelector("#modelInput"),
  profileNameInput: document.querySelector("#profileNameInput"),
  roleInput: document.querySelector("#roleInput"),
  toneInput: document.querySelector("#toneInput"),
  personalityInput: document.querySelector("#personalityInput"),
  rulesInput: document.querySelector("#rulesInput"),
  styleInput: document.querySelector("#styleInput"),
  promptPreview: document.querySelector("#promptPreview"),
  memoryForm: document.querySelector("#memoryForm"),
  memoryInput: document.querySelector("#memoryInput"),
  memoryList: document.querySelector("#memoryList"),
  makerForm: document.querySelector("#makerForm"),
  makerQuestionInput: document.querySelector("#makerQuestionInput"),
  makerFactsInput: document.querySelector("#makerFactsInput"),
  makerStyleInput: document.querySelector("#makerStyleInput"),
  makerDraftButton: document.querySelector("#makerDraftButton"),
  makerAnswerInput: document.querySelector("#makerAnswerInput"),
  makerSaveButton: document.querySelector("#makerSaveButton"),
  makerClearButton: document.querySelector("#makerClearButton"),
  datasetList: document.querySelector("#datasetList"),
  exportButton: document.querySelector("#exportButton"),
  clearDatasetButton: document.querySelector("#clearDatasetButton"),
  resetAppButton: document.querySelector("#resetAppButton"),
  tabs: document.querySelectorAll(".tab"),
  tabPanels: document.querySelectorAll(".tab-panel"),
};

function normalizeState(nextState) {
  return {
    ...nextState,
    settings: {
      ...defaultSettings,
      ...(nextState.settings ?? {}),
    },
    failures: nextState.failures ?? [],
  };
}

function getActiveProfile() {
  return state.profiles.find((profile) => profile.id === state.activeProfileId) ?? state.profiles[0];
}

function replaceActiveProfile(nextProfile) {
  state = {
    ...state,
    profiles: state.profiles.map((profile) => {
      return profile.id === nextProfile.id ? nextProfile : profile;
    }),
    activeProfileId: nextProfile.id,
  };
}

function readSettingsFromForm() {
  return {
    provider: elements.providerInput.value,
    model: elements.modelInput.value.trim() || modelDefaults[elements.providerInput.value],
  };
}

function persistAndRender() {
  saveState(state);
  render();
}

function render() {
  const profile = getActiveProfile();

  renderProfileList(profile);
  renderHeader(profile);
  renderProfileForm(profile);
  renderMessages(profile);
  renderMemories(profile);
  renderDataset();
}

function renderProfileList(activeProfile) {
  elements.profileList.innerHTML = "";

  state.profiles.forEach((profile) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `profile-item ${profile.id === activeProfile.id ? "active" : ""}`;
    button.innerHTML = `<strong>${profile.name}</strong><span>${summarizeProfile(profile)}</span>`;
    button.addEventListener("click", () => {
      state = { ...state, activeProfileId: profile.id };
      persistAndRender();
    });

    elements.profileList.append(button);
  });
}

function renderHeader(profile) {
  elements.activeProfileName.textContent = profile.name;
  elements.profileSummary.textContent = summarizeProfile(profile);
}

function renderProfileForm(profile) {
  elements.providerInput.value = state.settings.provider;
  elements.modelInput.value = state.settings.model;
  elements.profileNameInput.value = profile.name;
  elements.roleInput.value = profile.role;
  elements.toneInput.value = profile.tone;
  elements.personalityInput.value = profile.personality;
  elements.rulesInput.value = profile.rules;
  elements.styleInput.value = profile.style;
  elements.promptPreview.textContent = buildSystemPrompt(profile);
}

function renderMessages(profile) {
  elements.messageList.innerHTML = "";

  if (profile.messages.length === 0) {
    elements.messageList.innerHTML =
      '<div class="empty-state">아직 대화가 없습니다. 아래 입력창에서 첫 질문을 보내보세요.</div>';
    return;
  }

  profile.messages.forEach((message, index) => {
    const messageElement = document.createElement("article");
    messageElement.className = `message ${message.role} ${message.isError ? "error" : ""}`;
    messageElement.innerHTML = `
      <div class="message-meta">${message.role === "user" ? "사용자" : profile.name}</div>
      <p>${escapeHtml(message.content).replace(/\n/g, "<br>")}</p>
    `;

    if (message.role === "assistant") {
      const userMessage = profile.messages[index - 1];
      const actions = document.createElement("div");
      actions.className = "message-actions";
      actions.innerHTML = `
        <button type="button" data-action="save-good">좋은 답변 저장</button>
        <button type="button" data-action="save-edited">수정해서 저장</button>
        <button type="button" data-action="save-failure">실패 기록</button>
        <button type="button" data-action="save-tone">이 말투 기억</button>
      `;
      actions.querySelector('[data-action="save-good"]').addEventListener("click", () => {
        if (containsChineseCharacters(message.content)) {
          alert("중국어 한자가 섞인 답변은 좋은 답변 예시로 저장하지 않는 것이 좋습니다.");
          return;
        }

        state = {
          ...state,
          dataset: [...state.dataset, createDatasetItem(profile, userMessage, message)],
        };
        persistAndRender();
      });
      actions.querySelector('[data-action="save-edited"]').addEventListener("click", () => {
        const editedAnswer = prompt("좋은 답변으로 저장할 내용을 직접 고쳐 주세요.", message.content);

        if (!editedAnswer?.trim()) {
          return;
        }

        const correctedMessage = {
          ...message,
          content: editedAnswer.trim(),
          correctedFrom: message.content,
        };

        state = {
          ...state,
          dataset: [...state.dataset, createDatasetItem(profile, userMessage, correctedMessage)],
        };
        persistAndRender();
      });
      actions.querySelector('[data-action="save-failure"]').addEventListener("click", () => {
        const reason = prompt(
          "실패 이유를 적어 주세요. 예: 중국어 섞임, 질문 무시, 말투 불일치, 너무 김",
          containsChineseCharacters(message.content) ? "중국어 섞임" : "",
        );

        if (!reason?.trim()) {
          return;
        }

        state = {
          ...state,
          failures: [...state.failures, createFailureItem(profile, userMessage, message, reason.trim())],
        };
        persistAndRender();
      });
      actions.querySelector('[data-action="save-tone"]').addEventListener("click", () => {
        replaceActiveProfile(addMemory(profile, `좋았던 답변 스타일: ${message.content.slice(0, 80)}`));
        persistAndRender();
      });
      messageElement.append(actions);
    }

    elements.messageList.append(messageElement);
  });

  elements.messageList.scrollTop = elements.messageList.scrollHeight;
}

function renderMemories(profile) {
  elements.memoryList.innerHTML = "";

  if (profile.memories.length === 0) {
    elements.memoryList.innerHTML = '<div class="empty-state">저장된 기억이 없습니다.</div>';
    return;
  }

  profile.memories.forEach((memory) => {
    const item = document.createElement("div");
    item.className = "memory-item";
    item.innerHTML = `
      <span>${new Date(memory.createdAt).toLocaleString("ko-KR")}</span>
      <strong>${escapeHtml(memory.content)}</strong>
      <div class="item-actions">
        <button class="danger-button" type="button">삭제</button>
      </div>
    `;
    item.querySelector("button").addEventListener("click", () => {
      replaceActiveProfile(removeMemory(profile, memory.id));
      persistAndRender();
    });

    elements.memoryList.append(item);
  });
}

function renderDataset() {
  elements.datasetList.innerHTML = "";

  const goodSection = document.createElement("section");
  goodSection.className = "data-section";
  goodSection.innerHTML = '<div class="panel-title">좋은 예시</div>';

  if (state.dataset.length === 0) {
    goodSection.innerHTML += '<div class="empty-state">저장된 좋은 답변이 없습니다.</div>';
  } else {
    state.dataset
      .slice()
      .reverse()
      .forEach((item) => {
        const userMessage = item.messages.find((message) => message.role === "user");
        const assistantMessage = item.messages.find((message) => message.role === "assistant");
        const itemElement = document.createElement("div");
        itemElement.className = "dataset-item";
        itemElement.innerHTML = `
          <span>${item.profileName} · ${new Date(item.createdAt).toLocaleString("ko-KR")}</span>
          <strong>${escapeHtml(userMessage.content)}</strong>
          <span>${escapeHtml(assistantMessage.content.slice(0, 120))}</span>
        `;
        goodSection.append(itemElement);
      });
  }

  const failureSection = document.createElement("section");
  failureSection.className = "data-section";
  failureSection.innerHTML = '<div class="panel-title">실패 기록</div>';

  if (state.failures.length === 0) {
    failureSection.innerHTML += '<div class="empty-state">저장된 실패 기록이 없습니다.</div>';
  } else {
    state.failures
      .slice()
      .reverse()
      .forEach((item) => {
        const itemElement = document.createElement("div");
        itemElement.className = "dataset-item failure-item";
        itemElement.innerHTML = `
          <span>${item.profileName} · ${new Date(item.createdAt).toLocaleString("ko-KR")}</span>
          <strong>${escapeHtml(item.reason)}</strong>
          <span>${escapeHtml(item.userInput.slice(0, 120))}</span>
        `;
        failureSection.append(itemElement);
      });
  }

  elements.datasetList.append(goodSection, failureSection);
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };

    return entities[character];
  });
}

function containsChineseCharacters(text) {
  return /[\u3400-\u4DBF\u4E00-\u9FFF]/u.test(text);
}

function buildMakerSystemPrompt(profile) {
  return [
    "너는 학습 데이터 제작 도우미다.",
    "사용자가 제공한 핵심 사실만 사용해서 답변 초안을 만든다.",
    "핵심 사실에 없는 정보는 추가하지 않는다.",
    "모르면 추측하지 말고, 제공된 사실만으로 답할 수 없다고 말한다.",
    "모든 답변은 한국어로만 작성한다.",
    `원하는 기본 말투: ${profile.tone}`,
    `AI 역할 참고: ${profile.role}`,
    `답변 스타일 참고: ${profile.style}`,
  ].join("\n");
}

function buildMakerUserInput() {
  return [
    `질문:\n${elements.makerQuestionInput.value.trim()}`,
    "",
    `핵심 사실:\n${elements.makerFactsInput.value.trim()}`,
    "",
    `원하는 말투/형식:\n${elements.makerStyleInput.value.trim()}`,
    "",
    "위 핵심 사실만 사용해서 학습 데이터로 쓸 답변을 만들어줘.",
  ].join("\n");
}

async function requestMakerDraft(profile, settings) {
  const systemPrompt = buildMakerSystemPrompt(profile);
  const userInput = buildMakerUserInput();
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      provider: settings.provider,
      model: settings.model,
      systemPrompt,
      messages: [{ role: "user", content: userInput }],
    }),
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error ?? "초안을 만들지 못했습니다.");
  }

  return data.answer;
}

function clearMakerForm() {
  elements.makerQuestionInput.value = "";
  elements.makerFactsInput.value = "";
  elements.makerStyleInput.value = "";
  elements.makerAnswerInput.value = "";
}

elements.newProfileButton.addEventListener("click", () => {
  const nextProfile = createProfile({
    name: `새 AI ${state.profiles.length + 1}`,
    messages: [],
  });

  state = {
    ...state,
    profiles: [...state.profiles, nextProfile],
    activeProfileId: nextProfile.id,
  };
  persistAndRender();
});

elements.profileForm.addEventListener("submit", (event) => {
  event.preventDefault();

  state = {
    ...state,
    settings: readSettingsFromForm(),
  };

  replaceActiveProfile(
    updateProfile(getActiveProfile(), {
      name: elements.profileNameInput.value.trim(),
      role: elements.roleInput.value.trim(),
      tone: elements.toneInput.value,
      personality: elements.personalityInput.value.trim(),
      rules: elements.rulesInput.value.trim(),
      style: elements.styleInput.value.trim(),
    }),
  );
  persistAndRender();
});

elements.providerInput.addEventListener("change", () => {
  elements.modelInput.value = modelDefaults[elements.providerInput.value];
  state = {
    ...state,
    settings: readSettingsFromForm(),
  };
  saveState(state);
});

elements.chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const input = elements.chatInput.value.trim();

  if (!input) {
    return;
  }

  elements.chatInput.value = "";
  elements.chatInput.disabled = true;
  elements.chatForm.querySelector("button").disabled = true;
  state = {
    ...state,
    settings: readSettingsFromForm(),
  };
  saveState(state);

  const nextTurn = await appendChatTurn(getActiveProfile(), input, state.settings, state.dataset);

  replaceActiveProfile(nextTurn.profile);
  elements.chatInput.disabled = false;
  elements.chatForm.querySelector("button").disabled = false;
  elements.chatInput.focus();
  persistAndRender();
});

elements.memoryForm.addEventListener("submit", (event) => {
  event.preventDefault();

  replaceActiveProfile(addMemory(getActiveProfile(), elements.memoryInput.value));
  elements.memoryInput.value = "";
  persistAndRender();
});

elements.makerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!elements.makerQuestionInput.value.trim() || !elements.makerFactsInput.value.trim()) {
    alert("질문과 핵심 사실은 꼭 입력해야 합니다.");
    return;
  }

  state = {
    ...state,
    settings: readSettingsFromForm(),
  };
  saveState(state);

  elements.makerDraftButton.disabled = true;
  elements.makerDraftButton.textContent = "초안 만드는 중...";

  try {
    elements.makerAnswerInput.value = await requestMakerDraft(getActiveProfile(), state.settings);
  } catch (error) {
    elements.makerAnswerInput.value = `초안 생성 오류: ${error.message}`;
  } finally {
    elements.makerDraftButton.disabled = false;
    elements.makerDraftButton.textContent = "초안 만들기";
  }
});

elements.makerSaveButton.addEventListener("click", () => {
  const question = elements.makerQuestionInput.value.trim();
  const facts = elements.makerFactsInput.value.trim();
  const answer = elements.makerAnswerInput.value.trim();

  if (!question || !facts || !answer) {
    alert("질문, 핵심 사실, 최종 답변이 모두 있어야 저장할 수 있습니다.");
    return;
  }

  const profile = getActiveProfile();
  const systemPrompt = buildMakerSystemPrompt(profile);
  const userInput = buildMakerUserInput();

  state = {
    ...state,
    dataset: [...state.dataset, createDatasetItemFromParts(profile, systemPrompt, userInput, answer)],
  };
  persistAndRender();
  alert("학습 데이터 후보로 저장했습니다.");
});

elements.makerClearButton.addEventListener("click", () => {
  clearMakerForm();
});

elements.exportButton.addEventListener("click", () => {
  if (state.dataset.length === 0) {
    return;
  }

  downloadTextFile("ai-maker-dataset.jsonl", toJsonl(state.dataset));
});

elements.clearDatasetButton.addEventListener("click", () => {
  if (confirm("좋은 예시와 실패 기록을 모두 비울까요?")) {
    state = { ...state, dataset: [], failures: [] };
    persistAndRender();
  }
});

elements.resetAppButton.addEventListener("click", () => {
  if (confirm("앱에 저장된 프로필, 기억, 대화, 데이터셋을 모두 초기화할까요?")) {
    clearState();
    window.location.reload();
  }
});

elements.tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    elements.tabs.forEach((item) => item.classList.remove("active"));
    elements.tabPanels.forEach((panel) => panel.classList.remove("active"));

    tab.classList.add("active");
    document.querySelector(`#${tab.dataset.tab}Tab`).classList.add("active");
  });
});

render();
