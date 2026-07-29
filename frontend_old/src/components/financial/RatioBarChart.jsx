import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function RatioBarChart({ data }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "12px",
        marginTop: "30px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          color: "#2563eb",
        }}
      >
        📊 Top ROE Companies
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <BarChart
          data={data.slice(0,10)}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="company_name"
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

export default RatioBarChart;