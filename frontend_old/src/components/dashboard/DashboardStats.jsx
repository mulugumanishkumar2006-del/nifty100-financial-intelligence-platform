function StatCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "14px",
        padding: "20px",
        boxShadow: "0 5px 18px rgba(0,0,0,.08)",
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
        }}
      >
        {value}
      </h2>
    </div>
  );
}

function DashboardStats({
  companies,
  sectors,
  avgROE,
  totalMarketCap,
}) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit,minmax(220px,1fr))",
        gap: "20px",
        marginBottom: "35px",
      }}
    >
      <StatCard
        title="Companies"
        value={companies}
        color="#2563eb"
      />

      <StatCard
        title="Sectors"
        value={sectors}
        color="#16a34a"
      />

      <StatCard
        title="Average ROE"
        value={`${avgROE}%`}
        color="#9333ea"
      />

      <StatCard
        title="Market Cap"
        value={totalMarketCap}
        color="#f59e0b"
      />
    </div>
  );
}

export default DashboardStats;