import { deleteState, fetchState, putState } from "../api/stateApi.js";

export async function loadState() {
  return fetchState();
}

export async function saveState(state) {
  await putState(state);
}

export async function clearState() {
  await deleteState();
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
