import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Header from "../components/Header";
import StatCard from "../components/StatCard";
import DashboardChart from "../components/DashboardChart";
import SectorPieChart from "../components/SectorPieChart";

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

function Dashboard() {
  const [api, setApi] = useState(null);

  const [dashboard, setDashboard] = useState(null);

  const [latestYear, setLatestYear] = useState(null);

  const [topRevenue, setTopRevenue] = useState(null);

  const [topProfit, setTopProfit] = useState(null);

  const [sectorData, setSectorData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((data) => setApi(data));

    getDashboard().then(setDashboard);

    getLatestYear().then(setLatestYear);

    getTopRevenue().then((data) => {
      if (data?.length) {
        setTopRevenue(data[0]);
      }
    });

    getTopProfit().then((data) => {
      if (data?.length) {
        setTopProfit(data[0]);
      }
    });

    getSectorDistribution().then(setSectorData);
  }, []);

  return (
    <Layout>
      <Header />

      {/* Statistics */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <StatCard
          title="Companies"
          value={dashboard?.companies ?? "..."}
          icon={<FaBuilding />}
          color="#2563eb"
        />

        <StatCard
          title="Financial Ratios"
          value={dashboard?.financial_ratios ?? "..."}
          icon={<FaChartBar />}
          color="#16a34a"
        />

        <StatCard
          title="Stock Prices"
          value={dashboard?.stock_prices ?? "..."}
          icon={<FaDatabase />}
          color="#dc2626"
        />

        <StatCard
          title="Sectors"
          value={dashboard?.sectors ?? "..."}
          icon={<FaIndustry />}
          color="#9333ea"
        />
      </div>

      {/* Info Cards */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))",
          gap: "20px",
          marginTop: "35px",
        }}
      >
        <div className="card">
          <h2>Backend Status</h2>

          {api ? (
            <>
              <p>
                <b>Message :</b> {api.message}
              </p>

              <p>
                <b>Version :</b> {api.version}
              </p>

              <p>
                <b>Status :</b> {api.status}
              </p>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        <div className="card">
          <h2>Latest Financial Year</h2>

          <h3>{latestYear?.latest_year ?? "Loading..."}</h3>
        </div>

        <div className="card">
          <h2>Top Revenue Company</h2>

          <h3>{topRevenue?.company_name ?? "Loading..."}</h3>
        </div>

        <div className="card">
          <h2>Top Profit Company</h2>

          <h3>{topProfit?.company_name ?? "Loading..."}</h3>
        </div>

        <div className="card">
          <h2>Sector Distribution</h2>

          <h3>
            {sectorData
              ? `${sectorData.length} Sectors`
              : "Loading..."}
          </h3>
        </div>
      </div>

      {/* Charts */}

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
    </Layout>
  );
}

export default Dashboard;