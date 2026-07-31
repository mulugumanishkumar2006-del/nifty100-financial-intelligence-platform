function AIInsightsCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "15px",
        padding: "25px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        borderTop: `6px solid ${color}`,
      }}
    >
      <h3
        style={{
          color: "#64748b",
          marginBottom: "10px",
        }}
      >
        {title}
      </h3>

      <h1
        style={{
          color,
          margin: 0,
          fontSize: "30px",
        }}
      >
        {value}
      </h1>
    </div>
  );
}

export default AIInsightsCard;