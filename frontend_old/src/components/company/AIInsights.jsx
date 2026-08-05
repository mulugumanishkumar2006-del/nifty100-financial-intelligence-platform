import { useEffect, useState } from "react";

import {
  getAISummary,
  getRecommendation,
} from "../../services/companyService";

function AIInsights({ company }) {
  const [summary, setSummary] = useState(null);
  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    if (!company?.id) return;

    async function loadAI() {
      const summaryData = await getAISummary(company.id);
      const recommendationData = await getRecommendation(company.id);

      setSummary(summaryData);
      setRecommendation(recommendationData);
    }

    loadAI();
  }, [company]);

  if (!summary || !recommendation) {
    return (
      <div
        style={{
          background: "#fff",
          padding: 25,
          borderRadius: 15,
          marginTop: 30,
          boxShadow: "0 8px 20px rgba(0,0,0,.08)",
        }}
      >
        Loading AI Analysis...
      </div>
    );
  }

  let badgeColor = "#3b82f6";

  if (recommendation.recommendation === "BUY")
    badgeColor = "#16a34a";

  if (recommendation.recommendation === "SELL")
    badgeColor = "#dc2626";

  return (
    <div
      style={{
        background: "#ffffff",
        padding: 25,
        borderRadius: 15,
        marginTop: 30,
        boxShadow: "0 8px 20px rgba(0,0,0,.08)",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: 20,
        }}
      >
        🤖 AI Investment Insights
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(250px,1fr))",
          gap: 20,
        }}
      >
        <Card
          title="Health Score"
          value={summary.health_score}
          color="#2563eb"
        />

        <Card
          title="Risk Level"
          value={summary.risk}
          color="#dc2626"
        />

        <Card
          title="Recommendation"
          value={recommendation.recommendation}
          color={badgeColor}
        />
      </div>

      <div
        style={{
          marginTop: 25,
          background: "#f8fafc",
          padding: 20,
          borderRadius: 12,
        }}
      >
        <h3>AI Summary</h3>

        <p
          style={{
            lineHeight: 1.8,
            color: "#374151",
          }}
        >
          {summary.summary}
        </p>
      </div>
    </div>
  );
}

function Card({ title, value, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        borderLeft: `6px solid ${color}`,
        padding: 20,
        borderRadius: 10,
        boxShadow: "0 4px 10px rgba(0,0,0,.05)",
      }}
    >
      <h4>{title}</h4>

      <h2
        style={{
          color,
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default AIInsights;