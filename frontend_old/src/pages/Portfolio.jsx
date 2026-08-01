import Layout from "../components/Layout";

import PortfolioSummary from "../components/portfolio/PortfolioSummary";
import AddStock from "../components/portfolio/AddStock";
import PortfolioTable from "../components/portfolio/PortfolioTable";
import PortfolioPieChart from "../components/portfolio/PortfolioPieChart";
import PortfolioPerformanceChart from "../components/portfolio/PortfolioPerformanceChart";

function Portfolio() {
  return (
    <Layout>
      <div style={{ marginBottom: "30px" }}>
        <h1>📈 Portfolio Tracker</h1>

        <p
          style={{
            color: "#6b7280",
            fontSize: "16px",
          }}
        >
          Track your investments, monitor profit/loss,
          and analyze portfolio performance.
        </p>
      </div>

      {/* Portfolio Summary */}
      <PortfolioSummary />

      {/* Add Stock */}
      <AddStock />

      {/* Holdings Table */}
      <PortfolioTable />

      {/* Charts */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(450px,1fr))",
          gap: "25px",
          marginTop: "30px",
        }}
      >
        <PortfolioPieChart />

        <PortfolioPerformanceChart />
      </div>
    </Layout>
  );
}

export default Portfolio;