import { useParams } from "react-router-dom";
import Layout from "../components/Layout";

function CompanyDetails() {
  const { id } = useParams();

  return (
    <Layout>
      <div
        style={{
          background: "#ffffff",
          padding: "30px",
          borderRadius: "15px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
        }}
      >
        <h1
          style={{
            color: "#2563eb",
            marginBottom: "10px",
          }}
        >
          🏢 Company Details
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "30px",
          }}
        >
          Detailed financial information for the selected company.
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
            gap: "20px",
          }}
        >
          <div
            style={{
              background: "#f9fafb",
              padding: "20px",
              borderRadius: "10px",
            }}
          >
            <h3>Company ID</h3>
            <p
              style={{
                fontSize: "22px",
                fontWeight: "bold",
                color: "#2563eb",
              }}
            >
              {id}
            </p>
          </div>

          <div
            style={{
              background: "#f9fafb",
              padding: "20px",
              borderRadius: "10px",
            }}
          >
            <h3>Company Name</h3>
            <p>Loading...</p>
          </div>

          <div
            style={{
              background: "#f9fafb",
              padding: "20px",
              borderRadius: "10px",
            }}
          >
            <h3>Sector</h3>
            <p>Loading...</p>
          </div>

          <div
            style={{
              background: "#f9fafb",
              padding: "20px",
              borderRadius: "10px",
            }}
          >
            <h3>Website</h3>
            <p>Loading...</p>
          </div>
        </div>

        <div
          style={{
            marginTop: "40px",
            background: "#f9fafb",
            padding: "25px",
            borderRadius: "10px",
          }}
        >
          <h2>📈 Financial Overview</h2>

          <table
            style={{
              width: "100%",
              marginTop: "20px",
              borderCollapse: "collapse",
            }}
          >
            <tbody>
              <tr>
                <td><strong>Market Cap</strong></td>
                <td>Loading...</td>
              </tr>

              <tr>
                <td><strong>Sales</strong></td>
                <td>Loading...</td>
              </tr>

              <tr>
                <td><strong>Net Profit</strong></td>
                <td>Loading...</td>
              </tr>

              <tr>
                <td><strong>ROE</strong></td>
                <td>Loading...</td>
              </tr>

              <tr>
                <td><strong>ROCE</strong></td>
                <td>Loading...</td>
              </tr>

              <tr>
                <td><strong>P/E Ratio</strong></td>
                <td>Loading...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}

export default CompanyDetails;