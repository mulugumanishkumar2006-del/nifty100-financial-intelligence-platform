import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

const COLORS = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#9333ea",
  "#f59e0b",
  "#06b6d4",
  "#8b5cf6",
  "#ef4444",
  "#22c55e",
  "#0ea5e9",
];

function SectorDistributionChart({ data = [] }) {
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
        <h3>🏭 Sector Distribution</h3>
        <p>No sector distribution data available.</p>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    name: item.sector,
    value: Number(item.company_count ?? item.count ?? 0),
  }));

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
        🏭 NIFTY100 Sector Distribution
      </h3>

      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={140}
            innerRadius={70}
            paddingAngle={3}
            label={({ name, percent }) =>
              `${name} ${(percent * 100).toFixed(1)}%`
            }
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`sector-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip
            formatter={(value, name) => [
              `${value} companies`,
              name,
            ]}
          />

          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SectorDistributionChart;