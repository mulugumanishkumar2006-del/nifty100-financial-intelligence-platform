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

// ================= CHART SERVICES & COMPONENTS =================

import {
  getRevenueTrend,
  getMarketCap,
  getStockHistory,
} from "../services/chartService";

import PriceChart from "../charts/PriceChart";
import PriceLineChart from "../charts/PriceLineChart";
import VolumeBarChart from "../charts/VolumeBarChart";

import { getCompanies } from "../services/companyService";

// ================= UI FEEDBACK COMPONENTS =================

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";

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
  
  // Error State
  const [error, setError] = useState(null);

  // Stats state
  const [companies, setCompanies] = useState([]);
  const [sectorSummary, setSectorSummary] = useState([]);
  const [financialRatios, setFinancialRatios] = useState([]);

  // Dynamic Chart States
  const [selectedCompany, setSelectedCompany] = useState("");
  const [revenueTrend, setRevenueTrend] = useState([]);
  const [marketCapData, setMarketCapData] = useState([]);
  const [stockHistory, setStockHistory] = useState([]);

  // Step 10.1 – Optimized loadDashboard() using Promise.all()
  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        // Backend health check
        const response = await fetch("http://127.0.0.1:8000/");
        if (!response.ok) {
          throw new Error("Unable to connect to backend service.");
        }

        const apiData = await response.json();
        setApi(apiData);

        // Fetch all independent APIs in parallel for optimal load times
        const [
          dashboardData,
          yearData,
          revenueData,
          profitData,
          sector,
          revenueRank,
          profitRank,
        ] = await Promise.all([
          getDashboard(),
          getLatestYear(),
          getTopRevenue(),
          getTopProfit(),
          getSectorDistribution(),
          getRevenueRanking(),
          getProfitRanking(),
        ]);

        setDashboard(dashboardData);
        setLatestYear(yearData);
        setTopRevenue(revenueData?.[0] || null);
        setTopProfit(profitData?.[0] || null);
        setSectorData(sector || []);
        setRevenueRanking(revenueRank || []);
        setProfitRanking(profitRank || []);

        // Load Company List
        const companyList = await getCompanies();
        setCompanies(companyList || []);
        if (companyList && companyList.length > 0) {
          setSelectedCompany(companyList[0].id);
        }

        // Safe fallbacks using loaded dashboard data
        setSectorSummary(sector || []);
        setFinancialRatios([]);
      } catch (err) {
        console.error("Dashboard Loading Error:", err);
        setError(err.message || "Failed to load dashboard data. Please try again.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  // loadCharts Function
  async function loadCharts(companyId) {
    try {
      const revenue = await getRevenueTrend(companyId);
      const market = await getMarketCap();
      const stock = await getStockHistory(companyId);

      setRevenueTrend(revenue || []);
      setMarketCapData(market || []);
      setStockHistory(stock || []);
    } catch (err) {
      console.error("Chart Loading Error:", err);
    }
  }

  // Load charts dynamically on selectedCompany change
  useEffect(() => {
    if (selectedCompany) {
      loadCharts(selectedCompany);
    }
  }, [selectedCompany]);

  // Auto Refresh (5 Minutes)
  useEffect(() => {
    const interval = setInterval(() => {
      window.location.reload();
    }, 300000); // 5 minutes

    return () => clearInterval(interval);
  }, []);

  // Calculate stats
  const averageROE = dashboard?.average_roe ?? 0;
  const totalMarketCap = "₹ --";

  // Handle Loading State
  if (loading) {
    return (
      <Layout>
        <Header />
        <LoadingSpinner />
      </Layout>
    );
  }

  // Handle Error State
  if (error) {
    return (
      <Layout>
        <Header />
        <ErrorMessage
          message={error}
          onRetry={() => window.location.reload()}
        />
      </Layout>
    );
  }

  return (
    <Layout>
      <Header />

      {/* Dashboard Container */}
      <div
        style={{
          padding: "25px",
          background: "#f8fafc",
          minHeight: "100vh",
        }}
      >
        {/* ================= DASHBOARD STATS ================= */}

        <DashboardStats
          companies={dashboard?.companies ?? companies.length}
          sectors={sectorData.length}
          avgROE={averageROE}
          totalMarketCap={totalMarketCap}
        />

        {/* ================= QUICK NAVIGATION & COMPANY SELECTOR ================= */}

        <div style={{ marginTop: "30px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "20px",
            }}
          >
            <h2>Quick Navigation</h2>

            {/* Company Selector Dropdown */}
            {companies.length > 0 && (
              <div>
                <label
                  htmlFor="company-select"
                  style={{ marginRight: "10px", fontWeight: "bold" }}
                >
                  Select Company:
                </label>
                <select
                  id="company-select"
                  value={selectedCompany}
                  onChange={(e) => setSelectedCompany(e.target.value)}
                  style={{
                    padding: "8px 12px",
                    borderRadius: "6px",
                    border: "1px solid #ccc",
                    fontSize: "14px",
                  }}
                >
                  {companies.map((company) => (
                    <option key={company.id} value={company.id}>
                      {company.name || company.company_name || company.id}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <QuickLinks />
        </div>

        {/* ================= KPI CARDS ================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
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
            value={dashboard ? `${dashboard.average_roe}%` : "0%"}
            subtitle="Return on Equity"
            icon={<FaChartBar />}
            color="#16a34a"
          />

          <StatCard
            title="Average ROCE"
            value={dashboard ? `${dashboard.average_roce}%` : "0%"}
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
            gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))",
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
            gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "40px",
          }}
        >
          {!dashboard ? (
            <EmptyState title="Dashboard Chart Data Not Available" />
          ) : (
            <DashboardChart dashboard={dashboard} />
          )}

          {sectorData.length === 0 ? (
            <EmptyState title="Sector Analytics Not Available" />
          ) : (
            <SectorPieChart sectorData={sectorData} />
          )}
        </div>

        {/* ================= RANKINGS ================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "40px",
          }}
        >
          {revenueRanking.length === 0 ? (
            <EmptyState title="Revenue Rankings Not Available" />
          ) : (
            <RevenueRanking data={revenueRanking} />
          )}

          {profitRanking.length === 0 ? (
            <EmptyState title="Profit Rankings Not Available" />
          ) : (
            <ProfitRanking data={profitRanking} />
          )}
        </div>

        {/* ================= SECTOR ANALYTICS ================= */}

        {sectorData.length === 0 ? (
          <EmptyState title="Sector Overview Not Available" />
        ) : (
          <SectorAnalytics data={sectorData} />
        )}

        {/* ================= ANALYTICS SUMMARY ================= */}

        <AnalyticsOverview dashboard={dashboard} />

        {/* ================= DYNAMIC CHART SECTION ================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "40px",
          }}
        >
          {revenueTrend.length === 0 ? (
            <EmptyState title="Revenue Trend Data Not Available" />
          ) : (
            <PriceLineChart data={revenueTrend} />
          )}

          {marketCapData.length === 0 ? (
            <EmptyState title="Market Cap Data Not Available" />
          ) : (
            <VolumeBarChart data={marketCapData} />
          )}

          {stockHistory.length === 0 ? (
            <EmptyState title="Stock History Not Available" />
          ) : (
            <PriceChart data={stockHistory} />
          )}
        </div>
      </div>
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