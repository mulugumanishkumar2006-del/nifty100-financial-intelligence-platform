import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { getStockHistoryChart } from "../../services/companyService";

function StockHistoryChart({ company }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadStockHistory = async () => {
      if (!company?.id) {
        setData([]);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        console.log(
          "📈 Loading stock history for:",
          company.id
        );

        const result = await getStockHistoryChart(company.id);

        console.log(
          "📈 Stock History API Response:",
          result
        );

        if (Array.isArray(result)) {
          setData(result);
        } else {
          setData([]);
          setError(
            "Invalid stock history data received from API."
          );
        }
      } catch (err) {
        console.error(
          "Stock History Chart Error:",
          err
        );

        setData([]);
        setError(
          "Unable to load stock history."
        );
      } finally {
        setLoading(false);
      }
    };

    loadStockHistory();
  }, [company?.id]);

  // ======================================================
  // No company
  // ======================================================

  if (!company?.id) {
    return (
      <div className="chart-card">
        <h2>📈 Stock Price History</h2>

        <p>
          Select a company to view stock price history.
        </p>
      </div>
    );
  }

  // ======================================================
  // Loading
  // ======================================================

  if (loading) {
    return (
      <div className="chart-card">
        <h2>📈 Stock Price History</h2>

        <p>Loading stock price history...</p>
      </div>
    );
  }

  // ======================================================
  // Error
  // ======================================================

  if (error) {
    return (
      <div className="chart-card">
        <h2>📈 Stock Price History</h2>

        <p style={{ color: "#dc2626" }}>
          {error}
        </p>
      </div>
    );
  }

  // ======================================================
  // No data
  // ======================================================

  if (data.length === 0) {
    return (
      <div className="chart-card">
        <h2>📈 Stock Price History</h2>

        <p>
          No stock price data available for{" "}
          {company.company_name || company.name}.
        </p>
      </div>
    );
  }

  // ======================================================
  // Chart
  // ======================================================

  return (
    <div
      className="chart-card"
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        marginTop: "25px",
        boxShadow:
          "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      {/* Header */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <div>
          <h2
            style={{
              margin: 0,
              color: "#2563eb",
            }}
          >
            📈 Stock Price History
          </h2>

          <p
            style={{
              marginTop: "6px",
              color: "#6b7280",
              fontSize: "14px",
            }}
          >
            Historical stock prices of{" "}
            <strong>
              {company.company_name ||
                company.name}
            </strong>
          </p>
        </div>

        <div
          style={{
            background: "#eff6ff",
            color: "#2563eb",
            padding: "8px 14px",
            borderRadius: "20px",
            fontSize: "13px",
            fontWeight: "600",
          }}
        >
          {data.length} Records
        </div>
      </div>

      {/* Chart */}

      <div
        style={{
          width: "100%",
          height: "350px",
        }}
      >
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <LineChart
            data={data}
            margin={{
              top: 10,
              right: 20,
              left: 10,
              bottom: 10,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#e5e7eb"
            />

            <XAxis
              dataKey="date"
              tick={{
                fontSize: 11,
                fill: "#6b7280",
              }}
            />

            <YAxis
              tick={{
                fontSize: 12,
                fill: "#6b7280",
              }}
              tickFormatter={(value) =>
                `₹${value}`
              }
            />

            <Tooltip
              formatter={(value) => [
                `₹${Number(value).toFixed(2)}`,
                "Close Price",
              ]}
              labelFormatter={(label) =>
                `Date: ${label}`
              }
            />

            <Line
              type="monotone"
              dataKey="close"
              stroke="#2563eb"
              strokeWidth={3}
              dot={false}
              activeDot={{
                r: 6,
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Footer */}

      <div
        style={{
          marginTop: "15px",
          paddingTop: "15px",
          borderTop:
            "1px solid #e5e7eb",
          display: "flex",
          justifyContent: "space-between",
          color: "#6b7280",
          fontSize: "13px",
        }}
      >
        <span>
          Source: NIFTY100 Financial Database
        </span>

        <span>
          Closing price history
        </span>
      </div>
    </div>
  );
}

export default StockHistoryChart;