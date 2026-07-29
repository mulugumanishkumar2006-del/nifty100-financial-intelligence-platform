import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function PriceLineChart({ stocks }) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2>📈 Stock Price Trend</h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <LineChart data={stocks}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="company" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="price"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceLineChart;