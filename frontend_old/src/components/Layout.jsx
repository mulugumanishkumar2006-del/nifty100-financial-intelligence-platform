import Sidebar from "./Sidebar";

function Layout({ children }) {
  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background:
          "linear-gradient(to bottom right, #f8fafc, #eef2ff)",
      }}
    >
      {/* ================= Sidebar ================= */}

      <div
        style={{
          position: "sticky",
          top: 0,
          height: "100vh",
          flexShrink: 0,
        }}
      >
        <Sidebar />
      </div>

      {/* ================= Main Content ================= */}

      <main
        className="fade-in"
        style={{
          flex: 1,
          padding: "35px",
          overflowY: "auto",
          overflowX: "hidden",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            maxWidth: "1600px",
            margin: "0 auto",
            width: "100%",
          }}
        >
          {children}
        </div>
      </main>
    </div>
  );
}

export default Layout;