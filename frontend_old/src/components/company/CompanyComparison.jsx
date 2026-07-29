import React from "react";

function CompanyComparison({ company }) {
  if (!company) return null;

  const metrics = [
    {
      title: "Book Value",
      value: company.book_value,
      color: "#2563eb",
    },
    {
      title: "ROE %",
      value: company.roe_percentage,
      color: "#16a34a",
    },
    {
      title: "ROCE %",
      value: company.roce_percentage,
      color: "#dc2626",
    },
    {
      title: "P/E Ratio",
      value: company.pe_ratio,
      color: "#9333ea",
    },
    {
      title: "EPS",
      value: company.eps,
      color: "#f59e0b",
    },
    {
      title: "Face Value",
      value: company.face_value,
      color: "#0891b2",
    },
  ];

  return (
    <div
      style={{
        marginTop: "35px",
        background: "#fff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          color: "#1f2937",
        }}
      >
        📈 Company Performance Snapshot
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        {metrics.map((item) => (
          <div
            key={item.title}
            style={{
              background: "#f9fafb",
              padding: "20px",
              borderRadius: "12px",
              borderLeft: `6px solid ${item.color}`,
            }}
          >
            <h4>{item.title}</h4>

            <h2
              style={{
                color: item.color,
                marginTop: "10px",
              }}
            >
              {item.value ?? "-"}
            </h2>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CompanyComparison;