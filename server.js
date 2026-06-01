const http = require("node:http");
const fs = require("node:fs/promises");
const path = require("node:path");

const PORT = Number(process.env.PORT ?? 5173);
const DEFAULT_PROVIDER = process.env.AI_PROVIDER ?? "ollama";
const DEFAULT_OLLAMA_MODEL = process.env.OLLAMA_MODEL ?? "qwen2.5:7b";
const DEFAULT_OPENAI_MODEL = process.env.OPENAI_MODEL ?? "gpt-4.1-mini";
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL ?? "http://localhost:11434";
const PUBLIC_DIR = __dirname;

const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
};

const server = http.createServer(async (request, response) => {
  try {
    if (request.method === "POST" && request.url === "/api/chat") {
      await handleChat(request, response);
      return;
    }

    if (request.method !== "GET") {
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }

    await serveStaticFile(request, response);
  } catch (error) {
    sendJson(response, 500, { error: error.message });
  }
});

server.listen(PORT, () => {
  console.log(`AI Maker Studio running at http://localhost:${PORT}`);
  console.log(`Default provider: ${DEFAULT_PROVIDER}`);
  console.log(`Ollama URL: ${OLLAMA_BASE_URL}`);
});

async function handleChat(request, response) {
  const body = await readJsonBody(request);
  const messages = Array.isArray(body.messages) ? body.messages : [];
  const provider = body.provider ?? DEFAULT_PROVIDER;

  if (!body.systemPrompt || messages.length === 0) {
    sendJson(response, 400, { error: "systemPrompt and messages are required." });
    return;
  }

  if (provider === "practice") {
    sendJson(response, 200, answerWithPracticeEngine(body.systemPrompt, messages));
    return;
  }

  if (provider === "ollama") {
    const model = body.model || DEFAULT_OLLAMA_MODEL;
    sendJson(response, 200, await answerWithOllama(body.systemPrompt, messages, model));
    return;
  }

  if (provider === "openai") {
    const model = body.model || DEFAULT_OPENAI_MODEL;
    sendJson(response, 200, await answerWithOpenAI(body.systemPrompt, messages, model));
    return;
  }

  sendJson(response, 400, { error: `Unknown provider: ${provider}` });
}

async function answerWithOllama(systemPrompt, messages, model) {
  const ollamaResponse = await fetch(`${OLLAMA_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      stream: false,
      options: {
        temperature: 0.2,
        top_p: 0.8,
        repeat_penalty: 1.15,
        num_predict: 360,
      },
      messages: [{ role: "system", content: systemPrompt }, ...messages],
    }),
  });

  const data = await ollamaResponse.json();

  if (!ollamaResponse.ok) {
    throw new Error(data.error ?? "Ollama request failed.");
  }

  let answer = cleanModelAnswer(data.message?.content ?? "Ollama response did not include message content.");

  if (containsChineseCharacters(answer)) {
    answer = await rewriteKoreanOnly(answer, model);
  }

  return {
    answer,
    provider: "ollama",
    model,
  };
}

async function rewriteKoreanOnly(answer, model) {
  const rewriteResponse = await fetch(`${OLLAMA_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      stream: false,
      options: {
        temperature: 0.1,
        top_p: 0.7,
        repeat_penalty: 1.15,
        num_predict: 260,
      },
      messages: [
        {
          role: "system",
          content:
            "너는 문장 교정기다. 입력된 답변을 한국어로만 다시 쓴다. 중국어, 일본어, 영어를 섞지 않는다. 의미는 유지하고 3문장 이내로 짧게 쓴다.",
        },
        {
          role: "user",
          content: answer,
        },
      ],
    }),
  });

  const data = await rewriteResponse.json();

  if (!rewriteResponse.ok) {
    return answer;
  }

  return cleanModelAnswer(data.message?.content ?? answer);
}

async function answerWithOpenAI(systemPrompt, messages, model) {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is required when provider is openai.");
  }

  const openAIResponse = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      instructions: systemPrompt,
      input: messages.map((message) => ({
        role: message.role,
        content: message.content,
      })),
    }),
  });

  const data = await openAIResponse.json();

  if (!openAIResponse.ok) {
    throw new Error(data.error?.message ?? "OpenAI request failed.");
  }

  return {
    answer: cleanModelAnswer(extractOpenAIOutputText(data)),
    provider: "openai",
    model,
  };
}

function cleanModelAnswer(answer) {
  return answer
    .replace(/<think>[\s\S]*?<\/think>/gi, "")
    .replace(/^\s*(답변|assistant|AI)\s*[:：]\s*/i, "")
    .trim();
}

function containsChineseCharacters(text) {
  return /[\u3400-\u4DBF\u4E00-\u9FFF]/u.test(text);
}

function answerWithPracticeEngine(systemPrompt, messages) {
  const lastUserMessage = messages.filter((message) => message.role === "user").at(-1);

  return {
    answer: [
      "연습용 가짜 답변입니다.",
      "",
      `받은 질문: ${lastUserMessage?.content ?? ""}`,
      "",
      "이 모드는 비용 없이 화면과 데이터 저장 흐름을 테스트할 때 사용합니다.",
      "실제 답변을 받으려면 AI 제공자를 Ollama 또는 OpenAI로 바꿔 주세요.",
      "",
      "현재 시스템 프롬프트 일부:",
      systemPrompt.slice(0, 240),
    ].join("\n"),
    provider: "practice",
    model: "practice",
  };
}

async function serveStaticFile(request, response) {
  const url = new URL(request.url, `http://localhost:${PORT}`);
  const requestedPath = url.pathname === "/" ? "/index.html" : decodeURIComponent(url.pathname);
  const filePath = path.normalize(path.join(PUBLIC_DIR, requestedPath));

  if (!filePath.startsWith(PUBLIC_DIR)) {
    sendJson(response, 403, { error: "Forbidden" });
    return;
  }

  try {
    const file = await fs.readFile(filePath);
    const extension = path.extname(filePath);

    response.writeHead(200, {
      "Content-Type": contentTypes[extension] ?? "application/octet-stream",
    });
    response.end(file);
  } catch {
    sendJson(response, 404, { error: "Not found" });
  }
}

function readJsonBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";

    request.on("data", (chunk) => {
      body += chunk;

      if (body.length > 1_000_000) {
        request.destroy();
        reject(new Error("Request body is too large."));
      }
    });

    request.on("end", () => {
      try {
        resolve(JSON.parse(body || "{}"));
      } catch {
        reject(new Error("Invalid JSON body."));
      }
    });
  });
}

function extractOpenAIOutputText(data) {
  if (typeof data.output_text === "string" && data.output_text.trim()) {
    return data.output_text;
  }

  const textParts = [];

  for (const item of data.output ?? []) {
    for (const content of item.content ?? []) {
      if (content.type === "output_text" && content.text) {
        textParts.push(content.text);
      }
    }
  }

  return textParts.join("\n").trim() || "OpenAI response did not include output text.";
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
  });
  response.end(JSON.stringify(payload));
}
