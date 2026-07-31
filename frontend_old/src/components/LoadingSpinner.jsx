function LoadingSpinner() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "300px",
      }}
    >
      <div
        style={{
          width: "60px",
          height: "60px",
          border: "6px solid #e5e7eb",
          borderTop: "6px solid #2563eb",
          borderRadius: "50%",
          animation: "spin 1s linear infinite",
        }}
      />
    </div>
  );
}

export default LoadingSpinner;