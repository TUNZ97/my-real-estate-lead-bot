import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchLead } from "../services/api";
import type { Lead } from "../types";

function qualBadge(level?: string | null) {
  if (!level) return "badge-unknown";
  const l = level.toUpperCase();
  if (l === "HIGH") return "badge-high";
  if (l === "MEDIUM") return "badge-medium";
  if (l === "LOW") return "badge-low";
  return "badge-unknown";
}

export default function LeadDetailPage() {
  const { leadId } = useParams();
  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!leadId) return;
    fetchLead(leadId)
      .then(setLead)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [leadId]);

  if (loading) return <p style={{ color: "var(--gray-500)" }}>Loading…</p>;
  if (error) return <p style={{ color: "#991b1b" }}>{error}</p>;
  if (!lead) return <p>Lead not found.</p>;

  const rows: [string, string][] = [
    ["Status", lead.status],
    ["Intent", lead.intent || "—"],
    ["Property type", lead.property_type || "—"],
    ["Bedrooms", lead.bedrooms != null ? String(lead.bedrooms) : "—"],
    ["Location", lead.location_text || "—"],
    [
      "Budget",
      lead.budget_min || lead.budget_max
        ? `₦${lead.budget_min?.toLocaleString() || "?"} – ₦${lead.budget_max?.toLocaleString() || "?"}`
        : "—",
    ],
    ["Timeframe", lead.timeframe || "—"],
    ["Qualification", `${lead.qualification_level || "—"} (${lead.qualification_score ?? "—"})`],
    ["Urgency", lead.urgency || "—"],
    ["Created", new Date(lead.created_at).toLocaleString()],
  ];

  return (
    <div style={{ maxWidth: 640, margin: "0 auto" }}>
      <Link to="/dashboard" style={{ fontSize: 14, fontWeight: 500 }}>
        ← Back to dashboard
      </Link>
      <h1 style={{ margin: "12px 0 4px", fontSize: 22 }}>Lead Detail</h1>
      <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 24 }}>
        ID: {lead.id}
      </p>

      <div
        style={{
          background: "var(--white)",
          borderRadius: 12,
          boxShadow: "var(--shadow)",
          border: "1px solid var(--orange-100)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            padding: "14px 20px",
            background: "linear-gradient(90deg, var(--orange-50), #fffbeb)",
            borderBottom: "1px solid var(--orange-100)",
            display: "flex",
            gap: 10,
          }}
        >
          <span className={`badge ${qualBadge(lead.qualification_level)}`}>
            {lead.qualification_level || "UNKNOWN"}
          </span>
          <span className={`badge ${qualBadge(lead.urgency)}`}>
            Urgency: {lead.urgency || "UNKNOWN"}
          </span>
          <span className="badge badge-status">{lead.status}</span>
        </div>

        <dl style={{ margin: 0, padding: "8px 0" }}>
          {rows.map(([label, value]) => (
            <div
              key={label}
              style={{
                display: "grid",
                gridTemplateColumns: "140px 1fr",
                padding: "10px 20px",
                borderBottom: "1px solid var(--gray-100)",
                fontSize: 14,
              }}
            >
              <dt style={{ color: "var(--gray-500)", fontWeight: 500 }}>{label}</dt>
              <dd style={{ margin: 0, color: "var(--slate-900)" }}>{value}</dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  );
}
