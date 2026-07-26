import {
  FaBuilding,
  FaMoneyBillWave,
  FaChartLine,
  FaPercent,
  FaCalendarAlt,
  FaIndustry,
} from "react-icons/fa";

function AnalyticsOverview({ dashboard }) {
  if (!dashboard) return <h3>Loading Analytics...</h3>;

  const cards = [
    {
      title: "Total Companies",
      value: dashboard.companies,
      icon: <FaBuilding />,
      color: "#2563eb",
    },
    {
      title: "Total Revenue",
      value: `₹ ${Number(dashboard.total_revenue).toLocaleString()}`,
      icon: <FaMoneyBillWave />,
      color: "#16a34a",
    },
    {
      title: "Total Profit",
      value: `₹ ${Number(dashboard.total_profit).toLocaleString()}`,
      icon: <FaChartLine />,
      color: "#dc2626",
    },
    {
      title: "Average ROE",
      value: `${dashboard.average_roe}%`,
      icon: <FaPercent />,
      color: "#7c3aed",
    },
    {
      title: "Average ROCE",
      value: `${dashboard.average_roce}%`,
      icon: <FaIndustry />,
      color: "#ea580c",
    },
    {
      title: "Latest Year",
      value: dashboard.latest_year,
      icon: <FaCalendarAlt />,
      color: "#0f766e",
    },
  ];

  return (
    <div
      style={{
        marginTop: "50px",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
        }}
      >
        Analytics Overview
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
          gap: "20px",
        }}
      >
        {cards.map((card) => (
          <div
            key={card.title}
            style={{
              background: "#ffffff",
              borderRadius: "12px",
              padding: "20px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
            }}
          >
            <div
              style={{
                fontSize: "28px",
                color: card.color,
                marginBottom: "12px",
              }}
            >
              {card.icon}
            </div>

            <h3
              style={{
                margin: 0,
                fontSize: "15px",
                color: "#555",
              }}
            >
              {card.title}
            </h3>

            <h2
              style={{
                marginTop: "10px",
                color: card.color,
              }}
            >
              {card.value}
            </h2>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AnalyticsOverview;