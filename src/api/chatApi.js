export async function postChat({ provider, model, systemPrompt, messages }) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      provider,
      model,
      systemPrompt,
      messages,
    }),
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error ?? "AI response failed.");
  }

  return data;
}
