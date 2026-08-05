import { useEffect, useState } from "react";
import { getCompanyRatios } from "../../services/companyService";

function FinancialRatios({ company }) {
  const [ratios, setRatios] = useState(null);

  useEffect(() => {
    async function loadRatios() {
      if (!company?.id) return;

      const data = await getCompanyRatios(company.id);

      if (data && data.length > 0) {
        setRatios(data[0]); // Latest Year
      }
    }

    loadRatios();
  }, [company]);

  if (!ratios) {
    return (
      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "15px",
          marginTop: "30px",
          boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        }}
      >
        <h2>📊 Financial Ratios</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        marginTop: "30px",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: "25px",
        }}
      >
        📊 Financial Ratios ({ratios.year})
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        <RatioCard
          title="ROE"
          value={ratios.return_on_equity_pct}
          suffix="%"
          color="#2563eb"
        />

        <RatioCard
          title="Net Profit Margin"
          value={ratios.net_profit_margin_pct}
          suffix="%"
          color="#16a34a"
        />

        <RatioCard
          title="Operating Margin"
          value={ratios.operating_profit_margin_pct}
          suffix="%"
          color="#0ea5e9"
        />

        <RatioCard
          title="Debt to Equity"
          value={ratios.debt_to_equity}
          color="#dc2626"
        />

        <RatioCard
          title="Interest Coverage"
          value={ratios.interest_coverage}
          color="#7c3aed"
        />

        <RatioCard
          title="Asset Turnover"
          value={ratios.asset_turnover}
          color="#0891b2"
        />

        <RatioCard
          title="EPS"
          value={ratios.earnings_per_share}
          color="#f59e0b"
        />

        <RatioCard
          title="Book Value"
          value={ratios.book_value_per_share}
          color="#2563eb"
        />

        <RatioCard
          title="Dividend Payout"
          value={ratios.dividend_payout_ratio_pct}
          suffix="%"
          color="#16a34a"
        />

        <RatioCard
          title="Free Cash Flow"
          value={ratios.free_cash_flow_cr}
          color="#8b5cf6"
        />

        <RatioCard
          title="Total Debt"
          value={ratios.total_debt_cr}
          color="#dc2626"
        />

        <RatioCard
          title="Cash From Operations"
          value={ratios.cash_from_operations_cr}
          color="#0f766e"
        />
      </div>
    </div>
  );
}

function RatioCard({
  title,
  value,
  suffix = "",
  color,
}) {
  return (
    <div
      style={{
        background: "#f8fafc",
        padding: "20px",
        borderRadius: "12px",
        borderLeft: `5px solid ${color}`,
      }}
    >
      <h3
        style={{
          marginBottom: "12px",
          color: "#475569",
          fontSize: "15px",
        }}
      >
        {title}
      </h3>

      <h2
        style={{
          color,
          margin: 0,
          fontSize: "28px",
          fontWeight: "700",
        }}
      >
        {value ?? "-"}
        {value !== null && value !== undefined ? suffix : ""}
      </h2>
    </div>
  );
}

export default FinancialRatios;