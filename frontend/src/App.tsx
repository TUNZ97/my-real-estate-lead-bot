import { Routes, Route, Link } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import LeadDetailPage from "./pages/LeadDetailPage";

export default function App() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          padding: "12px 24px",
          background: "#0f172a",
          color: "#fff",
          display: "flex",
          gap: "24px",
          alignItems: "center",
        }}
      >
        <strong>PrimeHomes Lead Bot</strong>
        <nav style={{ display: "flex", gap: "16px" }}>
          <Link to="/" style={{ color: "#94a3b8" }}>
            Customer Chat
          </Link>
          <Link to="/dashboard" style={{ color: "#94a3b8" }}>
            Sales Dashboard
          </Link>
        </nav>
      </header>
      <main style={{ flex: 1, padding: "24px" }}>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/leads/:leadId" element={<LeadDetailPage />} />
        </Routes>
      </main>
    </div>
  );
}
