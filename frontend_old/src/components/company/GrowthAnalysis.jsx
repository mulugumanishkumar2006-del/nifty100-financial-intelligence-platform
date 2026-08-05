function GrowthAnalysis({ company }) {
  const profitLoss = company?.profit_loss || [];

  // Sort by year (oldest -> newest)
  const sortedData = [...profitLoss].sort(
    (a, b) => Number(a.year) - Number(b.year)
  );

  if (sortedData.length < 2) {
    return (
      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "15px",
          marginTop: "30px",
          boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        }}
      >
        <h2 style={{ color: "#2563eb" }}>
          📈 Growth Analysis
        </h2>

        <p style={{ color: "#64748b" }}>
          Not enough financial data available.
        </p>
      </div>
    );
  }

  const latest = sortedData[sortedData.length - 1];
  const previous = sortedData[sortedData.length - 2];

  function calculateGrowth(current, previous) {
    current = Number(current || 0);
    previous = Number(previous || 0);

    if (previous === 0) return 0;

    return (((current - previous) / previous) * 100).toFixed(2);
  }

  const revenueGrowth = calculateGrowth(
    latest.sales,
    previous.sales
  );

  const profitGrowth = calculateGrowth(
    latest.net_profit,
    previous.net_profit
  );

  const epsGrowth = calculateGrowth(
    latest.eps,
    previous.eps
  );

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        marginTop: "30px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: "20px",
        }}
      >
        📈 Growth Analysis
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        <GrowthCard
          title="Revenue Growth"
          value={`${revenueGrowth}%`}
          positive={Number(revenueGrowth) >= 0}
        />

        <GrowthCard
          title="Profit Growth"
          value={`${profitGrowth}%`}
          positive={Number(profitGrowth) >= 0}
        />

        <GrowthCard
          title="EPS Growth"
          value={`${epsGrowth}%`}
          positive={Number(epsGrowth) >= 0}
        />

        <GrowthCard
          title="Financial Year"
          value={latest.year}
          positive={true}
        />
      </div>
    </div>
  );
}

function GrowthCard({
  title,
  value,
  positive,
}) {
  return (
    <div
      style={{
        background: "#f8fafc",
        padding: "20px",
        borderRadius: "12px",
        borderLeft: `6px solid ${
          positive ? "#16a34a" : "#dc2626"
        }`,
        transition: "0.3s",
      }}
    >
      <p
        style={{
          margin: 0,
          fontSize: "14px",
          color: "#64748b",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop: "12px",
          marginBottom: 0,
          color: positive ? "#16a34a" : "#dc2626",
          fontWeight: "700",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default GrowthAnalysis;