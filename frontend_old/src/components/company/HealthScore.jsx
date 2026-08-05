import { useEffect, useState } from "react";
import { getHealthScore } from "../../services/companyService";

function HealthScore({ company }) {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    async function loadHealth() {
      if (!company?.id) return;

      const data = await getHealthScore(company.id);
      setHealth(data);
    }

    loadHealth();
  }, [company]);

  if (!health) {
    return (
      <div className="card">
        <h3>Health Score</h3>
        <p>Loading...</p>
      </div>
    );
  }

  const score = health.health_score || 0;

  let color = "#ef4444";

  if (score >= 80) color = "#22c55e";
  else if (score >= 60) color = "#3b82f6";
  else if (score >= 40) color = "#f59e0b";

  return (
    <div
      className="card"
      style={{
        padding: 20,
        borderRadius: 12,
        background: "#fff",
        boxShadow: "0 4px 12px rgba(0,0,0,.08)",
      }}
    >
      <h3>Health Score</h3>

      <div
        style={{
          fontSize: 52,
          fontWeight: "bold",
          color,
          marginTop: 15,
        }}
      >
        {score}
      </div>

      <h2>{health.grade}</h2>

      <div
        style={{
          height: 12,
          width: "100%",
          background: "#eee",
          borderRadius: 20,
          overflow: "hidden",
          marginTop: 20,
        }}
      >
        <div
          style={{
            width: `${score}%`,
            height: "100%",
            background: color,
          }}
        />
      </div>
    </div>
  );
}

export default HealthScore;