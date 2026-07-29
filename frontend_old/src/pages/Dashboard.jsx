import { useEffect, useState } from "react";

import Layout from "../components/Layout";
import Header from "../components/Header";

import StatCard from "../components/StatCard";

import DashboardChart from "../components/DashboardChart";
import SectorPieChart from "../components/SectorPieChart";


// ================= DAY 13 COMPONENTS =================

import MarketOverview from "../dashboard/MarketOverview";
import InvestmentInsights from "../dashboard/InvestmentInsights";


// ================= ANALYTICS COMPONENTS =================

import RevenueRanking from "../components/analytics/RevenueRanking";
import ProfitRanking from "../components/analytics/ProfitRanking";
import SectorAnalytics from "../components/analytics/SectorAnalytics";
import AnalyticsOverview from "../components/analytics/AnalyticsOverview";


// ================= QUICK LINKS & STATS =================

import QuickLinks from "../dashboard/QuickLinks";
import DashboardStats from "../components/dashboard/DashboardStats";


// ================= ICONS =================

import {
  FaBuilding,
  FaChartBar,
  FaIndustry,
  FaDatabase,
} from "react-icons/fa";


// ================= SERVICES =================

import {
  getDashboard,
  getLatestYear,
  getTopRevenue,
  getTopProfit,
  getSectorDistribution,
} from "../services/api";

import {
  getRevenueRanking,
  getProfitRanking,
} from "../services/analyticsService";


function Dashboard() {

  const [api, setApi] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [latestYear, setLatestYear] = useState(null);
  const [topRevenue, setTopRevenue] = useState(null);
  const [topProfit, setTopProfit] = useState(null);
  const [sectorData, setSectorData] = useState([]);
  const [revenueRanking, setRevenueRanking] = useState([]);
  const [profitRanking, setProfitRanking] = useState([]);
  const [loading, setLoading] = useState(true);

  // Stats state
  const [companies, setCompanies] = useState([]);
  const [sectorSummary, setSectorSummary] = useState([]);
  const [financialRatios, setFinancialRatios] = useState([]);

  useEffect(() => {

    async function loadDashboard() {

      try {

        // Backend health check
        const response = await fetch(
          "http://127.0.0.1:8000/"
        );

        const apiData = await response.json();
        setApi(apiData);

        // Dashboard APIs
        const [
          dashboardData,
          yearData,
          revenueData,
          profitData,
          sector,
          revenueRank,
          profitRank
        ] = await Promise.all([
          getDashboard(),
          getLatestYear(),
          getTopRevenue(),
          getTopProfit(),
          getSectorDistribution(),
          getRevenueRanking(),
          getProfitRanking()
        ]);

        setDashboard(dashboardData);
        setLatestYear(yearData);
        setTopRevenue(revenueData?.[0] || null);
        setTopProfit(profitData?.[0] || null);
        setSectorData(sector || []);
        setRevenueRanking(revenueRank || []);
        setProfitRanking(profitRank || []);

        // Safe fallbacks using loaded dashboard data
        setCompanies(new Array(dashboardData?.companies || 0).fill({}));
        setSectorSummary(sector || []);
        setFinancialRatios([]);

      } catch (error) {

        console.error(
          "Dashboard Loading Error:",
          error
        );

      } finally {

        setLoading(false);

      }

    }

    loadDashboard();

  }, []);

  // Calculate stats
  const averageROE = dashboard?.average_roe ?? 0;
  const totalMarketCap = "₹ --";

  if (loading) {

    return (

      <Layout>

        <Header />

        <h2
          style={{
            textAlign: "center",
            marginTop: "60px",
          }}
        >
          Loading Dashboard...
        </h2>

      </Layout>

    );

  }

  return (

    <Layout>

      <Header />

      {/* ================= DASHBOARD STATS ================= */}

      <DashboardStats
        companies={dashboard?.companies ?? companies.length}
        sectors={sectorData.length}
        avgROE={averageROE}
        totalMarketCap={totalMarketCap}
      />

      {/* ================= QUICK NAVIGATION ================= */}

      <div style={{ marginTop: "30px" }}>
        <h2
          style={{
            marginBottom: "20px",
          }}
        >
          Quick Navigation
        </h2>
        <QuickLinks />
      </div>

      {/* ================= KPI CARDS ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(260px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >

        <StatCard
          title="Companies"
          value={dashboard?.companies ?? 0}
          subtitle="Listed Companies"
          icon={<FaBuilding />}
          color="#2563eb"
        />

        <StatCard
          title="Average ROE"
          value={
            dashboard ? `${dashboard.average_roe}%` : "0%"
          }
          subtitle="Return on Equity"
          icon={<FaChartBar />}
          color="#16a34a"
        />

        <StatCard
          title="Average ROCE"
          value={
            dashboard ? `${dashboard.average_roce}%` : "0%"
          }
          subtitle="Capital Efficiency"
          icon={<FaDatabase />}
          color="#dc2626"
        />

        <StatCard
          title="Sectors"
          value={dashboard?.total_sectors ?? 0}
          subtitle="Market Sectors"
          icon={<FaIndustry />}
          color="#9333ea"
        />

      </div>

      {/* ================= DAY 13 FEATURES ================= */}

      <MarketOverview dashboard={dashboard} />

      <InvestmentInsights dashboard={dashboard} />

      {/* ================= SUMMARY CARDS ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(300px,1fr))",
          gap: "20px",
          marginTop: "35px",
        }}
      >

        <InfoCard
          title="Backend Status"
          value={api?.status || "Offline"}
        />

        <InfoCard
          title="Latest Financial Year"
          value={
            latestYear?.latest_year ??
            dashboard?.latest_year ??
            "-"
          }
        />

        <InfoCard
          title="Total Revenue"
          value={
            dashboard
              ? `₹ ${Number(
                  dashboard.total_revenue
                ).toLocaleString("en-IN")}`
              : "-"
          }
        />

        <InfoCard
          title="Total Profit"
          value={
            dashboard
              ? `₹ ${Number(
                  dashboard.total_profit
                ).toLocaleString("en-IN")}`
              : "-"
          }
        />

        <InfoCard
          title="Top Revenue Company"
          value={topRevenue?.company_name || "-"}
        />

        <InfoCard
          title="Top Profit Company"
          value={topProfit?.company_name || "-"}
        />

        <InfoCard
          title="Sector Distribution"
          value={`${sectorData.length} Sectors`}
        />

      </div>

      {/* ================= CHARTS ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(500px,1fr))",
          gap: "25px",
          marginTop: "40px",
        }}
      >

        <DashboardChart dashboard={dashboard} />

        <SectorPieChart sectorData={sectorData} />

      </div>

      {/* ================= RANKINGS ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(500px,1fr))",
          gap: "25px",
          marginTop: "40px",
        }}
      >

        <RevenueRanking data={revenueRanking} />

        <ProfitRanking data={profitRanking} />

      </div>

      {/* ================= SECTOR ANALYTICS ================= */}

      <SectorAnalytics data={sectorData} />

      {/* ================= ANALYTICS SUMMARY ================= */}

      <AnalyticsOverview dashboard={dashboard} />

    </Layout>

  );

}

function InfoCard({ title, value }) {

  return (

    <div className="card">

      <h2>{title}</h2>

      <h3>{value}</h3>

    </div>

  );

}

export default Dashboard;