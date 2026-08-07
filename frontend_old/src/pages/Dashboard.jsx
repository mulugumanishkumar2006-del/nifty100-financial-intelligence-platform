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

import {
  getRevenueTrend,
  getMarketCap,
  getStockHistory,
} from "../services/chartService";

import { getCompanies } from "../services/companyService";

// ================= CHART COMPONENTS =================

import PriceChart from "../components/charts/PriceChart";
import PriceLineChart from "../components/charts/PriceLineChart";
import VolumeBarChart from "../components/charts/VolumeBarChart";
import MarketSharePieChart from "../components/charts/MarketSharePieChart";

// ================= UI FEEDBACK =================

import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";

// =====================================================
// DASHBOARD
// =====================================================

function Dashboard() {
  // =====================================================
  // MAIN DASHBOARD STATE
  // =====================================================

  const [api, setApi] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [latestYear, setLatestYear] = useState(null);

  const [topRevenue, setTopRevenue] = useState(null);
  const [topProfit, setTopProfit] = useState(null);

  const [sectorData, setSectorData] = useState([]);

  const [revenueRanking, setRevenueRanking] = useState([]);
  const [profitRanking, setProfitRanking] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // =====================================================
  // COMPANY STATE
  // =====================================================

  const [companies, setCompanies] = useState([]);

  // =====================================================
  // DYNAMIC CHART STATE
  // =====================================================

  const [selectedCompany, setSelectedCompany] = useState("");

  const [revenueTrend, setRevenueTrend] = useState([]);
  const [marketCapData, setMarketCapData] = useState([]);
  const [stockHistory, setStockHistory] = useState([]);

  // =====================================================
  // INITIAL DASHBOARD LOAD
  // =====================================================

  useEffect(() => {
    let mounted = true;

    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        // -------------------------------------------------
        // BACKEND HEALTH CHECK
        // -------------------------------------------------

        const response = await fetch(
          "http://127.0.0.1:8000/"
        ).catch(() => {
          throw new Error(
            "Unable to connect to backend server at http://127.0.0.1:8000/"
          );
        });

        if (!response.ok) {
          throw new Error(
            "Backend server returned an invalid response."
          );
        }

        const apiData = await response.json();

        if (!mounted) return;

        setApi(apiData);

        // -------------------------------------------------
        // LOAD DASHBOARD APIs IN PARALLEL
        // -------------------------------------------------

        const [
          dashboardData,
          yearData,
          revenueData,
          profitData,
          sector,
          revenueRank,
          profitRank,
          companyList,
        ] = await Promise.all([
          getDashboard(),
          getLatestYear(),
          getTopRevenue(),
          getTopProfit(),
          getSectorDistribution(),
          getRevenueRanking(),
          getProfitRanking(),
          getCompanies(),
        ]);

        if (!mounted) return;

        // -------------------------------------------------
        // DASHBOARD
        // -------------------------------------------------

        setDashboard(dashboardData || null);

        setLatestYear(yearData || null);

        setTopRevenue(
          Array.isArray(revenueData)
            ? revenueData[0] || null
            : null
        );

        setTopProfit(
          Array.isArray(profitData)
            ? profitData[0] || null
            : null
        );

        // -------------------------------------------------
        // SECTORS
        // -------------------------------------------------

        setSectorData(
          Array.isArray(sector)
            ? sector
            : []
        );

        // -------------------------------------------------
        // RANKINGS
        // -------------------------------------------------

        setRevenueRanking(
          Array.isArray(revenueRank)
            ? revenueRank
            : []
        );

        setProfitRanking(
          Array.isArray(profitRank)
            ? profitRank
            : []
        );

        // -------------------------------------------------
        // COMPANIES
        // -------------------------------------------------

        const safeCompanies = Array.isArray(companyList)
          ? companyList
          : [];

        setCompanies(safeCompanies);

        // -------------------------------------------------
        // SELECT FIRST COMPANY
        // -------------------------------------------------

        if (safeCompanies.length > 0) {
          const firstCompany =
            safeCompanies[0]?.id ||
            safeCompanies[0]?.company_id ||
            "";

          setSelectedCompany(firstCompany);
        }
      } catch (err) {
        console.error(
          "Dashboard Loading Error:",
          err
        );

        if (!mounted) return;

        setError(
          err.message ||
            "Failed to load dashboard data. Please try again."
        );
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      mounted = false;
    };
  }, []);

  // =====================================================
  // DYNAMIC CHART DATA
  // =====================================================

  useEffect(() => {
    if (!selectedCompany) {
      setRevenueTrend([]);
      setMarketCapData([]);
      setStockHistory([]);
      return;
    }

    let mounted = true;

    async function loadCharts() {
      try {
        console.log(
          "📊 Loading charts for:",
          selectedCompany
        );

        // -------------------------------------------------
        // LOAD CHART DATA IN PARALLEL
        // -------------------------------------------------

        const [
          revenue,
          market,
          stock,
        ] = await Promise.all([
          getRevenueTrend(selectedCompany),
          getMarketCap(),
          getStockHistory(selectedCompany),
        ]);

        if (!mounted) return;

        console.log(
          "📈 Revenue:",
          revenue
        );

        console.log(
          "💰 Market Cap:",
          market
        );

        console.log(
          "📊 Stock History:",
          stock
        );

        setRevenueTrend(
          Array.isArray(revenue)
            ? revenue
            : []
        );

        setMarketCapData(
          Array.isArray(market)
            ? market
            : []
        );

        setStockHistory(
          Array.isArray(stock)
            ? stock
            : []
        );
      } catch (err) {
        console.error(
          "Chart Loading Error:",
          err
        );

        if (!mounted) return;

        setRevenueTrend([]);
        setMarketCapData([]);
        setStockHistory([]);
      }
    }

    loadCharts();

    return () => {
      mounted = false;
    };
  }, [selectedCompany]);

  // =====================================================
  // AUTO REFRESH - 5 MINUTES
  // =====================================================

  useEffect(() => {
    const interval = setInterval(() => {
      window.location.reload();
    }, 300000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  // =====================================================
  // CALCULATED VALUES
  // =====================================================

  const averageROE =
    dashboard?.average_roe ?? 0;

  const averageROCE =
    dashboard?.average_roce ?? 0;

  const totalMarketCap =
    dashboard?.total_market_cap ??
    "₹ --";

  // =====================================================
  // LOADING SCREEN
  // =====================================================

  if (loading) {
    return (
      <Layout>
        <Header />

        <div
          style={{
            minHeight: "70vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <LoadingSpinner />
        </div>
      </Layout>
    );
  }

  // =====================================================
  // ERROR SCREEN
  // =====================================================

  if (error) {
    return (
      <Layout>
        <Header />

        <div
          style={{
            padding: "40px",
          }}
        >
          <ErrorMessage
            message={error}
            onRetry={() =>
              window.location.reload()
            }
          />
        </div>
      </Layout>
    );
  }

  // =====================================================
  // MAIN DASHBOARD
  // =====================================================

  return (
    <Layout>
      <Header />

      <div
        style={{
          padding: "25px",
          background: "#f8fafc",
          minHeight: "100vh",
        }}
      >

        {/* =================================================
            DASHBOARD STATS
        ================================================= */}

        <DashboardStats
          companies={
            dashboard?.companies ??
            companies.length
          }
          sectors={
            dashboard?.total_sectors ??
            sectorData.length
          }
          avgROE={averageROE}
          totalMarketCap={totalMarketCap}
        />

        {/* =================================================
            QUICK NAVIGATION
        ================================================= */}

        <div
          style={{
            marginTop: "30px",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "20px",
              flexWrap: "wrap",
              gap: "15px",
            }}
          >
            <h2>
              Quick Navigation
            </h2>

            {/* COMPANY SELECTOR */}

            {companies.length > 0 && (
              <div>
                <label
                  htmlFor="company-select"
                  style={{
                    marginRight: "10px",
                    fontWeight: "bold",
                  }}
                >
                  Select Company:
                </label>

                <select
                  id="company-select"
                  value={selectedCompany}
                  onChange={(event) =>
                    setSelectedCompany(
                      event.target.value
                    )
                  }
                  style={{
                    padding: "8px 12px",
                    borderRadius: "6px",
                    border:
                      "1px solid #ccc",
                    fontSize: "14px",
                    background: "#ffffff",
                    minWidth: "220px",
                  }}
                >
                  {companies.map(
                    (company) => {
                      const companyId =
                        company.id ||
                        company.company_id;

                      const companyName =
                        company.name ||
                        company.company_name ||
                        companyId;

                      return (
                        <option
                          key={companyId}
                          value={companyId}
                        >
                          {companyName}
                        </option>
                      );
                    }
                  )}
                </select>
              </div>
            )}
          </div>

          <QuickLinks />
        </div>

        {/* =================================================
            KPI CARDS
        ================================================= */}

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
            value={
              dashboard?.companies ??
              companies.length
            }
            subtitle="Listed Companies"
            icon={<FaBuilding />}
            color="#2563eb"
          />

          <StatCard
            title="Average ROE"
            value={`${averageROE}%`}
            subtitle="Return on Equity"
            icon={<FaChartBar />}
            color="#16a34a"
          />

          <StatCard
            title="Average ROCE"
            value={`${averageROCE}%`}
            subtitle="Capital Efficiency"
            icon={<FaDatabase />}
            color="#dc2626"
          />

          <StatCard
            title="Sectors"
            value={
              dashboard?.total_sectors ??
              sectorData.length
            }
            subtitle="Market Sectors"
            icon={<FaIndustry />}
            color="#9333ea"
          />
        </div>

        {/* =================================================
            DAY 13 FEATURES
        ================================================= */}

        <MarketOverview
          dashboard={dashboard}
        />

        <InvestmentInsights
          dashboard={dashboard}
        />

        {/* =================================================
            SUMMARY CARDS
        ================================================= */}

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
            value={
              api?.status ||
              "Online"
            }
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
                    dashboard.total_revenue || 0
                  ).toLocaleString(
                    "en-IN"
                  )}`
                : "-"
            }
          />

          <InfoCard
            title="Total Profit"
            value={
              dashboard
                ? `₹ ${Number(
                    dashboard.total_profit || 0
                  ).toLocaleString(
                    "en-IN"
                  )}`
                : "-"
            }
          />

          <InfoCard
            title="Top Revenue Company"
            value={
              topRevenue?.company_name ||
              topRevenue?.company ||
              "-"
            }
          />

          <InfoCard
            title="Top Profit Company"
            value={
              topProfit?.company_name ||
              topProfit?.company ||
              "-"
            }
          />

          <InfoCard
            title="Sector Distribution"
            value={`${sectorData.length} Sectors`}
          />
        </div>

        {/* =================================================
            MAIN DASHBOARD CHARTS
        ================================================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "40px",
          }}
        >
          {!dashboard ? (
            <EmptyState
              title="Dashboard Chart Data Not Available"
            />
          ) : (
            <DashboardChart
              dashboard={dashboard}
            />
          )}

          {sectorData.length === 0 ? (
            <EmptyState
              title="Sector Analytics Not Available"
            />
          ) : (
            <SectorPieChart
              sectorData={sectorData}
            />
          )}
        </div>

        {/* =================================================
            RANKINGS
        ================================================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "40px",
          }}
        >
          {revenueRanking.length === 0 ? (
            <EmptyState
              title="Revenue Rankings Not Available"
            />
          ) : (
            <RevenueRanking
              data={revenueRanking}
            />
          )}

          {profitRanking.length === 0 ? (
            <EmptyState
              title="Profit Rankings Not Available"
            />
          ) : (
            <ProfitRanking
              data={profitRanking}
            />
          )}
        </div>

        {/* =================================================
            SECTOR ANALYTICS
        ================================================= */}

        {sectorData.length === 0 ? (
          <EmptyState
            title="Sector Overview Not Available"
          />
        ) : (
          <SectorAnalytics
            data={sectorData}
          />
        )}

        {/* =================================================
            ANALYTICS SUMMARY
        ================================================= */}

        <AnalyticsOverview
          dashboard={dashboard}
        />

        {/* =================================================
            COMPANY FINANCIAL ANALYTICS
        ================================================= */}

        <div
          style={{
            marginTop: "40px",
          }}
        >
          <h2>
            Company Financial Analytics
          </h2>

          <p
            style={{
              color: "#64748b",
              marginBottom: "20px",
            }}
          >
            Showing analytics for{" "}
            <strong>
              {selectedCompany || "-"}
            </strong>
          </p>
        </div>

        {/* =================================================
            DYNAMIC CHARTS
        ================================================= */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(500px,1fr))",
            gap: "25px",
            marginTop: "20px",
          }}
        >

          {/* REVENUE TREND */}

          {revenueTrend.length === 0 ? (
            <EmptyState
              title="Revenue Trend Data Not Available"
            />
          ) : (
            <PriceLineChart
              data={revenueTrend}
            />
          )}

          {/* MARKET CAP */}

          {marketCapData.length === 0 ? (
            <EmptyState
              title="Market Cap Data Not Available"
            />
          ) : (
            <VolumeBarChart
              data={marketCapData}
            />
          )}

          {/* STOCK HISTORY */}

          {stockHistory.length === 0 ? (
            <EmptyState
              title="Stock History Not Available"
            />
          ) : (
            <PriceChart
              data={stockHistory}
            />
          )}
        </div>

        {/* =================================================
            MARKET ACTIVITY
        ================================================= */}

        <div
          style={{
            marginTop: "40px",
          }}
        >
          <h2>
            Market Activity
          </h2>

          <p
            style={{
              color: "#64748b",
              marginBottom: "20px",
            }}
          >
            Trading activity across
            NIFTY100 companies.
          </p>

          {/* MARKET SHARE PIE CHART */}

          {marketCapData.length === 0 ? (
            <EmptyState
              title="Market Activity Data Not Available"
            />
          ) : (
            <MarketSharePieChart
              stocks={marketCapData}
            />
          )}
        </div>

      </div>
    </Layout>
  );
}

// =======================================================
// INFO CARD
// =======================================================

function InfoCard({
  title,
  value,
}) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow:
          "0 5px 15px rgba(0,0,0,0.06)",
      }}
    >
      <p
        style={{
          margin: 0,
          color: "#64748b",
          fontSize: "14px",
          fontWeight: "600",
        }}
      >
        {title}
      </p>

      <h3
        style={{
          marginTop: "8px",
          marginBottom: 0,
        }}
      >
        {value}
      </h3>
    </div>
  );
}

export default Dashboard;