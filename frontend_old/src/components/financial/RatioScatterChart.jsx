import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

function RatioScatterChart({ data }) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "25px",
        borderRadius: "12px",
        marginTop: "30px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          color: "#16a34a",
        }}
      >
        ROE vs ROCE
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <ScatterChart>
          <CartesianGrid />

          <XAxis
            type="number"
            dataKey="roe_percentage"
            name="ROE"
          />

          <YAxis
            type="number"
            dataKey="roce_percentage"
            name="ROCE"
          />

          <Tooltip cursor={{ strokeDasharray: "3 3" }} />

          <Scatter
            data={data}
            fill="#16a34a"
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RatioScatterChart;