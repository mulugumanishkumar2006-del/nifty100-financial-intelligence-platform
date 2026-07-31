function EmptyState({ title }) {
  return (
    <div
      style={{
        padding: "40px",
        textAlign: "center",
        background: "#fff",
        borderRadius: "12px",
      }}
    >
      <h2>📭 No Data Available</h2>

      <p>{title}</p>
    </div>
  );
}

export default EmptyState;