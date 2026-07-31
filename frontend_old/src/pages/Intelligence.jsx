import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import AIInsightsCard from "../components/AIInsightsCard";

import {
  getCompanies,
  getAIAnalysis,
} from "../services/intelligenceService";

function Intelligence() {

  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");

  const [health, setHealth] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [summary, setSummary] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadCompanies();
  }, []);

  useEffect(() => {
    if (companyId) {
      loadAI();
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

      setError("Unable to load companies.");

    }

  }

  async function loadAI() {

    try {

      setLoading(true);

      setError("");

      const ai = await getAIAnalysis(companyId);

      setHealth(ai.health);

      setRecommendation(ai.recommendation);

      setSummary(ai.summary);

    } catch (err) {

      console.error(err);

      setError("Unable to load AI Intelligence.");

    } finally {

      setLoading(false);

    }

  }

  return (

    <Layout>

      <div
        style={{
          marginBottom: 35,
        }}
      >

        <h1>🤖 AI Intelligence Dashboard</h1>

        <p
          style={{
            color: "#64748b",
          }}
        >
          AI Powered Financial Analysis Platform
        </p>

      </div>

      <div
        style={{
          marginBottom: 30,
        }}
      >

        <label
          style={{
            marginRight: 15,
            fontWeight: "600",
          }}
        >
          Select Company
        </label>

        <select
          value={companyId}
          onChange={(e) =>
            setCompanyId(e.target.value)
          }
          style={{
            padding: 12,
            borderRadius: 10,
            minWidth: 280,
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

      </div>

      {loading && <h2>Loading AI Analysis...</h2>}

      {error &&

        <h2
          style={{
            color: "red",
          }}
        >
          {error}
        </h2>

      }

      {!loading && !error && (

        <>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(250px,1fr))",
              gap: 20,
            }}
          >

            <AIInsightsCard
              title="Health Score"
              value={
                health?.health_score ??
                "-"
              }
              color="#16a34a"
            />

            <AIInsightsCard
              title="Recommendation"
              value={
                recommendation?.recommendation ??
                "-"
              }
              color="#2563eb"
            />

            <AIInsightsCard
              title="Risk Level"
              value={
                summary?.risk ??
                "-"
              }
              color="#dc2626"
            />

          </div>

          <div
            style={{
              marginTop: 25,
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(250px,1fr))",
              gap: 20,
            }}
          >

            <AIInsightsCard
              title="Investment Grade"
              value={
                health?.grade ??
                "-"
              }
              color="#7c3aed"
            />

            <AIInsightsCard
              title="Selected Company"
              value={
                companyId
              }
              color="#f59e0b"
            />

            <AIInsightsCard
              title="AI Confidence"
              value="95%"
              color="#0ea5e9"
            />

          </div>

          <div
            style={{
              marginTop: 35,
              background: "#ffffff",
              padding: 25,
              borderRadius: 15,
              boxShadow:
                "0 8px 20px rgba(0,0,0,0.08)",
            }}
          >

            <h2>📈 AI Financial Summary</h2>

            <p
              style={{
                marginTop: 20,
                lineHeight: 1.8,
                color: "#374151",
              }}
            >

              {summary?.summary ??
                "No summary available."}

            </p>

          </div>

        </>

      )}

    </Layout>

  );

}

export default Intelligence;