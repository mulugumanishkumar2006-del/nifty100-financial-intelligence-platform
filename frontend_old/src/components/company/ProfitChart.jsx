import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function ProfitChart() {
  const profitData = [
    { year: "2020", profit: 4800 },
    { year: "2021", profit: 5200 },
    { year: "2022", profit: 6100 },
    { year: "2023", profit: 7300 },
    { year: "2024", profit: 8200 },
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
          color: "#16a34a",
        }}
      >
        💹 Profit Trend
      </h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={profitData}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="profit"
            stroke="#16a34a"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ProfitChart;