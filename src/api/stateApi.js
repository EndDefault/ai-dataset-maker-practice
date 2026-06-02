export async function fetchState() {
  const response = await fetch("/api/state");

  if (!response.ok) {
    return null;
  }

  return response.json();
}

export async function putState(state) {
  await fetch("/api/state", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(state),
  });
}

export async function deleteState() {
  await fetch("/api/state", {
    method: "DELETE",
  });
}
