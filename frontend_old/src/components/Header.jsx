import { FaChartLine } from "react-icons/fa";

function Header() {
  return (
    <header
      style={{
        background: "#1e293b",
        color: "white",
        padding: "20px 40px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderRadius: "12px",
        marginBottom: "30px",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
        <FaChartLine size={35} />
        <div>
          <h1 style={{ margin: 0 }}>NIFTY100 Financial Intelligence</h1>
          <p style={{ margin: 0, color: "#cbd5e1" }}>
            Financial Analytics Dashboard
          </p>
        </div>
      </div>

      <div
        style={{
          background: "#22c55e",
          padding: "8px 16px",
          borderRadius: "8px",
          fontWeight: "bold",
        }}
      >
        Backend Online
      </div>
    </header>
  );
}

export default Header;