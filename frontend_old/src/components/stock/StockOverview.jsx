function Card({ title, value, color }) {
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
        }}
      >
        {value}
      </h2>
    </div>
  );
}

function StockOverview({ stocks = [] }) {
  if (!stocks.length) return null;

  const parsePrice = (value) =>
    Number(String(value).replace(/[₹,]/g, ""));

  const parseVolume = (value) =>
    Number(String(value).replace("M", ""));

  const highest = Math.max(
    ...stocks.map((stock) => parsePrice(stock.high52))
  );

  const lowest = Math.min(
    ...stocks.map((stock) => parsePrice(stock.low52))
  );

  const average =
    (
      stocks.reduce(
        (sum, stock) =>
          sum + parsePrice(stock.price),
        0
      ) / stocks.length
    ).toFixed(2);

  const totalVolume = stocks.reduce(
    (sum, stock) =>
      sum + parseVolume(stock.volume),
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
        title="📈 Highest 52W High"
        value={`₹ ${highest.toLocaleString("en-IN")}`}
        color="#16a34a"
      />

      <Card
        title="📉 Lowest 52W Low"
        value={`₹ ${lowest.toLocaleString("en-IN")}`}
        color="#dc2626"
      />

      <Card
        title="💹 Average Price"
        value={`₹ ${Number(average).toLocaleString("en-IN")}`}
        color="#2563eb"
      />

      <Card
        title="📊 Total Volume"
        value={`${totalVolume.toFixed(1)} M`}
        color="#9333ea"
      />
    </div>
  );
}

export default StockOverview;