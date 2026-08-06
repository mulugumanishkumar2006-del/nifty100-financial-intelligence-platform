import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import AIInsightsCard from "../components/AIInsightsCard";

import {
  getCompanyAIInsights,
  getGrowthAnalysis,
  getRiskAnalysis,
  getInvestmentRecommendation,
} from "../services/aiInsightService";

import { getCompanies } from "../services/companyService";

function AIInsights() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");

  const [insights, setInsights] = useState({});
  const [growth, setGrowth] = useState({});
  const [risk, setRisk] = useState({});
  const [recommendation, setRecommendation] = useState({});

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCompanies();
  }, []);

  useEffect(() => {
    if (companyId) {
      loadAIData();
    }
  }, [companyId]);

  async function loadCompanies() {
    try {
      const data = await getCompanies();

      setCompanies(data);

      if (data.length > 0) {
        setCompanyId(data[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function loadAIData() {
    try {
      setLoading(true);

      const company = await getCompanyAIInsights(companyId);
      const growthData = await getGrowthAnalysis(companyId);
      const riskData = await getRiskAnalysis(companyId);
      const recommendationData =
        await getInvestmentRecommendation(companyId);

      setInsights(company);
      setGrowth(growthData);
      setRisk(riskData);
      setRecommendation(recommendationData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <div
        style={{
          padding: "30px",
        }}
      >
        <h1
          style={{
            marginBottom: 5,
          }}
        >
          🤖 AI Financial Intelligence
        </h1>

        <p
          style={{
            color: "#64748b",
            marginBottom: 25,
          }}
        >
          AI Powered Investment Insights & Risk Analytics
        </p>

        <select
          value={companyId}
          onChange={(e) => setCompanyId(e.target.value)}
          style={{
            padding: 12,
            borderRadius: 10,
            width: 320,
            marginBottom: 30,
            border: "1px solid #ddd",
          }}
        >
          {companies.map((company) => (
            <option
              key={company.id}
              value={company.id}
            >
              {company.company_name}
            </option>
          ))}
        </select>

        {loading ? (
          <h2>Loading AI Analysis...</h2>
        ) : (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(300px,1fr))",
                gap: 20,
                marginBottom: 30,
              }}
            >
              <AIInsightsCard
                title="Growth Score"
                value={growth.score || growth.growth_score || "N/A"}
                subtitle={
                  growth.analysis ||
                  growth.growth_analysis ||
                  "-"
                }
                color="#22c55e"
              />

              <AIInsightsCard
                title="Risk Score"
                value={risk.score || risk.risk_score || "N/A"}
                subtitle={
                  risk.analysis ||
                  risk.risk_analysis ||
                  "-"
                }
                color="#ef4444"
              />

              <AIInsightsCard
                title="Recommendation"
                value={
                  recommendation.recommendation ||
                  recommendation.action ||
                  "N/A"
                }
                subtitle={
                  recommendation.reason ||
                  recommendation.summary ||
                  "-"
                }
                color="#3b82f6"
              />
            </div>

            <div
              style={{
                background: "#fff",
                borderRadius: 15,
                padding: 25,
                boxShadow: "0 8px 20px rgba(0,0,0,.08)",
              }}
            >
              <h2>Company AI Summary</h2>

              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                  marginTop: 20,
                }}
              >
                <tbody>
                  {Object.entries(insights).map(([key, value]) => (
                    <tr key={key}>
                      <td
                        style={{
                          padding: 12,
                          borderBottom: "1px solid #eee",
                          fontWeight: 600,
                          width: "30%",
                        }}
                      >
                        {key}
                      </td>

                      <td
                        style={{
                          padding: 12,
                          borderBottom: "1px solid #eee",
                        }}
                      >
                        {typeof value === "object"
                          ? JSON.stringify(value)
                          : value?.toString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}

export default AIInsights;