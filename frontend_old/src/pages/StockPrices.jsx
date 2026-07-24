import Layout from "../components/Layout";

function StockPrices() {
  const stocks = [
    {
      company: "Reliance",
      price: "₹2,985.40",
      change: "+1.25%",
      high52: "₹3,210",
      low52: "₹2,220",
      volume: "5.8M",
    },
    {
      company: "TCS",
      price: "₹4,230.75",
      change: "-0.42%",
      high52: "₹4,590",
      low52: "₹3,510",
      volume: "2.3M",
    },
    {
      company: "Infosys",
      price: "₹1,725.30",
      change: "+0.88%",
      high52: "₹1,950",
      low52: "₹1,350",
      volume: "4.1M",
    },
    {
      company: "HDFC Bank",
      price: "₹1,645.20",
      change: "-0.21%",
      high52: "₹1,790",
      low52: "₹1,420",
      volume: "6.2M",
    },
    {
      company: "ICICI Bank",
      price: "₹1,280.15",
      change: "+2.05%",
      high52: "₹1,340",
      low52: "₹950",
      volume: "8.4M",
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
          📉 Stock Prices
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "30px",
          }}
        >
          Daily stock price overview of selected NIFTY100 companies.
        </p>

        <div
          style={{
            background: "#ffffff",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
            }}
          >
            <thead>
              <tr
                style={{
                  background: "#2563eb",
                  color: "#ffffff",
                }}
              >
                <th style={{ padding: "12px" }}>Company</th>
                <th>Current Price</th>
                <th>Daily Change</th>
                <th>52W High</th>
                <th>52W Low</th>
                <th>Volume</th>
              </tr>
            </thead>

            <tbody>
              {stocks.map((stock, index) => (
                <tr
                  key={index}
                  style={{
                    borderBottom: "1px solid #e5e7eb",
                    textAlign: "center",
                  }}
                >
                  <td
                    style={{
                      padding: "12px",
                      fontWeight: "600",
                    }}
                  >
                    {stock.company}
                  </td>

                  <td>{stock.price}</td>

                  <td
                    style={{
                      color: stock.change.startsWith("+")
                        ? "#16a34a"
                        : "#dc2626",
                      fontWeight: "bold",
                    }}
                  >
                    {stock.change}
                  </td>

                  <td>{stock.high52}</td>

                  <td>{stock.low52}</td>

                  <td>{stock.volume}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Market Summary */}

        <div
          style={{
            marginTop: "30px",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
            gap: "20px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>📈 Top Gainer</h3>
            <h2 style={{ color: "#16a34a" }}>
              ICICI Bank (+2.05%)
            </h2>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>📉 Top Loser</h3>
            <h2 style={{ color: "#dc2626" }}>
              TCS (-0.42%)
            </h2>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>📊 Total Volume</h3>
            <h2 style={{ color: "#2563eb" }}>
              26.8M Shares
            </h2>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default StockPrices;