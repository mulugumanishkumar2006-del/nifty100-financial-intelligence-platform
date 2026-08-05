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
      ? "linear-gradient(135deg,#2563eb,#1d4ed8)"
      : "transparent",

    fontWeight: "600",
    fontSize: "15px",

    transition: "all .3s ease",

    boxShadow: isActive
      ? "0 8px 20px rgba(37,99,235,.35)"
      : "none",
  });

  const navItems = [

    {
      name: "Dashboard",
      path: "/",
      icon: <FaChartLine />,
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
      name: "Portfolio",
      path: "/portfolio",
      icon: <FaBriefcase />,
    },

  ];

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
      }}
    >

      {/* ================= Logo ================= */}

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
          }}
        >
          📈 NIFTY100
        </h2>

        <p
          style={{
            color: "#94a3b8",
            marginTop: "8px",
            fontSize: "13px",
          }}
        >
          Financial Intelligence Platform
        </p>

      </div>

      {/* ================= Navigation ================= */}

      <nav>

        {navItems.map((item) => (

          <NavLink
            key={item.path}
            to={item.path}
            style={menuStyle}
          >

            {item.icon}

            {item.name}

          </NavLink>

        ))}

      </nav>

      {/* ================= Footer ================= */}

      <div
        style={{
          marginTop: "auto",
          textAlign: "center",
          color: "#64748b",
          fontSize: "12px",
          paddingTop: "30px",
          borderTop: "1px solid #1e293b",
        }}
      >

        <strong>NIFTY100 Platform</strong>

        <br />

        Version 2.0

        <br />

        Bluestock FinTech Internship

      </div>

    </aside>

  );
}

export default Sidebar;