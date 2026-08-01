import React from "react";

function SummaryCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${color}`,
      }}
    >
      <h4
        style={{
          color: "#6b7280",
          marginBottom: "10px",
        }}
      >
        {title}
      </h4>

      <h2
        style={{
          margin: 0,
          color,
          fontWeight: "700",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

function PortfolioSummary() {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))",
        gap: "20px",
        marginBottom: "30px",
      }}
    >
      <SummaryCard
        title="Total Investment"
        value="₹12,50,000"
        color="#2563eb"
      />

      <SummaryCard
        title="Current Value"
        value="₹13,78,000"
        color="#16a34a"
      />

      <SummaryCard
        title="Profit / Loss"
        value="+₹1,28,000"
        color="#dc2626"
      />

      <SummaryCard
        title="Holdings"
        value="18"
        color="#9333ea"
      />
    </div>
  );
}

export default PortfolioSummary;