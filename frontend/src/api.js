const API_URL = import.meta.env.VITE_API_URL;

export async function getRecommendations(userId, n = 10) {
  const res = await fetch(`${API_URL}/recommendations/${userId}?n=${n}`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}