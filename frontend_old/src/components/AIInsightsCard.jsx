function AIInsightsCard({
  title,
  value,
  color = "#2563eb",
  icon,
}) {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "18px",
        padding: "24px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${color}`,
        transition: "all 0.3s ease",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-6px)";
        e.currentTarget.style.boxShadow =
          "0 18px 35px rgba(0,0,0,0.15)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0px)";
        e.currentTarget.style.boxShadow =
          "0 10px 30px rgba(0,0,0,0.08)";
      }}
    >
      {/* Icon */}

      {icon && (
        <div
          style={{
            fontSize: "34px",
            color: color,
            marginBottom: "15px",
          }}
        >
          {icon}
        </div>
      )}

      {/* Title */}

      <h3
        style={{
          margin: 0,
          color: "#64748b",
          fontSize: "16px",
          fontWeight: "600",
        }}
      >
        {title}
      </h3>

      {/* Value */}

      <h1
        style={{
          marginTop: "18px",
          marginBottom: "10px",
          color: color,
          fontSize: "34px",
          fontWeight: "700",
        }}
      >
        {value}
      </h1>

      {/* Footer */}

      <p
        style={{
          color: "#94a3b8",
          fontSize: "13px",
          margin: 0,
        }}
      >
        AI Generated Insight
      </p>
    </div>
  );
}

export default AIInsightsCard;