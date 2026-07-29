import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function ROEChart({ data = [] }) {
  const chartData = [...data]
    .sort(
      (a, b) =>
        (Number(b.roe_percentage) || 0) -
        (Number(a.roe_percentage) || 0)
    )
    .slice(0, 10);

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
        marginTop: "30px",
      }}
    >
      <h2>📊 Top 10 ROE Companies</h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="company_name"
            angle={-25}
            textAnchor="end"
            interval={0}
            height={80}
          />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="roe_percentage"
            fill="#2563eb"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ROEChart;