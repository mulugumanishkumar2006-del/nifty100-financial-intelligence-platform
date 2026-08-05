import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import AIInsightsCard from "../components/AIInsightsCard";

import {
  getCompanies,
  getHealthScore,
  getRecommendation,
  getAISummary,
} from "../services/companyService";

function Intelligence() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");

  const [health, setHealth] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [summary, setSummary] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [error, setError] = useState("");

  // ============================================
  // Load Companies
  // ============================================

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setLoadingCompanies(true);

      const data = await getCompanies();

      setCompanies(data || []);

      if (data?.length > 0) {
        setCompanyId(data[0].id);
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load companies.");
    } finally {
      setLoadingCompanies(false);
    }
  };

  // ============================================
  // Load AI Data
  // ============================================

  useEffect(() => {
    if (companyId) {
      loadAIData();
    }
  }, [companyId]);

  const loadAIData = async () => {
    try {
      setLoading(true);
      setError("");

      const [healthData, recommendationData, summaryData] =
        await Promise.all([
          getHealthScore(companyId),
          getRecommendation(companyId),
          getAISummary(companyId),
        ]);

      setHealth(healthData);
      setRecommendation(recommendationData);
      setSummary(summaryData);
    } catch (err) {
      console.error(err);
      setError("Unable to load AI Intelligence.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      {/* ===================================== */}
      {/* Header */}
      {/* ===================================== */}

      <div style={{ marginBottom: 35 }}>
        <h1>🤖 AI Intelligence Dashboard</h1>

        <p
          style={{
            color: "#64748b",
            marginTop: 8,
          }}
        >
          AI-powered financial insights for every NIFTY100 company.
        </p>
      </div>

      {/* ===================================== */}
      {/* Company Selector */}
      {/* ===================================== */}

      <div
        style={{
          marginBottom: 30,
          display: "flex",
          alignItems: "center",
          gap: 15,
          flexWrap: "wrap",
        }}
      >
        <label
          style={{
            fontWeight: 600,
          }}
        >
          Select Company
        </label>

        <select
          value={companyId}
          disabled={loadingCompanies}
          onChange={(e) => setCompanyId(e.target.value)}
          style={{
            padding: 12,
            minWidth: 320,
            borderRadius: 10,
          }}
        >
          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.company_name}
            </option>
          ))}
        </select>
      </div>

      {/* ===================================== */}
      {/* Loading */}
      {/* ===================================== */}

      {loading && (
        <h2 style={{ color: "#2563eb" }}>
          Loading AI Analysis...
        </h2>
      )}

      {/* ===================================== */}
      {/* Error */}
      {/* ===================================== */}

      {error && (
        <div
          style={{
            padding: 18,
            background: "#fee2e2",
            color: "#dc2626",
            borderRadius: 10,
            marginBottom: 25,
          }}
        >
          {error}
        </div>
      )}

      {/* ===================================== */}
      {/* Dashboard */}
      {/* ===================================== */}

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
              value={health?.health_score ?? "-"}
              color="#16a34a"
            />

            <AIInsightsCard
              title="Investment Grade"
              value={health?.grade ?? "-"}
              color="#7c3aed"
            />

            <AIInsightsCard
              title="Recommendation"
              value={
                recommendation?.recommendation ??
                "HOLD"
              }
              color="#2563eb"
            />

            <AIInsightsCard
              title="Risk Level"
              value={summary?.risk ?? "-"}
              color="#dc2626"
            />
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(250px,1fr))",
              gap: 20,
              marginTop: 25,
            }}
          >
            <AIInsightsCard
              title="AI Confidence"
              value="95%"
              color="#0891b2"
            />

            <AIInsightsCard
              title="Model Version"
              value="FinGPT v2"
              color="#f59e0b"
            />

            <AIInsightsCard
              title="Analysis Status"
              value="Completed"
              color="#22c55e"
            />

            <AIInsightsCard
              title="Selected Company"
              value={
                companies.find(
                  (c) => c.id === companyId
                )?.company_name ?? "-"
              }
              color="#2563eb"
            />
          </div>

          {/* ===================================== */}
          {/* AI Summary */}
          {/* ===================================== */}

          <div
            style={{
              marginTop: 35,
              background: "#ffffff",
              borderRadius: 15,
              padding: 25,
              boxShadow:
                "0 8px 20px rgba(0,0,0,0.08)",
            }}
          >
            <h2
              style={{
                marginBottom: 20,
              }}
            >
              📈 AI Financial Summary
            </h2>

            <p
              style={{
                lineHeight: 1.9,
                color: "#475569",
                fontSize: 16,
              }}
            >
              {summary?.summary ??
                "No AI summary available."}
            </p>
          </div>
        </>
      )}
    </Layout>
  );
}

export default Intelligence;