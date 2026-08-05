import { useEffect, useState } from "react";
import {
  getRecommendation,
  getHealthScore,
  getAISummary,
} from "../../services/companyService";

function PerformanceScore({ company }) {
  const [recommendation, setRecommendation] = useState(null);
  const [health, setHealth] = useState(null);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    async function loadData() {
      if (!company?.id) return;

      try {
        const [rec, score, ai] = await Promise.all([
          getRecommendation(company.id),
          getHealthScore(company.id),
          getAISummary(company.id),
        ]);

        setRecommendation(rec);
        setHealth(score);
        setSummary(ai);
      } catch (err) {
        console.error(err);
      }
    }

    loadData();
  }, [company]);

  if (!recommendation || !health || !summary) {
    return (
      <div
        style={{
          background: "#fff",
          padding: "25px",
          borderRadius: "15px",
          boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        }}
      >
        <h2>Performance Score</h2>
        <p>Loading...</p>
      </div>
    );
  }

  const score = health.health_score || 0;

  let recommendationColor = "#2563eb";

  if (recommendation.recommendation === "BUY")
    recommendationColor = "#16a34a";

  if (recommendation.recommendation === "SELL")
    recommendationColor = "#dc2626";

  let scoreColor = "#16a34a";

  if (score < 80) scoreColor = "#f59e0b";
  if (score < 60) scoreColor = "#dc2626";

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: "20px",
        }}
      >
        ⭐ Performance Score
      </h2>

      {/* Health Score */}

      <div style={{ marginBottom: "25px" }}>
        <h3>Health Score</h3>

        <div
          style={{
            width: "100%",
            height: "12px",
            background: "#e5e7eb",
            borderRadius: "10px",
            overflow: "hidden",
            marginTop: "10px",
          }}
        >
          <div
            style={{
              width: `${score}%`,
              height: "100%",
              background: scoreColor,
            }}
          />
        </div>

        <h2
          style={{
            color: scoreColor,
            marginTop: "10px",
          }}
        >
          {score}/100
        </h2>
      </div>

      {/* Recommendation */}

      <div
        style={{
          marginBottom: "20px",
        }}
      >
        <h3>Recommendation</h3>

        <h1
          style={{
            color: recommendationColor,
            margin: 0,
          }}
        >
          {recommendation.recommendation}
        </h1>
      </div>

      {/* Grade */}

      <div
        style={{
          marginBottom: "20px",
        }}
      >
        <h3>Grade</h3>

        <h2
          style={{
            color: "#2563eb",
          }}
        >
          {health.grade}
        </h2>
      </div>

      {/* Risk */}

      <div
        style={{
          marginBottom: "20px",
        }}
      >
        <h3>Risk Level</h3>

        <h2
          style={{
            color:
              summary.risk === "Low"
                ? "#16a34a"
                : summary.risk === "Medium"
                ? "#f59e0b"
                : "#dc2626",
          }}
        >
          {summary.risk}
        </h2>
      </div>

      {/* AI Summary */}

      <div
        style={{
          marginTop: "25px",
          background: "#f8fafc",
          padding: "18px",
          borderRadius: "10px",
        }}
      >
        <h3
          style={{
            marginBottom: "10px",
          }}
        >
          🤖 AI Summary
        </h3>

        <p
          style={{
            lineHeight: "1.7",
            color: "#475569",
          }}
        >
          {summary.summary}
        </p>
      </div>
    </div>
  );
}

export default PerformanceScore;