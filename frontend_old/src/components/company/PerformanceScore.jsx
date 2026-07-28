function calculateScore(company) {
  let score = 0;

  score += Number(company.roe_percentage || 0);

  score += Number(company.roce_percentage || 0);

  score += Number(company.book_value || 0) / 10;

  if (score > 100) score = 100;

  return Math.round(score);
}

function getRating(score) {
  if (score >= 90)
    return {
      text: "Excellent",
      color: "#16a34a",
    };

  if (score >= 75)
    return {
      text: "Good",
      color: "#2563eb",
    };

  if (score >= 60)
    return {
      text: "Average",
      color: "#f59e0b",
    };

  return {
    text: "Weak",
    color: "#dc2626",
  };
}

function PerformanceScore({ company }) {
  const score = calculateScore(company);

  const rating = getRating(score);

  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,.08)",
      }}
    >
      <h2>Performance Score</h2>

      <div
        style={{
          fontSize: "50px",
          fontWeight: "700",
          color: rating.color,
        }}
      >
        {score}
      </div>

      <div
        style={{
          fontSize: "20px",
          color: rating.color,
          fontWeight: "600",
        }}
      >
        {rating.text}
      </div>

      <progress
        value={score}
        max="100"
        style={{
          width: "100%",
          marginTop: "20px",
          height: "15px",
        }}
      />
    </div>
  );
}

export default PerformanceScore;