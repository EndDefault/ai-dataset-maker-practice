const STORAGE_KEY = "ai-maker-studio-state-v1";

export function loadState() {
  const rawState = localStorage.getItem(STORAGE_KEY);

  if (!rawState) {
    return null;
  }

  try {
    return JSON.parse(rawState);
  } catch {
    return null;
  }
}

export function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export function clearState() {
  localStorage.removeItem(STORAGE_KEY);
}

export function downloadTextFile(filename, text) {
  const blob = new Blob([text], { type: "application/jsonl;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  link.click();

  URL.revokeObjectURL(url);
}
