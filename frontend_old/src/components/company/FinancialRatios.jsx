function FinancialRatios({ company }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        marginTop: "30px",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: "20px",
        }}
      >
        📊 Financial Ratios
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        <RatioCard
          title="ROE"
          value={company.roe_percentage}
          color="#2563eb"
        />

        <RatioCard
          title="ROCE"
          value={company.roce_percentage}
          color="#16a34a"
        />

        <RatioCard
          title="P/E Ratio"
          value={company.pe_ratio}
          color="#dc2626"
        />

        <RatioCard
          title="EPS"
          value={company.eps}
          color="#7c3aed"
        />

        <RatioCard
          title="Book Value"
          value={company.book_value}
          color="#0891b2"
        />

        <RatioCard
          title="Face Value"
          value={company.face_value}
          color="#ea580c"
        />
      </div>
    </div>
  );
}

function RatioCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#f9fafb",
        padding: "20px",
        borderRadius: "10px",
        borderLeft: `6px solid ${color}`,
      }}
    >
      <h3
        style={{
          marginBottom: "10px",
          color: "#374151",
        }}
      >
        {title}
      </h3>

      <p
        style={{
          fontSize: "26px",
          fontWeight: "700",
          color: color,
        }}
      >
        {value ?? "-"}
      </p>
    </div>
  );
}

export default FinancialRatios;