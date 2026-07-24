import Layout from "../components/Layout";
import CompanyTable from "../components/CompanyTable";

function Companies() {
  return (
    <Layout>
      <div
        style={{
          marginBottom: "30px",
        }}
      >
        <h1
          style={{
            fontSize: "32px",
            fontWeight: "700",
            color: "#111827",
            marginBottom: "10px",
          }}
        >
          🏢 NIFTY100 Companies
        </h1>

        <p
          style={{
            color: "#6b7280",
            fontSize: "16px",
          }}
        >
          Browse, search and filter all listed companies in the
          NIFTY100 Financial Intelligence Platform.
        </p>
      </div>

      <CompanyTable />
    </Layout>
  );
}

export default Companies;