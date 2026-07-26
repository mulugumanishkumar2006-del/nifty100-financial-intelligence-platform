import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import CompanyTable from "../components/CompanyTable";
import { getCompanies } from "../services/companyService";

function Companies() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const data = await getCompanies();
        console.log("Companies:", data);

        setCompanies(data);
      } catch (error) {
        console.error("Error fetching companies:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchCompanies();
  }, []);

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

      {loading ? (
        <h2>Loading Companies...</h2>
      ) : (
        <CompanyTable companies={companies} />
      )}
    </Layout>
  );
}

export default Companies;