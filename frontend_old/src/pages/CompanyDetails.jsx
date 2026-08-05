import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

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

  const [company, setCompany] = useState(null);

  const [aiInsights, setAIInsights] = useState(null);
  const [growthAnalysis, setGrowthAnalysis] = useState(null);
  const [riskAnalysis, setRiskAnalysis] = useState(null);
  const [recommendation, setRecommendation] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCompanyData() {
      try {
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

        setCompany(companyData);
        setAIInsights(aiData);
        setGrowthAnalysis(growthData);
        setRiskAnalysis(riskData);
        setRecommendation(recommendationData);

        console.log(companyData);
        console.log(aiData);
        console.log(growthData);
        console.log(riskData);
        console.log(recommendationData);

      } catch (error) {
        console.error("Company Details Error:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchCompanyData();
  }, [id]);

  if (loading) {
    return (
      <Layout>
        <h2>Loading Company...</h2>
      </Layout>
    );
  }

  if (!company) {
    return (
      <Layout>
        <h2>Company Not Found</h2>
      </Layout>
    );
  }

  return (
    <Layout>

      {/* ================= Company Header ================= */}

      <CompanyHeader company={company.company} />

      {/* ================= Company Summary ================= */}

      <CompanySummary company={company.company} />

      {/* ================= AI Score Cards ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <HealthScore company={company.company} />

        <PerformanceScore
          company={company.company}
          recommendation={recommendation}
        />
      </div>

      {/* ================= AI Insights ================= */}

      <AIInsights
        company={company.company}
        insights={aiInsights}
      />

      {/* ================= Growth Analysis ================= */}

      <GrowthAnalysis
        company={company}
        analysis={growthAnalysis}
      />

      {/* ================= Risk Analysis ================= */}

      <RiskAnalysis
        company={company}
        analysis={riskAnalysis}
      />

      {/* ================= Charts ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <RevenueChart company={company} />

        <ProfitChart company={company} />
      </div>

      {/* ================= Financial Statements ================= */}

      <ProfitLossTable
        data={company.profit_loss || []}
      />

      <BalanceSheetTable
        data={company.balance_sheet || []}
      />

      <CashFlowTable
        data={company.cash_flow || []}
      />

      {/* ================= Financial Ratios ================= */}

      <FinancialRatios
        company={company.company}
        ratios={company.financial_ratios}
      />

      {/* ================= Company Snapshot ================= */}

      <CompanyComparison
        company={company.company}
      />

      {/* ================= Peer Comparison ================= */}

      <PeerComparison
        company={company.company}
      />

    </Layout>
  );
}

export default CompanyDetails;