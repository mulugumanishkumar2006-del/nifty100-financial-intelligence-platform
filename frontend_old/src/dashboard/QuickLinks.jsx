import { Link } from "react-router-dom";

const cards = [
  {
    title: "Companies",
    description: "Browse all NIFTY100 companies",
    path: "/companies",
    color: "#2563eb",
    icon: "🏢",
  },
  {
    title: "Financial Ratios",
    description: "Analyze ROE, ROCE, EPS and P/E",
    path: "/financial-ratios",
    color: "#16a34a",
    icon: "📊",
  },
  {
    title: "Stock Prices",
    description: "Daily market prices",
    path: "/stock-prices",
    color: "#dc2626",
    icon: "📈",
  },
  {
    title: "Sectors",
    description: "Sector-wise analysis",
    path: "/sectors",
    color: "#9333ea",
    icon: "🏭",
  },
  {
    title: "Analytics",
    description: "Business intelligence",
    path: "/analytics",
    color: "#f59e0b",
    icon: "📉",
  },
  {
    title: "AI Intelligence",
    description: "AI-powered financial insights",
    path: "/intelligence",
    color: "#06b6d4",
    icon: "🤖",
  },
];

function QuickLinks() {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
        gap: "20px",
      }}
    >
      {cards.map((card) => (
        <Link
          key={card.title}
          to={card.path}
          style={{
            textDecoration: "none",
          }}
        >
          <div
            style={{
              background: "#fff",
              padding: "25px",
              borderRadius: "15px",
              borderLeft: `6px solid ${card.color}`,
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
              transition: "0.25s",
              cursor: "pointer",
            }}
          >
            <div
              style={{
                fontSize: "40px",
              }}
            >
              {card.icon}
            </div>

            <h2
              style={{
                marginTop: "15px",
                color: "#111827",
              }}
            >
              {card.title}
            </h2>

            <p
              style={{
                color: "#6b7280",
              }}
            >
              {card.description}
            </p>
          </div>
        </Link>
      ))}
    </div>
  );
}

export default QuickLinks;