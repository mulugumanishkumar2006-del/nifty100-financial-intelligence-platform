import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const COLORS = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#9333ea",
  "#f59e0b",
  "#14b8a6",
  "#ec4899",
  "#8b5cf6",
  "#22c55e",
  "#0ea5e9",
];

function SectorPieChart({ sectorData }) {
  return (
    <div className="card">
      <h2>Sector Distribution</h2>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
            data={sectorData}
            dataKey="companies"
            nameKey="broad_sector"
            outerRadius={120}
            label
          >
            {sectorData.map((entry, index) => (
              <Cell
                key={index}
                fill={
                  COLORS[index % COLORS.length]
                }
              />
            ))}
          </Pie>

          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SectorPieChart;