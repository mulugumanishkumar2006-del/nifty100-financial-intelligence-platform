import Layout from "../components/Layout";

function Analytics() {
  const cards = [
    {
      title: "Market Overview",
      value: "100 Companies",
      color: "#2563eb",
    },
    {
      title: "Top Performing Sector",
      value: "Financials",
      color: "#16a34a",
    },
    {
      title: "Average ROE",
      value: "18.5%",
      color: "#9333ea",
    },
    {
      title: "Average ROCE",
      value: "21.2%",
      color: "#dc2626",
    },
  ];

  return (
    <Layout>
      <div>
        <h1
          style={{
            fontSize: "32px",
            fontWeight: "700",
            marginBottom: "10px",
          }}
        >
          📊 Analytics Dashboard
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "30px",
          }}
        >
          Executive insights and overall market analytics.
        </p>

        {/* KPI Cards */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
            gap: "20px",
          }}
        >
          {cards.map((card, index) => (
            <div
              key={index}
              style={{
                background: "#ffffff",
                borderLeft: `6px solid ${card.color}`,
                padding: "25px",
                borderRadius: "12px",
                boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
              }}
            >
              <h3
                style={{
                  color: "#6b7280",
                  marginBottom: "10px",
                }}
              >
                {card.title}
              </h3>

              <h1
                style={{
                  color: card.color,
                  margin: 0,
                }}
              >
                {card.value}
              </h1>
            </div>
          ))}
        </div>

        {/* Charts Placeholder */}

        <div
          style={{
            marginTop: "40px",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(400px,1fr))",
            gap: "20px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              height: "350px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "22px",
              color: "#9ca3af",
            }}
          >
            📈 Revenue Analytics Chart
          </div>

          <div
            style={{
              background: "#ffffff",
              height: "350px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "22px",
              color: "#9ca3af",
            }}
          >
            🥧 Sector Analytics Chart
          </div>
        </div>

        {/* Summary */}

        <div
          style={{
            marginTop: "40px",
            background: "#ffffff",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
          }}
        >
          <h2>📋 Summary</h2>

          <ul
            style={{
              lineHeight: "2",
              color: "#374151",
            }}
          >
            <li>Total NIFTY100 Companies</li>
            <li>Sector-wise Performance Analysis</li>
            <li>Top Revenue Companies</li>
            <li>Top Profit Companies</li>
            <li>Financial Ratios Comparison</li>
            <li>Stock Performance Analytics</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}

export default Analytics;