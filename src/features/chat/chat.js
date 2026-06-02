import { buildSystemPrompt } from "../../core/promptBuilder.js";
import { findRelatedMemories } from "../memories/memories.js";

const MAX_GOOD_EXAMPLES = 10;
const MIN_RICH_EXAMPLE_LENGTH = 30;

export function createMessage(role, content, extra = {}) {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: new Date().toISOString(),
    ...extra,
  };
}

export async function answerWithSelectedProvider(profile, userInput, settings, dataset = []) {
  const relatedMemories = findRelatedMemories(profile, userInput);
  const goodExamples = findGoodExamples(profile, dataset);
  const systemPrompt = buildSystemPrompt(profile, relatedMemories, goodExamples);
  const recentMessages = profile.messages
    .filter((message) => !message.isError)
    .slice(-6)
    .map((message) => ({
      role: message.role,
      content: message.content,
    }));

  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      provider: settings.provider,
      model: settings.model,
      systemPrompt,
      messages: [...recentMessages, { role: "user", content: userInput }],
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error ?? "AI response failed.");
  }

  return {
    message: createMessage("assistant", data.answer, {
      systemPrompt,
      relatedMemoryIds: relatedMemories.map((memory) => memory.id),
      goodExampleIds: goodExamples.map((example) => example.id),
      provider: data.provider,
      model: data.model,
    }),
    relatedMemories,
  };
}

export async function appendChatTurn(profile, userInput, settings, dataset = []) {
  const userMessage = createMessage("user", userInput);

  try {
    const assistantResult = await answerWithSelectedProvider(profile, userInput, settings, dataset);

    return {
      profile: {
        ...profile,
        messages: [...profile.messages, userMessage, assistantResult.message],
      },
      userMessage,
      assistantMessage: assistantResult.message,
    };
  } catch (error) {
    const assistantMessage = createMessage(
      "assistant",
      [
        `AI 연결 오류: ${error.message}`,
        "",
        "Ollama를 쓰는 중이라면 `ollama serve`가 실행 중인지, 선택한 모델이 설치되어 있는지 확인해 주세요.",
      ].join("\n"),
      { isError: true },
    );

    return {
      profile: {
        ...profile,
        messages: [...profile.messages, userMessage, assistantMessage],
      },
      userMessage,
      assistantMessage,
    };
  }
}

function findGoodExamples(profile, dataset) {
  return dataset
    .filter((item) => item.profileId === profile.id)
    .map(toGoodExampleCandidate)
    .filter(Boolean)
    .sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }

      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    })
    .slice(0, MAX_GOOD_EXAMPLES)
    .map((item) => ({
      id: item.id,
      user: item.user,
      assistant: item.assistant,
    }));
}

function toGoodExampleCandidate(item) {
  const user = item.messages.find((message) => message.role === "user")?.content ?? "";
  const assistant = item.messages.find((message) => message.role === "assistant")?.content ?? "";

  if (!assistant || containsChineseCharacters(assistant)) {
    return null;
  }

  return {
    id: item.id,
    user,
    assistant,
    createdAt: item.createdAt,
    score: scoreGoodExample(item, user, assistant),
  };
}

function scoreGoodExample(item, user, assistant) {
  let score = 0;

  if (item.source === "maker") {
    score += 5;
  }

  if (assistant.length >= MIN_RICH_EXAMPLE_LENGTH) {
    score += 2;
  }

  if (user.length >= MIN_RICH_EXAMPLE_LENGTH) {
    score += 1;
  }

  if (assistant.length < 15) {
    score -= 2;
  }

  return score;
}

function containsChineseCharacters(text) {
  return /[\u3400-\u4DBF\u4E00-\u9FFF]/u.test(text);
}
