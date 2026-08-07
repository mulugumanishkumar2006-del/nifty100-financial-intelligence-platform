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
  FaRobot,
  FaBrain,
  FaBriefcase,
  FaComments,
} from "react-icons/fa";

function Sidebar() {
  // ==========================================================
  // Navigation Item Style
  // ==========================================================

  const menuStyle = ({ isActive }) => ({
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "14px 18px",
    marginBottom: "12px",
    borderRadius: "12px",
    textDecoration: "none",

    color: isActive
      ? "#ffffff"
      : "#cbd5e1",

    background: isActive
      ? "linear-gradient(135deg,#2563eb,#1d4ed8)"
      : "transparent",

    fontWeight: "600",
    fontSize: "15px",

    transition: "all .3s ease",

    boxShadow: isActive
      ? "0 8px 20px rgba(37,99,235,.35)"
      : "none",
  });

  // ==========================================================
  // Navigation Items
  // ==========================================================

  const navItems = [
    {
      name: "Dashboard",
      path: "/",
      icon: <FaChartLine />,
      end: true,
    },

    {
      name: "Companies",
      path: "/companies",
      icon: <FaBuilding />,
    },

    {
      name: "Analytics",
      path: "/analytics",
      icon: <FaChartBar />,
    },

    {
      name: "Financial Ratios",
      path: "/financial-ratios",
      icon: <FaPercentage />,
    },

    {
      name: "Stock Prices",
      path: "/stock-prices",
      icon: <FaDatabase />,
    },

    {
      name: "Stock Screener",
      path: "/stock-screener",
      icon: <FaSearchDollar />,
    },

    {
      name: "Company Comparison",
      path: "/comparison",
      icon: <FaBalanceScale />,
    },

    {
      name: "AI Intelligence",
      path: "/intelligence",
      icon: <FaRobot />,
    },

    {
      name: "AI Insights",
      path: "/ai-insights",
      icon: <FaBrain />,
    },

    {
      name: "AI Assistant",
      path: "/ai-chat",
      icon: <FaComments />,
    },

    {
      name: "Portfolio",
      path: "/portfolio",
      icon: <FaBriefcase />,
    },
  ];

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <aside
      style={{
        width: "270px",
        minHeight: "100vh",

        background: "#0f172a",
        color: "#ffffff",

        padding: "25px",

        display: "flex",
        flexDirection: "column",

        boxSizing: "border-box",

        position: "sticky",
        top: 0,
      }}
    >
      {/* ======================================================
          Logo
      ====================================================== */}

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
            fontSize: "26px",
            fontWeight: "700",
          }}
        >
          📈 NIFTY100
        </h2>

        <p
          style={{
            color: "#94a3b8",
            marginTop: "8px",
            marginBottom: 0,
            fontSize: "13px",
            lineHeight: "1.5",
          }}
        >
          Financial Intelligence Platform
        </p>
      </div>

      {/* ======================================================
          Navigation
      ====================================================== */}

      <nav
        style={{
          flex: 1,
        }}
      >
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.end}
            style={menuStyle}
          >
            <span
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: "20px",
                fontSize: "16px",
              }}
            >
              {item.icon}
            </span>

            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      {/* ======================================================
          AI Workflow Indicator
      ====================================================== */}

      <div
        style={{
          background:
            "linear-gradient(135deg,#172554,#1e3a8a)",
          borderRadius: "12px",
          padding: "15px",
          marginTop: "15px",
          marginBottom: "20px",
          border: "1px solid #1e40af",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            color: "#93c5fd",
            fontWeight: "600",
            marginBottom: "6px",
          }}
        >
          🤖 AI WORKFLOW
        </div>

        <div
          style={{
            fontSize: "12px",
            color: "#dbeafe",
            lineHeight: "1.6",
          }}
        >
          Analyze → Understand → Investigate → Ask AI
        </div>
      </div>

      {/* ======================================================
          Footer
      ====================================================== */}

      <div
        style={{
          textAlign: "center",
          color: "#64748b",
          fontSize: "12px",
          paddingTop: "20px",
          borderTop: "1px solid #1e293b",
          lineHeight: "1.6",
        }}
      >
        <strong
          style={{
            color: "#94a3b8",
          }}
        >
          NIFTY100 Platform
        </strong>

        <br />

        Version 2.0

        <br />

        Bluestock FinTech Internship
      </div>
    </aside>
  );
}

export default Sidebar;