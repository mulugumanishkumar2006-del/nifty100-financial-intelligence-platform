import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
} from "recharts";

function ChangeBarChart({ stocks }) {
  const COLORS = stocks.map((stock) =>
    stock.change >= 0 ? "#16a34a" : "#dc2626"
  );

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2>📊 Daily Change Comparison</h2>

      <ResponsiveContainer
        width="100%"
        height={380}
      >
        <BarChart data={stocks}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="company" />

          <YAxis />

          <Tooltip
            formatter={(value) => [`${value}%`, "Daily Change"]}
          />

          <Bar
            dataKey="change"
            radius={[8, 8, 0, 0]}
          >
            {stocks.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ChangeBarChart;