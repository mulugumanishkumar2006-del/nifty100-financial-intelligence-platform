function ErrorMessage({ message, onRetry }) {
  return (
    <div
      style={{
        background: "#fee2e2",
        color: "#991b1b",
        padding: "20px",
        borderRadius: "10px",
        textAlign: "center",
        margin: "20px 0",
      }}
    >
      <h3>⚠️ Something went wrong</h3>

      <p>{message}</p>

      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            marginTop: "15px",
            padding: "10px 18px",
            border: "none",
            borderRadius: "8px",
            background: "#dc2626",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Retry
        </button>
      )}
    </div>
  );
}

export default ErrorMessage;