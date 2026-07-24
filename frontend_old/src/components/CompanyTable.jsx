import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

function CompanyTable() {
  const [companies] = useState([
    {
      id: 1,
      company_name: "Reliance Industries Ltd",
      symbol: "RELIANCE",
      sector: "Energy",
      website: "https://www.ril.com",
    },
    {
      id: 2,
      company_name: "Tata Consultancy Services",
      symbol: "TCS",
      sector: "Information Technology",
      website: "https://www.tcs.com",
    },
    {
      id: 3,
      company_name: "Infosys",
      symbol: "INFY",
      sector: "Information Technology",
      website: "https://www.infosys.com",
    },
    {
      id: 4,
      company_name: "HDFC Bank",
      symbol: "HDFCBANK",
      sector: "Financials",
      website: "https://www.hdfcbank.com",
    },
    {
      id: 5,
      company_name: "ICICI Bank",
      symbol: "ICICIBANK",
      sector: "Financials",
      website: "https://www.icicibank.com",
    },
    {
      id: 6,
      company_name: "Larsen & Toubro",
      symbol: "LT",
      sector: "Industrials",
      website: "https://www.larsentoubro.com",
    },
    {
      id: 7,
      company_name: "ITC",
      symbol: "ITC",
      sector: "Consumer Staples",
      website: "https://www.itcportal.com",
    },
    {
      id: 8,
      company_name: "Bharti Airtel",
      symbol: "BHARTIARTL",
      sector: "Communication Services",
      website: "https://www.airtel.in",
    },
    {
      id: 9,
      company_name: "Axis Bank",
      symbol: "AXISBANK",
      sector: "Financials",
      website: "https://www.axisbank.com",
    },
    {
      id: 10,
      company_name: "Asian Paints",
      symbol: "ASIANPAINT",
      sector: "Materials",
      website: "https://www.asianpaints.com",
    },
  ]);

  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("All");
  const [currentPage, setCurrentPage] = useState(1);

  const rowsPerPage = 5;

  const sectors = [
    "All",
    ...new Set(companies.map((company) => company.sector)),
  ];

  const filteredCompanies = useMemo(() => {
    return companies.filter((company) => {
      const matchesSearch = company.company_name
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesSector =
        sector === "All" || company.sector === sector;

      return matchesSearch && matchesSector;
    });
  }, [companies, search, sector]);

  const totalPages = Math.ceil(
    filteredCompanies.length / rowsPerPage
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
          placeholder="Search company..."
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
            <option key={item}>{item}</option>
          ))}
        </select>
      </div>

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
            <th>Symbol</th>
            <th>Sector</th>
            <th>Website</th>
            <th>Details</th>
          </tr>
        </thead>

        <tbody>
          {paginatedCompanies.map((company) => (
            <tr
              key={company.id}
              style={{
                borderBottom: "1px solid #e5e7eb",
              }}
            >
              <td style={{ padding: "12px" }}>{company.id}</td>

              <td>{company.company_name}</td>

              <td>{company.symbol}</td>

              <td>{company.sector}</td>

              <td>
                <a
                  href={company.website}
                  target="_blank"
                  rel="noreferrer"
                >
                  Visit
                </a>
              </td>

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
          ))}
        </tbody>
      </table>

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
          Previous
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
          Next
        </button>
      </div>
    </div>
  );
}

export default CompanyTable;