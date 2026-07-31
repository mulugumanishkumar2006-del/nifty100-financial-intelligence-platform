import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function ProfitGrowthCard({ data = [] }) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2>💰 Profit Growth</h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis />

          <Tooltip />

          <Bar dataKey="profit" fill="#16a34a" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ProfitGrowthCard;