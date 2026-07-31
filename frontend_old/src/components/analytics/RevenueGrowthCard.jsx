import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function RevenueGrowthCard({ data = [] }) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2>📈 Revenue Growth</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RevenueGrowthCard;