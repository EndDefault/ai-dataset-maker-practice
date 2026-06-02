export async function loadState() {
  const response = await fetch("/api/state");

  if (!response.ok) {
    return null;
  }

  return response.json();
}

export async function saveState(state) {
  await fetch("/api/state", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(state),
  });
}

export async function clearState() {
  await fetch("/api/state", {
    method: "DELETE",
  });
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
