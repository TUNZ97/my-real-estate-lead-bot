import { useState, FormEvent } from "react";
import { sendMessage } from "../services/api";

interface ChatMessage {
  id: string;
  role: "customer" | "bot";
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "customer",
      content: input.trim(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendMessage({
        message: userMsg.content,
        conversation_id: conversationId ?? undefined,
      });
      if (res.conversation_id) setConversationId(res.conversation_id);
      if (res.response) {
        setMessages((prev) => [
          ...prev,
          { id: res.message_id || crypto.randomUUID(), role: "bot", content: res.response! },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "bot",
          content: "Sorry, something went wrong. Please try again or request a human agent.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        maxWidth: 640,
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 120px)",
        background: "#fff",
        borderRadius: 12,
        boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
        overflow: "hidden",
      }}
    >
      <div style={{ padding: "16px 20px", borderBottom: "1px solid #e5e7eb" }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>Property Enquiry</h1>
        <p style={{ margin: "4px 0 0", fontSize: 13, color: "#6b7280" }}>
          Tell us what you are looking for — buy, rent, or sell.
        </p>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: 20 }}>
        {messages.length === 0 && (
          <p style={{ color: "#9ca3af", textAlign: "center", marginTop: 40 }}>
            e.g. “I’m looking for a 3-bedroom apartment around Lekki. Budget is around N80 million.”
          </p>
        )}
        {messages.map((m) => (
          <div
            key={m.id}
            style={{
              marginBottom: 12,
              display: "flex",
              justifyContent: m.role === "customer" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "80%",
                padding: "10px 14px",
                borderRadius: 12,
                background: m.role === "customer" ? "#0f172a" : "#f3f4f6",
                color: m.role === "customer" ? "#fff" : "#1f2937",
                fontSize: 14,
              }}
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ color: "#9ca3af", fontSize: 13 }}>Processing…</div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          gap: 8,
          padding: 16,
          borderTop: "1px solid #e5e7eb",
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message…"
          disabled={loading}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: 8,
            border: "1px solid #d1d5db",
            fontSize: 14,
          }}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            padding: "10px 18px",
            borderRadius: 8,
            border: "none",
            background: "#0f172a",
            color: "#fff",
            fontWeight: 500,
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}
