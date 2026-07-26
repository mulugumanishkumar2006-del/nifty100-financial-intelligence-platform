import "./StatCard.css";

function StatCard({
  title,
  value,
  subtitle,
  icon,
  color,
}) {
  return (
    <div className="stat-card">
      <div className="stat-header">
        <div
          className="stat-icon"
          style={{ backgroundColor: color }}
        >
          {icon}
        </div>

        <div className="stat-title">
          {title}
        </div>
      </div>

      <div className="stat-value">
        {value}
      </div>

      <div className="stat-subtitle">
        {subtitle}
      </div>
    </div>
  );
}

export default StatCard;