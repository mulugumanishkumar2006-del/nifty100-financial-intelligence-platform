import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function RevenueChart() {
  const revenueData = [
    { year: "2020", revenue: 42000 },
    { year: "2021", revenue: 47000 },
    { year: "2022", revenue: 51000 },
    { year: "2023", revenue: 59000 },
    { year: "2024", revenue: 65000 },
  ];

  return (
    <div
      style={{
        background: "#ffffff",
        marginTop: "30px",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          color: "#2563eb",
        }}
      >
        📈 Revenue Trend
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <LineChart data={revenueData}>
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

export default RevenueChart;