import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import RatioOverview from "../components/financial/RatioOverview";
import { getFinancialRatios } from "../services/financialRatioService";

function FinancialRatios() {
  const [ratios, setRatios] = useState([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("roe_percentage");

  useEffect(() => {
    async function loadRatios() {
      try {
        const data = await getFinancialRatios();
        setRatios(data || []);
      } catch (error) {
        console.error("Financial Ratio Error:", error);
      } finally {
        setLoading(false);
      }
    }

    loadRatios();
  }, []);

  const filtered = useMemo(() => {
    return [...ratios]
      .filter((item) =>
        item.company_name
          ?.toLowerCase()
          .includes(search.toLowerCase())
      )
      .sort(
        (a, b) =>
          (Number(b[sortBy]) || 0) -
          (Number(a[sortBy]) || 0)
      );
  }, [ratios, search, sortBy]);

  const avgROE =
    filtered.length > 0
      ? (
          filtered.reduce(
            (sum, item) =>
              sum + Number(item.roe_percentage || 0),
            0
          ) / filtered.length
        ).toFixed(2)
      : 0;

  const avgROCE =
    filtered.length > 0
      ? (
          filtered.reduce(
            (sum, item) =>
              sum + Number(item.roce_percentage || 0),
            0
          ) / filtered.length
        ).toFixed(2)
      : 0;

  const highestEPS =
    filtered.length > 0
      ? Math.max(
          ...filtered.map((x) => Number(x.eps || 0))
        )
      : 0;

  if (loading) {
    return (
      <Layout>
        <h2>Loading Financial Ratios...</h2>
      </Layout>
    );
  }

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
          }}
        >
          📈 Financial Ratios Dashboard
        </h1>

        <p
          style={{
            color: "#6b7280",
          }}
        >
          Compare financial strength across all NIFTY100 companies.
        </p>
      </div>

      <RatioOverview ratios={filtered} />

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <StatCard
          title="Companies"
          value={filtered.length}
          color="#2563eb"
        />

        <StatCard
          title="Average ROE"
          value={`${avgROE}%`}
          color="#16a34a"
        />

        <StatCard
          title="Average ROCE"
          value={`${avgROCE}%`}
          color="#9333ea"
        />

        <StatCard
          title="Highest EPS"
          value={highestEPS}
          color="#dc2626"
        />
      </div>

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
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            minWidth: "250px",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
          }}
        />

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
          }}
        >
          <option value="roe_percentage">Sort by ROE</option>
          <option value="roce_percentage">Sort by ROCE</option>
          <option value="pe_ratio">Sort by P/E</option>
          <option value="eps">Sort by EPS</option>
          <option value="book_value">Sort by Book Value</option>
        </select>
      </div>

      <div
        style={{
          overflowX: "auto",
          background: "#ffffff",
          borderRadius: "15px",
          boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
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
                color: "white",
              }}
            >
              <th style={{ padding: "14px" }}>Company</th>
              <th>ROE</th>
              <th>ROCE</th>
              <th>P/E</th>
              <th>EPS</th>
              <th>Book Value</th>
            </tr>
          </thead>

          <tbody>
            {filtered.map((item) => (
              <tr
                key={item.id}
                style={{
                  borderBottom: "1px solid #eee",
                  textAlign: "center",
                }}
              >
                <td
                  style={{
                    padding: "14px",
                    fontWeight: "600",
                  }}
                >
                  {item.company_name}
                </td>

                <td style={{ color: "#16a34a" }}>
                  {item.roe_percentage ?? "-"}
                </td>

                <td style={{ color: "#2563eb" }}>
                  {item.roce_percentage ?? "-"}
                </td>

                <td>{item.pe_ratio ?? "-"}</td>

                <td style={{ color: "#9333ea" }}>
                  {item.eps ?? "-"}
                </td>

                <td>{item.book_value ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${color}`,
      }}
    >
      <h4
        style={{
          color: "#6b7280",
          marginBottom: "10px",
        }}
      >
        {title}
      </h4>

      <h2
        style={{
          color,
          margin: 0,
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default FinancialRatios;