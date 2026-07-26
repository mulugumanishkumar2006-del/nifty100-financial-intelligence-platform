import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function DashboardChart({ dashboard }) {
  const data = [
    {
      name: "Revenue",
      value: dashboard?.total_revenue || 0,
    },
    {
      name: "Profit",
      value: dashboard?.total_profit || 0,
    },
  ];

  return (
    <div className="card">
      <h2>Financial Overview</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 10,
          }}
        >
          <CartesianGrid strokeDasharray="4 4" />

          <XAxis dataKey="name" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="value"
            fill="#2563eb"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DashboardChart;