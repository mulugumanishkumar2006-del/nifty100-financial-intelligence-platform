import { NavLink } from "react-router-dom";
import {
  FaChartLine,
  FaBuilding,
  FaChartBar,
  FaPercentage,
  FaDatabase,
} from "react-icons/fa";

function Sidebar() {
  const menuStyle = ({ isActive }) => ({
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "14px 18px",
    marginBottom: "12px",
    borderRadius: "10px",
    textDecoration: "none",
    color: isActive ? "#ffffff" : "#d1d5db",
    background: isActive ? "#2563eb" : "transparent",
    transition: "0.3s",
    fontWeight: "600",
    fontSize: "15px",
  });

  return (
    <div
      style={{
        width: "260px",
        background: "#111827",
        color: "#ffffff",
        padding: "25px",
        minHeight: "100vh",
        boxSizing: "border-box",
      }}
    >
      {/* Logo */}

      <div
        style={{
          textAlign: "center",
          marginBottom: "40px",
        }}
      >
        <h2
          style={{
            margin: 0,
            color: "#60a5fa",
          }}
        >
          📈 NIFTY100
        </h2>

        <p
          style={{
            color: "#9ca3af",
            fontSize: "13px",
            marginTop: "8px",
          }}
        >
          Financial Intelligence
        </p>
      </div>

      {/* Navigation */}

      <NavLink to="/" style={menuStyle}>
        <FaChartLine />
        Dashboard
      </NavLink>

      <NavLink to="/companies" style={menuStyle}>
        <FaBuilding />
        Companies
      </NavLink>

      <NavLink to="/analytics" style={menuStyle}>
        <FaChartBar />
        Analytics
      </NavLink>

      <NavLink to="/financial-ratios" style={menuStyle}>
        <FaPercentage />
        Financial Ratios
      </NavLink>

      <NavLink to="/stock-prices" style={menuStyle}>
        <FaDatabase />
        Stock Prices
      </NavLink>

      {/* Footer */}

      <div
        style={{
          position: "absolute",
          bottom: "20px",
          width: "210px",
          color: "#6b7280",
          fontSize: "12px",
          textAlign: "center",
        }}
      >
        Version 1.0
        <br />
        Bluestock FinTech Internship
      </div>
    </div>
  );
}

export default Sidebar;