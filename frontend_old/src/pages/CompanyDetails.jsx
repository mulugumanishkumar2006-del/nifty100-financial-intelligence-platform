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
import AIInsights from "../components/company/AIInsights";
import { getCompany } from "../services/companyService";
import CompanyComparison from "../components/company/CompanyComparison";
function CompanyDetails() {
  const { id } = useParams();

  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCompany() {
      try {
        const response = await getCompany(id);

        console.log("Company Response:", response);

        setCompany(response);
      } catch (error) {
        console.error("Company Error:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchCompany();
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

      {/* ================= Header ================= */}

      <CompanyHeader company={company.company} />

      {/* ================= Summary ================= */}

      <CompanySummary company={company.company} />

      {/* ================= AI Analysis ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <HealthScore company={company.company} />

        <PerformanceScore company={company.company} />
      </div>

      <GrowthAnalysis company={company} />

      <RiskAnalysis company={company} />

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
      />
      <AIInsights company={company.company} />
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