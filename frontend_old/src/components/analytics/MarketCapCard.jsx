function MarketCapCard({ value }) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h3>🏢 Market Capitalization</h3>

      <h1
        style={{
          color: "#2563eb",
        }}
      >
        ₹ {Number(value || 0).toLocaleString("en-IN")} Cr
      </h1>
    </div>
  );
}

export default MarketCapCard;