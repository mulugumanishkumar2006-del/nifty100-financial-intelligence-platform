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

import { getROETrend } from "../../services/companyService";

function ROEChart({ company }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadROE = async () => {
      if (!company?.id) {
        setData([]);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        console.log("📊 Loading ROE for:", company.id);

        const result = await getROETrend(company.id);

        console.log("📊 ROE API Response:", result);

        if (Array.isArray(result)) {
          setData(result);
        } else {
          setData([]);
          setError("Invalid ROE data received from API.");
        }
      } catch (err) {
        console.error("ROE Chart Error:", err);
        setData([]);
        setError("Unable to load ROE data.");
      } finally {
        setLoading(false);
      }
    };

    loadROE();
  }, [company?.id]);

  // ======================================================
  // No company
  // ======================================================

  if (!company?.id) {
    return (
      <div className="chart-card">
        <h2>📊 ROE Trend</h2>

        <p>
          Select a company to view ROE history.
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
        <h2>📊 ROE Trend</h2>

        <p>Loading ROE data...</p>
      </div>
    );
  }

  // ======================================================
  // Error
  // ======================================================

  if (error) {
    return (
      <div className="chart-card">
        <h2>📊 ROE Trend</h2>

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
        <h2>📊 ROE Trend</h2>

        <p>
          No ROE data available for{" "}
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
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
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
            📊 ROE Trend
          </h2>

          <p
            style={{
              marginTop: "6px",
              color: "#6b7280",
              fontSize: "14px",
            }}
          >
            Return on Equity history of{" "}
            <strong>
              {company.company_name || company.name}
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
          {data.length} Years
        </div>
      </div>

      {/* Chart */}

      <div
        style={{
          width: "100%",
          height: "350px",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
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
              dataKey="year"
              tick={{
                fontSize: 12,
                fill: "#6b7280",
              }}
            />

            <YAxis
              tick={{
                fontSize: 12,
                fill: "#6b7280",
              }}
              tickFormatter={(value) =>
                `${value}%`
              }
            />

            <Tooltip
              formatter={(value) => [
                `${Number(value).toFixed(2)}%`,
                "ROE",
              ]}
              labelFormatter={(label) =>
                `Year: ${label}`
              }
            />

            <Line
              type="monotone"
              dataKey="roe"
              stroke="#16a34a"
              strokeWidth={3}
              dot={{
                r: 4,
              }}
              activeDot={{
                r: 7,
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
          borderTop: "1px solid #e5e7eb",
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
          ROE values shown as percentages
        </span>
      </div>
    </div>
  );
}

export default ROEChart;