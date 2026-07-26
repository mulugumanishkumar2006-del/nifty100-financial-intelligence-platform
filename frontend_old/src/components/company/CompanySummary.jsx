function CompanySummary({ company }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
        gap: "20px",
        marginBottom: "30px",
      }}
    >
      <SummaryCard
        title="Book Value"
        value={company.book_value}
      />

      <SummaryCard
        title="Face Value"
        value={company.face_value}
      />

      <SummaryCard
        title="ROE (%)"
        value={company.roe_percentage}
      />

      <SummaryCard
        title="ROCE (%)"
        value={company.roce_percentage}
      />
    </div>
  );
}

function SummaryCard({ title, value }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
      }}
    >
      <p
        style={{
          color: "#6b7280",
          fontSize: "14px",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop: "10px",
          color: "#2563eb",
        }}
      >
        {value ?? "-"}
      </h2>
    </div>
  );
}

export default CompanySummary;