import { Link } from "react-router-dom";

/** Sales lead dashboard — placeholder until backend list endpoint is live. */
export default function DashboardPage() {
  return (
    <div>
      <h1 style={{ marginTop: 0 }}>Sales Dashboard</h1>
      <p style={{ color: "#6b7280" }}>
        Lead list, filters (status, qualification, urgency), and quick actions will appear here.
      </p>
      <div
        style={{
          marginTop: 24,
          padding: 40,
          background: "#fff",
          borderRadius: 12,
          textAlign: "center",
          color: "#9ca3af",
        }}
      >
        No leads yet. Connect the backend <code>GET /api/leads</code> endpoint.
        <br />
        <Link to="/" style={{ marginTop: 12, display: "inline-block" }}>
          Try the customer chat →
        </Link>
      </div>
    </div>
  );
}
