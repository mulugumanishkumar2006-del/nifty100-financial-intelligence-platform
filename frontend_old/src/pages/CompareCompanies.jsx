import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import { getCompanies } from "../services/companyService";

function CompareCompanies() {
  const [companies, setCompanies] = useState([]);

  const [company1, setCompany1] = useState("");
  const [company2, setCompany2] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await getCompanies();
        setCompanies(data || []);
      } catch (error) {
        console.error(error);
      }
    }

    loadCompanies();
  }, []);

  const first = useMemo(
    () => companies.find((c) => String(c.id) === company1),
    [companies, company1]
  );

  const second = useMemo(
    () => companies.find((c) => String(c.id) === company2),
    [companies, company2]
  );

  return (
    <Layout>
      <h1>⚖ Company Comparison</h1>

      <p>
        Compare two companies across important financial metrics.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginTop: "25px",
        }}
      >
        <select
          value={company1}
          onChange={(e) => setCompany1(e.target.value)}
        >
          <option value="">Select Company 1</option>

          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.company_name}
            </option>
          ))}
        </select>

        <select
          value={company2}
          onChange={(e) => setCompany2(e.target.value)}
        >
          <option value="">Select Company 2</option>

          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.company_name}
            </option>
          ))}
        </select>
      </div>

      {first && second && (
        <table
          style={{
            width: "100%",
            marginTop: "40px",
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
              <th style={{ padding: "12px" }}>Metric</th>
              <th>{first.company_name}</th>
              <th>{second.company_name}</th>
            </tr>
          </thead>

          <tbody>
            <Row
              title="Sector"
              value1={first.sector}
              value2={second.sector}
            />

            <Row
              title="ROE %"
              value1={first.roe_percentage}
              value2={second.roe_percentage}
            />

            <Row
              title="ROCE %"
              value1={first.roce_percentage}
              value2={second.roce_percentage}
            />

            <Row
              title="P/E Ratio"
              value1={first.pe_ratio}
              value2={second.pe_ratio}
            />

            <Row
              title="Book Value"
              value1={first.book_value}
              value2={second.book_value}
            />

            <Row
              title="Face Value"
              value1={first.face_value}
              value2={second.face_value}
            />

            <Row
              title="EPS"
              value1={first.eps}
              value2={second.eps}
            />

            <Row
              title="Market Cap"
              value1={first.market_cap}
              value2={second.market_cap}
            />
          </tbody>
        </table>
      )}
    </Layout>
  );
}

function Row({ title, value1, value2 }) {
  return (
    <tr style={{ borderBottom: "1px solid #ddd" }}>
      <td style={{ padding: "12px", fontWeight: 600 }}>{title}</td>
      <td style={{ padding: "12px" }}>{value1 ?? "-"}</td>
      <td style={{ padding: "12px" }}>{value2 ?? "-"}</td>
    </tr>
  );
}

export default CompareCompanies;