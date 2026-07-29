function Card({ title, value, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "22px",
        borderRadius: "14px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${color}`,
      }}
    >
      <h4
        style={{
          color: "#6b7280",
          marginBottom: "10px",
          fontSize: "15px",
        }}
      >
        {title}
      </h4>

      <h2
        style={{
          margin: 0,
          color,
          fontSize: "28px",
          fontWeight: "700",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

function StockStats({ stocks = [] }) {
  if (!stocks.length) return null;

  const highestClose = Math.max(
    ...stocks.map((s) => Number(s.close || 0))
  );

  const lowestClose = Math.min(
    ...stocks.map((s) => Number(s.close || 0))
  );

  const highestHigh = Math.max(
    ...stocks.map((s) => Number(s.high || 0))
  );

  const lowestLow = Math.min(
    ...stocks.map((s) => Number(s.low || 0))
  );

  const averageClose = (
    stocks.reduce(
      (sum, s) => sum + Number(s.close || 0),
      0
    ) / stocks.length
  ).toFixed(2);

  const totalVolume = stocks.reduce(
    (sum, s) => sum + Number(s.volume || 0),
    0
  );

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit,minmax(220px,1fr))",
        gap: "20px",
        marginBottom: "30px",
      }}
    >
      <Card
        title="Highest Close"
        value={`₹ ${highestClose}`}
        color="#16a34a"
      />

      <Card
        title="Lowest Close"
        value={`₹ ${lowestClose}`}
        color="#dc2626"
      />

      <Card
        title="Highest High"
        value={`₹ ${highestHigh}`}
        color="#2563eb"
      />

      <Card
        title="Lowest Low"
        value={`₹ ${lowestLow}`}
        color="#f59e0b"
      />

      <Card
        title="Average Close"
        value={`₹ ${averageClose}`}
        color="#9333ea"
      />

      <Card
        title="Total Volume"
        value={totalVolume.toLocaleString()}
        color="#0f766e"
      />
    </div>
  );
}

export default StockStats;