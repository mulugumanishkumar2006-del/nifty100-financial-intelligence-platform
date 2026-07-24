import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function DashboardChart({ dashboard }) {
  if (!dashboard) return <h3>Loading Chart...</h3>;

  const data = [
    {
      name: "Companies",
      value: dashboard.companies,
    },
    {
      name: "Ratios",
      value: dashboard.financial_ratios,
    },
    {
      name: "Prices",
      value: dashboard.stock_prices,
    },
    {
      name: "Sectors",
      value: dashboard.sectors,
    },
  ];

  return (
    <div
      style={{
        background: "white",
        marginTop: "30px",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
      }}
    >
      <h2>Platform Statistics</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#2563eb" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DashboardChart;