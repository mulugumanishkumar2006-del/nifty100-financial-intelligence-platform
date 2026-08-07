import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function ROETrendChart({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div
        style={{
          background: "#ffffff",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        }}
      >
        <h3>📈 ROE Trend</h3>
        <p>No ROE data available.</p>
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginBottom: "20px" }}>
        📈 Return on Equity Trend
      </h3>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart
          data={data}
          margin={{
            top: 10,
            right: 30,
            left: 10,
            bottom: 10,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis
            tickFormatter={(value) => `${value}%`}
          />

          <Tooltip
            formatter={(value) => [
              `${value}%`,
              "ROE",
            ]}
          />

          <Legend />

          <Line
            type="monotone"
            dataKey="roe"
            name="ROE"
            stroke="#9333ea"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ROETrendChart;