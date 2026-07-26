import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Header from "../components/Header";
import StatCard from "../components/StatCard";
import DashboardChart from "../components/DashboardChart";
import SectorPieChart from "../components/SectorPieChart";

import RevenueRanking from "../components/analytics/RevenueRanking";
import ProfitRanking from "../components/analytics/ProfitRanking";
import SectorAnalytics from "../components/analytics/SectorAnalytics";
import AnalyticsOverview from "../components/analytics/AnalyticsOverview";

import {
  FaBuilding,
  FaChartBar,
  FaIndustry,
  FaDatabase,
} from "react-icons/fa";

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

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then(setApi);

    getDashboard().then(setDashboard);

    getLatestYear().then(setLatestYear);

    getTopRevenue().then((data) => {
      if (data?.length) setTopRevenue(data[0]);
    });

    getTopProfit().then((data) => {
      if (data?.length) setTopProfit(data[0]);
    });

    getSectorDistribution().then(setSectorData);

    getRevenueRanking().then(setRevenueRanking);

    getProfitRanking().then(setProfitRanking);
  }, []);

  return (
    <Layout>
      <Header />

      {/* ================= KPI Cards ================= */}

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
          value={dashboard?.companies ?? "..."}
          subtitle="Listed Companies"
          icon={<FaBuilding />}
          color="#2563eb"
        />

        <StatCard
          title="Average ROE"
          value={
            dashboard
              ? `${dashboard.average_roe}%`
              : "..."
          }
          subtitle="Return on Equity"
          icon={<FaChartBar />}
          color="#16a34a"
        />

        <StatCard
          title="Average ROCE"
          value={
            dashboard
              ? `${dashboard.average_roce}%`
              : "..."
          }
          subtitle="Capital Efficiency"
          icon={<FaDatabase />}
          color="#dc2626"
        />

        <StatCard
          title="Sectors"
          value={dashboard?.total_sectors ?? "..."}
          subtitle="Market Sectors"
          icon={<FaIndustry />}
          color="#9333ea"
        />
      </div>

      {/* ================= Information Cards ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))",
          gap: "20px",
          marginTop: "35px",
        }}
      >
        <div className="card">
          <h2>Backend Status</h2>

          {api ? (
            <>
              <p><b>Message :</b> {api.message}</p>
              <p><b>Version :</b> {api.version}</p>
              <p><b>Status :</b> {api.status}</p>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        <div className="card">
          <h2>Latest Financial Year</h2>

          <h2>
            {latestYear?.latest_year ??
              dashboard?.latest_year ??
              "Loading..."}
          </h2>
        </div>

        <div className="card">
          <h2>Total Revenue</h2>

          <h2>
            {dashboard
              ? `₹ ${Number(
                  dashboard.total_revenue
                ).toLocaleString("en-IN")}`
              : "Loading..."}
          </h2>
        </div>

        <div className="card">
          <h2>Total Net Profit</h2>

          <h2>
            {dashboard
              ? `₹ ${Number(
                  dashboard.total_profit
                ).toLocaleString("en-IN")}`
              : "Loading..."}
          </h2>
        </div>

        <div className="card">
          <h2>Top Revenue Company</h2>

          <h3>
            {topRevenue?.company_name ??
              "Loading..."}
          </h3>
        </div>

        <div className="card">
          <h2>Top Profit Company</h2>

          <h3>
            {topProfit?.company_name ??
              "Loading..."}
          </h3>
        </div>

        <div className="card">
          <h2>Sector Distribution</h2>

          <h2>
            {sectorData.length
              ? `${sectorData.length} Sectors`
              : "Loading..."}
          </h2>
        </div>
      </div>

      {/* ================= Charts ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
          gap: "25px",
          marginTop: "40px",
        }}
      >
        <DashboardChart dashboard={dashboard} />

        <SectorPieChart sectorData={sectorData} />
      </div>

      {/* ================= Revenue & Profit Ranking ================= */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(500px,1fr))",
          gap: "25px",
          marginTop: "40px",
        }}
      >
        <RevenueRanking data={revenueRanking} />

        <ProfitRanking data={profitRanking} />
      </div>

      {/* ================= Sector Analytics ================= */}

      <div
        style={{
          marginTop: "40px",
        }}
      >
        <SectorAnalytics data={sectorData} />
      </div>

      {/* ================= Analytics Overview ================= */}

      <AnalyticsOverview dashboard={dashboard} />

    </Layout>
  );
}

export default Dashboard;