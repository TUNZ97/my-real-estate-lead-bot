import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchLeads } from "../services/api";
import type { Lead } from "../types";

function qualBadge(level?: string | null) {
  if (!level) return "badge-unknown";
  const l = level.toUpperCase();
  if (l === "HIGH") return "badge-high";
  if (l === "MEDIUM") return "badge-medium";
  if (l === "LOW") return "badge-low";
  return "badge-unknown";
}

function formatBudget(min?: number | null, max?: number | null, currency = "NGN") {
  const fmt = (n: number) =>
    n >= 1_000_000 ? `₦${(n / 1_000_000).toFixed(0)}m` : `₦${n.toLocaleString()}`;
  if (min != null && max != null && min !== max) return `${fmt(min)} – ${fmt(max)}`;
  if (max != null) return `Below ${fmt(max)}`;
  if (min != null) return `Around ${fmt(min)}`;
  return "—";
}

export default function DashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLeads()
      .then((res) => {
        setLeads(res.items);
        setTotal(res.total);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24, color: "var(--slate-900)" }}>Sales Dashboard</h1>
          <p style={{ margin: "4px 0 0", color: "var(--gray-500)", fontSize: 14 }}>
            {total} lead{total !== 1 ? "s" : ""} total
          </p>
        </div>
        <Link
          to="/"
          style={{
            padding: "10px 18px",
            borderRadius: 10,
            background: "linear-gradient(135deg, #ea580c, #f97316)",
            color: "#fff",
            fontWeight: 600,
            fontSize: 14,
          }}
        >
          + New enquiry
        </Link>
      </div>

      {loading && (
        <div style={{ textAlign: "center", padding: 48, color: "var(--gray-500)" }}>Loading leads…</div>
      )}

      {error && (
        <div
          style={{
            padding: 20,
            background: "#fef2f2",
            borderRadius: 12,
            color: "#991b1b",
            marginBottom: 16,
          }}
        >
          {error}. Make sure the backend is running on port 8000.
        </div>
      )}

      {!loading && !error && leads.length === 0 && (
        <div
          style={{
            padding: 48,
            background: "var(--white)",
            borderRadius: 12,
            textAlign: "center",
            boxShadow: "var(--shadow-sm)",
            border: "1px solid var(--orange-100)",
          }}
        >
          <p style={{ color: "var(--gray-500)", marginBottom: 12 }}>No leads yet.</p>
          <Link to="/" style={{ fontWeight: 600 }}>
            Start a customer chat →
          </Link>
        </div>
      )}

      {leads.length > 0 && (
        <div
          style={{
            background: "var(--white)",
            borderRadius: 12,
            boxShadow: "var(--shadow)",
            border: "1px solid var(--orange-100)",
            overflow: "hidden",
          }}
        >
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ background: "var(--orange-50)", textAlign: "left" }}>
                {["Intent", "Property", "Location", "Budget", "Qualification", "Urgency", "Status", ""].map(
                  (h) => (
                    <th
                      key={h}
                      style={{
                        padding: "12px 16px",
                        fontWeight: 600,
                        color: "var(--orange-700)",
                        fontSize: 12,
                        textTransform: "uppercase",
                        letterSpacing: "0.04em",
                      }}
                    >
                      {h}
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr
                  key={lead.id}
                  style={{ borderTop: "1px solid var(--gray-100)" }}
                >
                  <td style={{ padding: "14px 16px" }}>{lead.intent || "—"}</td>
                  <td style={{ padding: "14px 16px" }}>
                    {lead.bedrooms ? `${lead.bedrooms}-bed ` : ""}
                    {lead.property_type || "—"}
                  </td>
                  <td style={{ padding: "14px 16px" }}>{lead.location_text || "—"}</td>
                  <td style={{ padding: "14px 16px" }}>
                    {formatBudget(lead.budget_min, lead.budget_max, lead.currency || undefined)}
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <span className={`badge ${qualBadge(lead.qualification_level)}`}>
                      {lead.qualification_level || "—"}
                      {lead.qualification_score != null ? ` (${lead.qualification_score})` : ""}
                    </span>
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <span className={`badge ${qualBadge(lead.urgency)}`}>
                      {lead.urgency || "—"}
                    </span>
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <span className="badge badge-status">{lead.status}</span>
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <Link
                      to={`/leads/${lead.id}`}
                      style={{ fontWeight: 600, fontSize: 13 }}
                    >
                      View →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
