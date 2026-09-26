/** API client for the FastAPI backend. */

import type { Lead } from "../types";

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

export interface LeadListResult {
  items: Lead[];
  total: number;
  limit: number;
  offset: number;
}

export async function sendMessage(payload: MessagePayload): Promise<MessageResult> {
  const res = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.error?.message || body?.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export async function fetchLeads(params?: {
  status?: string;
  qualification?: string;
}): Promise<LeadListResult> {
  const qs = new URLSearchParams();
  if (params?.status) qs.set("status", params.status);
  if (params?.qualification) qs.set("qualification", params.qualification);
  const url = `${API_BASE}/leads${qs.toString() ? `?${qs}` : ""}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load leads (${res.status})`);
  return res.json();
}

export async function fetchLead(leadId: string): Promise<Lead> {
  const res = await fetch(`${API_BASE}/leads/${leadId}`);
  if (!res.ok) throw new Error(`Failed to load lead (${res.status})`);
  return res.json();
}
