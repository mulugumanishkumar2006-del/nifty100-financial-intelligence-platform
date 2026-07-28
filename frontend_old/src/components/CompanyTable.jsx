import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

function CompanyTable({ companies = [] }) {
  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("All");
  const [currentPage, setCurrentPage] = useState(1);

  const [sortField, setSortField] = useState("company_name");
  const [ascending, setAscending] = useState(true);

  const rowsPerPage = 10;

  // =============================
  // Unique Sectors
  // =============================

  const sectors = useMemo(() => {
    const list = companies
      .map((company) => company.sector)
      .filter(Boolean);

    return ["All", ...new Set(list)];
  }, [companies]);

  // =============================
  // Sort
  // =============================

  function handleSort(field) {
    if (field === sortField) {
      setAscending(!ascending);
    } else {
      setSortField(field);
      setAscending(true);
    }
  }

  // =============================
  // Search + Filter + Sort
  // =============================

  const filteredCompanies = useMemo(() => {
    let result = [...companies];

    // Search
    result = result.filter((company) =>
      company.company_name
        ?.toLowerCase()
        .includes(search.toLowerCase())
    );

    // Sector
    if (sector !== "All") {
      result = result.filter(
        (company) => company.sector === sector
      );
    }

    // Sorting
    result.sort((a, b) => {
      const valueA = a[sortField] ?? "";
      const valueB = b[sortField] ?? "";

      if (
        typeof valueA === "number" &&
        typeof valueB === "number"
      ) {
        return ascending
          ? valueA - valueB
          : valueB - valueA;
      }

      return ascending
        ? String(valueA).localeCompare(String(valueB))
        : String(valueB).localeCompare(String(valueA));
    });

    return result;
  }, [
    companies,
    search,
    sector,
    sortField,
    ascending,
  ]);

  // =============================
  // Pagination
  // =============================

  const totalPages = Math.max(
    1,
    Math.ceil(filteredCompanies.length / rowsPerPage)
  );

  const paginatedCompanies = filteredCompanies.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  // =============================
  // UI
  // =============================

  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "15px",
        padding: "25px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
      }}
    >
      {/* Search + Filter */}

      <div
        style={{
          display: "flex",
          gap: "15px",
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
            minWidth: "250px",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
            fontSize: "15px",
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
            <option
              key={item}
              value={item}
            >
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
              color: "#ffffff",
            }}
          >
            <th
              style={headerStyle}
              onClick={() => handleSort("id")}
            >
              #
            </th>

            <th
              style={headerStyle}
              onClick={() =>
                handleSort("company_name")
              }
            >
              Company
            </th>

            <th style={headerStyle}>
              Website
            </th>

            <th
              style={headerStyle}
              onClick={() =>
                handleSort("book_value")
              }
            >
              Book Value
            </th>

            <th
              style={headerStyle}
              onClick={() =>
                handleSort("roe_percentage")
              }
            >
              ROE %
            </th>

            <th
              style={headerStyle}
              onClick={() =>
                handleSort("roce_percentage")
              }
            >
              ROCE %
            </th>

            <th style={headerStyle}>
              Action
            </th>
          </tr>
        </thead>

        <tbody>
          {paginatedCompanies.length === 0 ? (
            <tr>
              <td
                colSpan="7"
                style={{
                  padding: "30px",
                  textAlign: "center",
                }}
              >
                No Companies Found
              </td>
            </tr>
          ) : (
            paginatedCompanies.map((company) => (
              <tr
                key={company.id}
                style={{
                  borderBottom:
                    "1px solid #e5e7eb",
                  transition: "0.3s",
                }}
              >
                <td style={cellStyle}>
                  {company.id}
                </td>

                <td style={cellStyle}>
                  <strong>
                    {company.company_name}
                  </strong>
                </td>

                <td style={cellStyle}>
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

                <td style={cellStyle}>
                  {company.book_value ?? "-"}
                </td>

                <td style={cellStyle}>
                  {company.roe_percentage ?? "-"}
                </td>

                <td style={cellStyle}>
                  {company.roce_percentage ?? "-"}
                </td>

                <td style={cellStyle}>
                  <Link
                    to={`/company/${company.id}`}
                    style={{
                      background: "#2563eb",
                      color: "#fff",
                      padding:
                        "8px 14px",
                      borderRadius: "8px",
                      textDecoration: "none",
                      fontWeight: "600",
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
          gap: "20px",
          marginTop: "25px",
        }}
      >
        <button
          onClick={() =>
            setCurrentPage((page) =>
              Math.max(page - 1, 1)
            )
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
              Math.min(
                page + 1,
                totalPages
              )
            )
          }
          disabled={
            currentPage === totalPages
          }
        >
          Next ▶
        </button>
      </div>
    </div>
  );
}

const headerStyle = {
  padding: "15px",
  cursor: "pointer",
  textAlign: "left",
};

const cellStyle = {
  padding: "15px",
};

export default CompanyTable;