/** API client for the FastAPI backend. */

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

export interface MessagePayload {
  message: string;
  conversation_id?: string;
  external_message_id?: string;
  channel?: string;
}

export interface MessageResult {
  conversation_id: string;
  message_id: string;
  response?: string;
  lead_id?: string | null;
}

export async function sendMessage(payload: MessagePayload): Promise<MessageResult> {
  const res = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.error?.message || `Request failed (${res.status})`);
  }
  return res.json();
}
