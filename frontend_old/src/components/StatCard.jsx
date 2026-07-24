function StatCard({ title, value, icon, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <div>
        <h3>{title}</h3>

        <h1
          style={{
            color: color,
            marginTop: "10px",
          }}
        >
          {value}
        </h1>
      </div>

      <div
        style={{
          fontSize: "40px",
          color: color,
        }}
      >
        {icon}
      </div>
    </div>
  );
}

export default StatCard;