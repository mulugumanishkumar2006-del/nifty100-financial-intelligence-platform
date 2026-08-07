import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Layout from "../components/Layout";

import CompanyHeader from "../components/company/CompanyHeader";
import CompanySummary from "../components/company/CompanySummary";

import HealthScore from "../components/company/HealthScore";
import GrowthAnalysis from "../components/company/GrowthAnalysis";
import RiskAnalysis from "../components/company/RiskAnalysis";
import PerformanceScore from "../components/company/PerformanceScore";

import ProfitLossTable from "../components/company/ProfitLossTable";
import BalanceSheetTable from "../components/company/BalanceSheetTable";
import CashFlowTable from "../components/company/CashFlowTable";
import FinancialRatios from "../components/company/FinancialRatios";

import RevenueChart from "../components/company/RevenueChart";
import ProfitChart from "../components/company/ProfitChart";

import PeerComparison from "../components/company/PeerComparison";
import CompanyComparison from "../components/company/CompanyComparison";
import AIInsights from "../components/company/AIInsights";

import {
  getCompany,
  getAIInsights,
  getGrowthAnalysis,
  getRiskAnalysis,
  getAIRecommendation,
} from "../services/companyService";

function CompanyDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [company, setCompany] = useState(null);

  const [aiInsights, setAIInsights] = useState(null);
  const [growthAnalysis, setGrowthAnalysis] = useState(null);
  const [riskAnalysis, setRiskAnalysis] = useState(null);
  const [recommendation, setRecommendation] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ==========================================================
  // Fetch Company Data
  // ==========================================================

  useEffect(() => {
    let mounted = true;

    async function fetchCompanyData() {
      try {
        setLoading(true);
        setError("");

        const [
          companyData,
          aiData,
          growthData,
          riskData,
          recommendationData,
        ] = await Promise.all([
          getCompany(id),
          getAIInsights(id),
          getGrowthAnalysis(id),
          getRiskAnalysis(id),
          getAIRecommendation(id),
        ]);

        if (!mounted) return;

        setCompany(companyData);
        setAIInsights(aiData);
        setGrowthAnalysis(growthData);
        setRiskAnalysis(riskData);
        setRecommendation(recommendationData);

        console.log("Company:", companyData);
        console.log("AI Insights:", aiData);
        console.log("Growth:", growthData);
        console.log("Risk:", riskData);
        console.log("Recommendation:", recommendationData);
      } catch (err) {
        console.error("Company Details Error:", err);

        if (mounted) {
          setError(
            err?.response?.data?.detail ||
              err?.message ||
              "Unable to load company details."
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    fetchCompanyData();

    return () => {
      mounted = false;
    };
  }, [id]);

  // ==========================================================
  // Loading State
  // ==========================================================

  if (loading) {
    return (
      <Layout>
        <div
          style={{
            minHeight: "60vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            gap: "12px",
          }}
        >
          <div
            style={{
              fontSize: "40px",
            }}
          >
            📊
          </div>

          <h2
            style={{
              margin: 0,
              color: "#334155",
            }}
          >
            Loading Company...
          </h2>

          <p
            style={{
              color: "#64748b",
            }}
          >
            Loading financial intelligence and AI analysis.
          </p>
        </div>
      </Layout>
    );
  }

  // ==========================================================
  // Error State
  // ==========================================================

  if (error) {
    return (
      <Layout>
        <div
          style={{
            maxWidth: "700px",
            margin: "80px auto",
            padding: "30px",
            background: "#ffffff",
            borderRadius: "15px",
            textAlign: "center",
            boxShadow: "0 10px 25px rgba(0,0,0,.08)",
          }}
        >
          <div
            style={{
              fontSize: "45px",
              marginBottom: "15px",
            }}
          >
            ⚠️
          </div>

          <h2
            style={{
              color: "#dc2626",
            }}
          >
            Unable to Load Company
          </h2>

          <p
            style={{
              color: "#64748b",
              lineHeight: "1.6",
            }}
          >
            {error}
          </p>

          <button
            onClick={() => window.location.reload()}
            style={{
              marginTop: "15px",
              padding: "12px 22px",
              border: "none",
              borderRadius: "10px",
              background: "#2563eb",
              color: "#ffffff",
              fontWeight: "600",
              cursor: "pointer",
            }}
          >
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  // ==========================================================
  // Company Not Found
  // ==========================================================

  if (!company) {
    return (
      <Layout>
        <div
          style={{
            textAlign: "center",
            padding: "80px 20px",
          }}
        >
          <div
            style={{
              fontSize: "50px",
            }}
          >
            🔍
          </div>

          <h2>Company Not Found</h2>

          <p
            style={{
              color: "#64748b",
            }}
          >
            The requested company could not be found.
          </p>
        </div>
      </Layout>
    );
  }

  // ==========================================================
  // Normalize Company Object
  // ==========================================================

  const companyData = company.company || company;

  // ==========================================================
  // Ask AI About Company
  // ==========================================================

  function handleAskAI() {
    if (!companyData?.id) {
      return;
    }

    navigate(
      `/ai-chat?company=${encodeURIComponent(
        companyData.id
      )}&name=${encodeURIComponent(
        companyData.company_name || "Company"
      )}`
    );
  }

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <Layout>
      {/* ======================================================
          Company Header + AI Action
      ====================================================== */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: "20px",
          flexWrap: "wrap",
          marginBottom: "25px",
        }}
      >
        <div
          style={{
            flex: 1,
            minWidth: "280px",
          }}
        >
          <CompanyHeader company={companyData} />
        </div>

        <button
          onClick={handleAskAI}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",

            padding: "13px 20px",

            border: "none",
            borderRadius: "10px",

            background:
              "linear-gradient(135deg,#2563eb,#1d4ed8)",

            color: "#ffffff",

            fontSize: "15px",
            fontWeight: "600",

            cursor: "pointer",

            boxShadow:
              "0 8px 20px rgba(37,99,235,.25)",

            transition: "all .2s ease",

            whiteSpace: "nowrap",
          }}
          onMouseEnter={(event) => {
            event.currentTarget.style.transform =
              "translateY(-2px)";
            event.currentTarget.style.boxShadow =
              "0 12px 25px rgba(37,99,235,.35)";
          }}
          onMouseLeave={(event) => {
            event.currentTarget.style.transform =
              "translateY(0)";
            event.currentTarget.style.boxShadow =
              "0 8px 20px rgba(37,99,235,.25)";
          }}
        >
          🤖 Ask AI About This Company
        </button>
      </div>

      {/* ======================================================
          Company Summary
      ====================================================== */}

      <CompanySummary
        company={companyData}
      />

      {/* ======================================================
          AI Score Cards
      ====================================================== */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(320px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <HealthScore
          company={companyData}
        />

        <PerformanceScore
          company={companyData}
          recommendation={recommendation}
        />
      </div>

      {/* ======================================================
          AI Insights
      ====================================================== */}

      <AIInsights
        company={companyData}
        insights={aiInsights}
      />

      {/* ======================================================
          Growth Analysis
      ====================================================== */}

      <GrowthAnalysis
        company={company}
        analysis={growthAnalysis}
      />

      {/* ======================================================
          Risk Analysis
      ====================================================== */}

      <RiskAnalysis
        company={company}
        analysis={riskAnalysis}
      />

      {/* ======================================================
          Financial Charts
      ====================================================== */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(500px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <RevenueChart
          company={company}
        />

        <ProfitChart
          company={company}
        />
      </div>

      {/* ======================================================
          Financial Statements
      ====================================================== */}

      <ProfitLossTable
        data={company.profit_loss || []}
      />

      <BalanceSheetTable
        data={company.balance_sheet || []}
      />

      <CashFlowTable
        data={company.cash_flow || []}
      />

      {/* ======================================================
          Financial Ratios
      ====================================================== */}

      <FinancialRatios
        company={companyData}
        ratios={company.financial_ratios || []}
      />

      {/* ======================================================
          Company Snapshot
      ====================================================== */}

      <CompanyComparison
        company={companyData}
      />

      {/* ======================================================
          Peer Comparison
      ====================================================== */}

      <PeerComparison
        company={companyData}
      />
    </Layout>
  );
}

export default CompanyDetails;