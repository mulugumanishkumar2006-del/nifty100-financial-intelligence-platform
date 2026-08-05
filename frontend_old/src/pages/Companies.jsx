import { useEffect, useState } from "react";

import Layout from "../components/Layout";
import CompanyTable from "../components/CompanyTable";
import CompanyFilters from "../components/company/CompanyFilters";

import { getCompanies } from "../services/companyService";

function Companies() {
  const [companies, setCompanies] = useState([]);
  const [filteredCompanies, setFilteredCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const data = await getCompanies();

        console.log("Companies:", data);

        const companyList = data || [];
        setCompanies(companyList);
        setFilteredCompanies(companyList);
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
      {/* ================= PAGE HEADER ================= */}

      <div
        style={{
          marginBottom: "30px",
        }}
      >
        <h1
          style={{
            fontSize: "34px",
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
            marginBottom: "25px",
          }}
        >
          Browse, search and analyze all companies available in the NIFTY100
          Financial Intelligence Platform.
        </p>

        {/* Filters and Search Component */}
        <CompanyFilters
          companies={companies}
          onFilter={setFilteredCompanies}
        />

        {/* Statistics */}

        <div
          style={{
            display: "flex",
            gap: "20px",
            flexWrap: "wrap",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              padding: "15px 22px",
              borderRadius: "10px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
            }}
          >
            <h3
              style={{
                margin: 0,
                color: "#2563eb",
              }}
            >
              {companies.length}
            </h3>

            <p
              style={{
                margin: 0,
                color: "#6b7280",
              }}
            >
              Total Companies
            </p>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "15px 22px",
              borderRadius: "10px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
            }}
          >
            <h3
              style={{
                margin: 0,
                color: "#16a34a",
              }}
            >
              {filteredCompanies.length}
            </h3>

            <p
              style={{
                margin: 0,
                color: "#6b7280",
              }}
            >
              Search Results
            </p>
          </div>
        </div>
      </div>

      {/* ================= TABLE ================= */}

      {loading ? (
        <h2>Loading Companies...</h2>
      ) : (
        <CompanyTable companies={filteredCompanies} />
      )}
    </Layout>
  );
}

export default Companies;