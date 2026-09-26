import { Routes, Route, Link, useLocation } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import LeadDetailPage from "./pages/LeadDetailPage";

export default function App() {
  const location = useLocation();

  const linkStyle = (path: string) => ({
    color: location.pathname === path ? "#fff" : "rgba(255,255,255,0.7)",
    fontWeight: location.pathname === path ? 600 : 400,
    padding: "6px 12px",
    borderRadius: 8,
    background: location.pathname === path ? "rgba(255,255,255,0.15)" : "transparent",
    transition: "all 0.15s ease",
  });

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          padding: "14px 28px",
          background: "linear-gradient(135deg, #ea580c 0%, #f97316 50%, #eab308 100%)",
          color: "#fff",
          display: "flex",
          gap: 28,
          alignItems: "center",
          boxShadow: "0 2px 12px rgba(234, 88, 12, 0.3)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              background: "rgba(255,255,255,0.25)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 700,
              fontSize: 18,
            }}
          >
            P
          </div>
          <strong style={{ fontSize: 17, letterSpacing: "-0.02em" }}>
            PrimeHomes Lead Bot
          </strong>
        </div>
        <nav style={{ display: "flex", gap: 8, marginLeft: "auto" }}>
          <Link to="/" style={linkStyle("/")}>
            Customer Chat
          </Link>
          <Link to="/dashboard" style={linkStyle("/dashboard")}>
            Sales Dashboard
          </Link>
        </nav>
      </header>
      <main style={{ flex: 1, padding: "28px 20px" }}>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/leads/:leadId" element={<LeadDetailPage />} />
        </Routes>
      </main>
    </div>
  );
}
