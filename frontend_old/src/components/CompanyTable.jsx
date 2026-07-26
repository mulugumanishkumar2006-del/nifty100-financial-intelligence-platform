import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

function CompanyTable({ companies = [] }) {
  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("All");
  const [currentPage, setCurrentPage] = useState(1);

  const rowsPerPage = 5;

  // Get unique sectors from backend data
  const sectors = useMemo(() => {
    const sectorList = companies
      .map((company) => company.sector)
      .filter(Boolean);

    return ["All", ...new Set(sectorList)];
  }, [companies]);

  // Search + Filter
  const filteredCompanies = useMemo(() => {
    return companies.filter((company) => {
      const matchesSearch =
        company.company_name
          ?.toLowerCase()
          .includes(search.toLowerCase()) || false;

      const matchesSector =
        sector === "All" || company.sector === sector;

      return matchesSearch && matchesSector;
    });
  }, [companies, search, sector]);

  // Pagination
  const totalPages = Math.max(
    1,
    Math.ceil(filteredCompanies.length / rowsPerPage)
  );

  const paginatedCompanies = filteredCompanies.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "15px",
        padding: "25px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
      }}
    >
      {/* Search + Filter */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginBottom: "25px",
          flexWrap: "wrap",
        }}
      >
        <input
          type="text"
          placeholder="🔍 Search Company..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setCurrentPage(1);
          }}
          style={{
            flex: 1,
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
          }}
        />

        <select
          value={sector}
          onChange={(e) => {
            setSector(e.target.value);
            setCurrentPage(1);
          }}
          style={{
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
          }}
        >
          {sectors.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      {/* Table */}

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr
            style={{
              background: "#2563eb",
              color: "white",
            }}
          >
            <th style={{ padding: "12px" }}>ID</th>
            <th>Company</th>
            <th>Website</th>
            <th>Book Value</th>
            <th>ROE %</th>
            <th>Details</th>
          </tr>
        </thead>

        <tbody>
          {paginatedCompanies.length === 0 ? (
            <tr>
              <td
                colSpan="6"
                style={{
                  textAlign: "center",
                  padding: "20px",
                }}
              >
                No companies found.
              </td>
            </tr>
          ) : (
            paginatedCompanies.map((company) => (
              <tr
                key={company.id}
                style={{
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <td style={{ padding: "12px" }}>{company.id}</td>

                <td>{company.company_name}</td>

                <td>
                  {company.website ? (
                    <a
                      href={company.website}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Visit
                    </a>
                  ) : (
                    "-"
                  )}
                </td>

                <td>{company.book_value ?? "-"}</td>

                <td>{company.roe_percentage ?? "-"}</td>

                <td>
                  <Link
                    to={`/company/${company.id}`}
                    style={{
                      background: "#2563eb",
                      color: "white",
                      padding: "8px 12px",
                      borderRadius: "6px",
                      textDecoration: "none",
                    }}
                  >
                    View
                  </Link>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {/* Pagination */}

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "15px",
          marginTop: "25px",
        }}
      >
        <button
          onClick={() =>
            setCurrentPage((page) => Math.max(page - 1, 1))
          }
          disabled={currentPage === 1}
        >
          ◀ Previous
        </button>

        <strong>
          Page {currentPage} of {totalPages}
        </strong>

        <button
          onClick={() =>
            setCurrentPage((page) =>
              Math.min(page + 1, totalPages)
            )
          }
          disabled={currentPage === totalPages}
        >
          Next ▶
        </button>
      </div>
    </div>
  );
}

export default CompanyTable;