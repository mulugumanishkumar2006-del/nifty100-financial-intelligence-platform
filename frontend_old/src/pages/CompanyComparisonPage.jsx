import { useState } from "react";

import Layout from "../components/Layout";

import {
  getCompanies,
  compareCompanies,
} from "../services/companyService";

function CompanyComparisonPage() {

  const [companies, setCompanies] = useState([]);

  const [company1, setCompany1] = useState("");

  const [company2, setCompany2] = useState("");

  const [comparison, setComparison] = useState([]);

  useState(() => {
    async function loadCompanies() {
      const data = await getCompanies();
      setCompanies(data);
    }

    loadCompanies();
  }, []);

  async function handleCompare() {

    if (!company1 || !company2) return;

    const data = await compareCompanies(
      company1,
      company2
    );

    setComparison(data);
  }

  return (
    <Layout>

      <h1>📊 Company Comparison</h1>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "30px",
        }}
      >

        <select
          value={company1}
          onChange={(e) =>
            setCompany1(e.target.value)
          }
        >

          <option>Select Company 1</option>

          {companies.map((c) => (

            <option
              key={c.id}
              value={c.id}
            >
              {c.company_name}
            </option>

          ))}

        </select>

        <select
          value={company2}
          onChange={(e) =>
            setCompany2(e.target.value)
          }
        >

          <option>Select Company 2</option>

          {companies.map((c) => (

            <option
              key={c.id}
              value={c.id}
            >
              {c.company_name}
            </option>

          ))}

        </select>

        <button
          onClick={handleCompare}
        >
          Compare
        </button>

      </div>

      {comparison.length === 2 && (

        <table
          style={{
            marginTop: "40px",
            width: "100%",
            borderCollapse: "collapse",
          }}
        >

          <thead>

            <tr>

              <th>Metric</th>

              <th>{comparison[0].company_name}</th>

              <th>{comparison[1].company_name}</th>

            </tr>

          </thead>

          <tbody>

            <tr>

              <td>ROE</td>

              <td>{comparison[0].roe_percentage}</td>

              <td>{comparison[1].roe_percentage}</td>

            </tr>

            <tr>

              <td>ROCE</td>

              <td>{comparison[0].roce_percentage}</td>

              <td>{comparison[1].roce_percentage}</td>

            </tr>

            <tr>

              <td>Book Value</td>

              <td>{comparison[0].book_value}</td>

              <td>{comparison[1].book_value}</td>

            </tr>

            <tr>

              <td>Face Value</td>

              <td>{comparison[0].face_value}</td>

              <td>{comparison[1].face_value}</td>

            </tr>

            <tr>

              <td>Sector</td>

              <td>{comparison[0].broad_sector}</td>

              <td>{comparison[1].broad_sector}</td>

            </tr>

          </tbody>

        </table>

      )}

    </Layout>
  );
}

export default CompanyComparisonPage;