import React from "react";
import { NavLink } from "react-router-dom";
import {
  FaChartLine,
  FaBuilding,
  FaChartBar,
  FaPercentage,
  FaDatabase,
  FaSearchDollar,
  FaBalanceScale,
  FaBriefcase,
} from "react-icons/fa";

function Sidebar() {
  const menuStyle = ({ isActive }) => ({
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "14px 18px",
    marginBottom: "12px",
    borderRadius: "12px",
    textDecoration: "none",
    color: isActive ? "#ffffff" : "#cbd5e1",
    background: isActive
      ? "linear-gradient(135deg, #2563eb, #1d4ed8)"
      : "transparent",
    fontWeight: "600",
    fontSize: "15px",
    transition: "all 0.3s ease",
    boxShadow: isActive ? "0 8px 20px rgba(37, 99, 235, 0.35)" : "none",
  });

  const navItems = [
    { name: "Dashboard", path: "/", icon: <FaChartLine /> },
    { name: "Companies", path: "/companies", icon: <FaBuilding /> },
    { name: "Analytics", path: "/analytics", icon: <FaChartBar /> },
    { name: "Financial Ratios", path: "/financial-ratios", icon: <FaPercentage /> },
    { name: "Stock Prices", path: "/stock-prices", icon: <FaDatabase /> },
    { name: "Stock Screener", path: "/stock-screener", icon: <FaSearchDollar /> },
    { name: "Compare", path: "/compare", icon: <FaBalanceScale /> },
    { name: "Portfolio", path: "/portfolio", icon: <FaBriefcase /> },
  ];

  return (
    <aside
      style={{
        width: "260px",
        minHeight: "100vh",
        background: "#0f172a",
        color: "#ffffff",
        padding: "25px",
        display: "flex",
        flexDirection: "column",
        boxSizing: "border-box",
      }}
    >
      {/* Logo Section */}
      <div style={{ textAlign: "center", marginBottom: "40px" }}>
        <h2 style={{ margin: 0, color: "#60a5fa", fontSize: "24px" }}>
          📈 NIFTY100
        </h2>
        <p style={{ color: "#94a3b8", fontSize: "13px", marginTop: "8px" }}>
          Financial Intelligence
        </p>
      </div>

      {/* Navigation List */}
      <nav>
        {navItems.map((item) => (
          <NavLink key={item.path} to={item.path} style={menuStyle}>
            {item.icon}
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Sidebar Footer */}
      <div
        style={{
          marginTop: "auto",
          textAlign: "center",
          color: "#64748b",
          fontSize: "12px",
          paddingTop: "30px",
        }}
      >
        Version 1.0
        <br />
        Bluestock FinTech Internship
      </div>
    </aside>
  );
}

export default Sidebar;