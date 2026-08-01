import React from "react";

function PortfolioTable() {
  const portfolioData = [
    {
      company: "TCS",
      quantity: 25,
      buyPrice: 3450,
      currentPrice: 3820,
    },
    {
      company: "Infosys",
      quantity: 40,
      buyPrice: 1560,
      currentPrice: 1630,
    },
    {
      company: "Reliance",
      quantity: 15,
      buyPrice: 2450,
      currentPrice: 2395,
    },
    {
      company: "HDFC Bank",
      quantity: 30,
      buyPrice: 1680,
      currentPrice: 1755,
    },
  ];

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        overflowX: "auto",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>
        📊 Portfolio Holdings
      </h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr
            style={{
              background: "#f3f4f6",
            }}
          >
            <th style={thStyle}>Company</th>
            <th style={thStyle}>Quantity</th>
            <th style={thStyle}>Buy Price</th>
            <th style={thStyle}>Current Price</th>
            <th style={thStyle}>Investment</th>
            <th style={thStyle}>Current Value</th>
            <th style={thStyle}>Profit / Loss</th>
          </tr>
        </thead>

        <tbody>
          {portfolioData.map((stock, index) => {
            const investment =
              stock.quantity * stock.buyPrice;

            const currentValue =
              stock.quantity * stock.currentPrice;

            const profit =
              currentValue - investment;

            return (
              <tr key={index}>
                <td style={tdStyle}>{stock.company}</td>

                <td style={tdStyle}>{stock.quantity}</td>

                <td style={tdStyle}>
                  ₹{stock.buyPrice.toLocaleString()}
                </td>

                <td style={tdStyle}>
                  ₹{stock.currentPrice.toLocaleString()}
                </td>

                <td style={tdStyle}>
                  ₹{investment.toLocaleString()}
                </td>

                <td style={tdStyle}>
                  ₹{currentValue.toLocaleString()}
                </td>

                <td
                  style={{
                    ...tdStyle,
                    color:
                      profit >= 0
                        ? "#16a34a"
                        : "#dc2626",
                    fontWeight: "bold",
                  }}
                >
                  {profit >= 0 ? "+" : "-"}₹
                  {Math.abs(profit).toLocaleString()}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

const thStyle = {
  padding: "15px",
  textAlign: "left",
  fontWeight: "600",
};

const tdStyle = {
  padding: "15px",
  borderBottom: "1px solid #e5e7eb",
};

export default PortfolioTable;