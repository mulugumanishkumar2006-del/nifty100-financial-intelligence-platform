import Layout from "../components/Layout";

function FinancialRatios() {
  const ratios = [
    {
      company: "Reliance",
      roe: "18.4%",
      roce: "20.5%",
      pe: "28.6",
      eps: "95.2",
      debt: "0.42",
    },
    {
      company: "TCS",
      roe: "45.3%",
      roce: "58.4%",
      pe: "32.7",
      eps: "118.5",
      debt: "0.02",
    },
    {
      company: "Infosys",
      roe: "31.8%",
      roce: "37.2%",
      pe: "29.4",
      eps: "67.8",
      debt: "0.01",
    },
    {
      company: "HDFC Bank",
      roe: "17.2%",
      roce: "18.8%",
      pe: "21.5",
      eps: "82.4",
      debt: "0.00",
    },
    {
      company: "ICICI Bank",
      roe: "19.6%",
      roce: "21.4%",
      pe: "19.2",
      eps: "53.1",
      debt: "0.00",
    },
  ];

  return (
    <Layout>
      <div>
        <h1
          style={{
            fontSize: "32px",
            fontWeight: "700",
            marginBottom: "10px",
          }}
        >
          📈 Financial Ratios
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "30px",
          }}
        >
          Compare important financial ratios across NIFTY100 companies.
        </p>

        <div
          style={{
            background: "#ffffff",
            borderRadius: "12px",
            padding: "25px",
            boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
          }}
        >
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
                <th style={{ padding: "12px" }}>Company</th>
                <th>ROE</th>
                <th>ROCE</th>
                <th>P/E</th>
                <th>EPS</th>
                <th>Debt/Equity</th>
              </tr>
            </thead>

            <tbody>
              {ratios.map((item, index) => (
                <tr
                  key={index}
                  style={{
                    borderBottom: "1px solid #e5e7eb",
                    textAlign: "center",
                  }}
                >
                  <td
                    style={{
                      padding: "12px",
                      fontWeight: "600",
                    }}
                  >
                    {item.company}
                  </td>

                  <td>{item.roe}</td>
                  <td>{item.roce}</td>
                  <td>{item.pe}</td>
                  <td>{item.eps}</td>
                  <td>{item.debt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div
          style={{
            marginTop: "30px",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
            gap: "20px",
          }}
        >
          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>Highest ROE</h3>
            <h2 style={{ color: "#16a34a" }}>TCS</h2>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>Highest ROCE</h3>
            <h2 style={{ color: "#2563eb" }}>TCS</h2>
          </div>

          <div
            style={{
              background: "#ffffff",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h3>Lowest Debt</h3>
            <h2 style={{ color: "#dc2626" }}>Infosys</h2>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default FinancialRatios;