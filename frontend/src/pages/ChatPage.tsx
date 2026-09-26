import { useState, FormEvent, useRef, useEffect } from "react";
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
  const [leadId, setLeadId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
      if (res.lead_id) setLeadId(res.lead_id);
      if (res.response) {
        setMessages((prev) => [
          ...prev,
          {
            id: res.message_id || crypto.randomUUID(),
            role: "bot",
            content: res.response!,
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "bot",
          content:
            "Sorry, something went wrong. Please try again or ask to speak with an agent.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  const examples = [
    "I’m looking for a 3-bedroom apartment around Lekki. Budget is around N80 million.",
    "Do you have any 2-bedroom apartments in Ikeja?",
    "I need land around Ibadan, preferably below N20 million.",
  ];

  return (
    <div
      style={{
        maxWidth: 680,
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 140px)",
        background: "var(--white)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow)",
        overflow: "hidden",
        border: "1px solid var(--orange-100)",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "16px 20px",
          background: "linear-gradient(90deg, var(--orange-50), #fffbeb)",
          borderBottom: "1px solid var(--orange-100)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <h1 style={{ margin: 0, fontSize: 18, color: "var(--slate-900)" }}>
            Property Enquiry
          </h1>
          <p style={{ margin: "2px 0 0", fontSize: 13, color: "var(--gray-500)" }}>
            Tell us what you’re looking for — buy, rent or sell
          </p>
        </div>
        {leadId && (
          <span className="badge badge-status" title="Lead created">
            Lead active
          </span>
        )}
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: 20 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", marginTop: 32 }}>
            <div
              style={{
                width: 56,
                height: 56,
                borderRadius: 16,
                background: "linear-gradient(135deg, var(--orange-400), var(--yellow-400))",
                margin: "0 auto 16px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 24,
              }}
            >
              🏠
            </div>
            <p style={{ color: "var(--gray-500)", marginBottom: 20, fontSize: 14 }}>
              Try one of these examples:
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {examples.map((ex) => (
                <button
                  key={ex}
                  type="button"
                  onClick={() => setInput(ex)}
                  style={{
                    textAlign: "left",
                    padding: "10px 14px",
                    borderRadius: 10,
                    border: "1px solid var(--orange-200)",
                    background: "var(--orange-50)",
                    color: "var(--slate-800)",
                    fontSize: 13,
                    cursor: "pointer",
                  }}
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m) => (
          <div
            key={m.id}
            style={{
              marginBottom: 14,
              display: "flex",
              justifyContent: m.role === "customer" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "82%",
                padding: "12px 16px",
                borderRadius:
                  m.role === "customer" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
                background:
                  m.role === "customer"
                    ? "linear-gradient(135deg, #ea580c, #f97316)"
                    : "var(--gray-100)",
                color: m.role === "customer" ? "#fff" : "var(--slate-900)",
                fontSize: 14,
                lineHeight: 1.55,
                boxShadow: m.role === "customer" ? "0 2px 8px rgba(234,88,12,0.25)" : "none",
              }}
            >
              {m.content}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", gap: 6, padding: "8px 0" }}>
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "var(--orange-400)",
                  animation: `pulse 1.2s ease-in-out ${i * 0.2}s infinite`,
                }}
              />
            ))}
            <style>{`@keyframes pulse { 0%, 80%, 100% { opacity: 0.3; } 40% { opacity: 1; } }`}</style>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          gap: 10,
          padding: 16,
          borderTop: "1px solid var(--orange-100)",
          background: "var(--orange-50)",
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
            padding: "12px 16px",
            borderRadius: 10,
            border: "1px solid var(--orange-200)",
            fontSize: 14,
            outline: "none",
            background: "var(--white)",
          }}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            padding: "12px 22px",
            borderRadius: 10,
            border: "none",
            background: loading || !input.trim()
              ? "var(--gray-200)"
              : "linear-gradient(135deg, #ea580c, #f97316)",
            color: loading || !input.trim() ? "var(--gray-500)" : "#fff",
            fontWeight: 600,
            fontSize: 14,
            transition: "all 0.15s",
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}
