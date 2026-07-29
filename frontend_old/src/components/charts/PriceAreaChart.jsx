import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  Legend,
} from "recharts";

function PriceAreaChart({ stocks }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2>📈 Current Price vs 52 Week High</h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <AreaChart data={stocks}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="company" />

          <YAxis />

          <Tooltip />

          <Legend />

          <Area
            type="monotone"
            dataKey="price"
            stroke="#2563eb"
            fill="#93c5fd"
            name="Current Price"
          />

          <Area
            type="monotone"
            dataKey="high52"
            stroke="#16a34a"
            fill="#86efac"
            name="52W High"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceAreaChart;