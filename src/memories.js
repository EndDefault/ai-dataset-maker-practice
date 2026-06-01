export function addMemory(profile, content) {
  const trimmedContent = content.trim();

  if (!trimmedContent) {
    return profile;
  }

  return {
    ...profile,
    memories: [
      ...profile.memories,
      {
        id: crypto.randomUUID(),
        content: trimmedContent,
        createdAt: new Date().toISOString(),
      },
    ],
  };
}

export function removeMemory(profile, memoryId) {
  return {
    ...profile,
    memories: profile.memories.filter((memory) => memory.id !== memoryId),
  };
}

export function findRelatedMemories(profile, userInput) {
  const tokens = userInput
    .toLowerCase()
    .split(/\s+/)
    .map((token) => token.replace(/[^\p{L}\p{N}]/gu, ""))
    .filter(Boolean);

  if (tokens.length === 0) {
    return profile.memories.slice(0, 3);
  }

  return profile.memories
    .map((memory) => {
      const content = memory.content.toLowerCase();
      const score = tokens.reduce((total, token) => {
        return total + (content.includes(token) ? 1 : 0);
      }, 0);

      return { ...memory, score };
    })
    .filter((memory) => memory.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
}
