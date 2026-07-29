function RatioOverview({ ratios = [] }) {
  if (!ratios.length) return null;

  const highestROE = [...ratios].sort(
    (a, b) => (b.roe_percentage || 0) - (a.roe_percentage || 0)
  )[0];

  const highestROCE = [...ratios].sort(
    (a, b) => (b.roce_percentage || 0) - (a.roce_percentage || 0)
  )[0];

  const highestEPS = [...ratios].sort(
    (a, b) => (b.eps || 0) - (a.eps || 0)
  )[0];

  const averagePE =
    (
      ratios.reduce(
        (sum, item) => sum + (item.pe_ratio || 0),
        0
      ) / ratios.length
    ).toFixed(2);

  const cardStyle = {
    background: "#ffffff",
    borderRadius: "12px",
    padding: "20px",
    boxShadow: "0 6px 15px rgba(0,0,0,0.08)",
  };

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit,minmax(250px,1fr))",
        gap: "20px",
        marginBottom: "30px",
      }}
    >
      <div style={cardStyle}>
        <h3>🏆 Highest ROE</h3>
        <h2>{highestROE?.company_name}</h2>
        <p>{highestROE?.roe_percentage}%</p>
      </div>

      <div style={cardStyle}>
        <h3>🏆 Highest ROCE</h3>
        <h2>{highestROCE?.company_name}</h2>
        <p>{highestROCE?.roce_percentage}%</p>
      </div>

      <div style={cardStyle}>
        <h3>💰 Highest EPS</h3>
        <h2>{highestEPS?.company_name}</h2>
        <p>{highestEPS?.eps}</p>
      </div>

      <div style={cardStyle}>
        <h3>📊 Average P/E</h3>
        <h2>{averagePE}</h2>
      </div>
    </div>
  );
}

export default RatioOverview;