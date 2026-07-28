import { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import { getCompanies } from "../services/companyService";

function StockScreener() {
  const [companies, setCompanies] = useState([]);

  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");

  const [sector, setSector] = useState("All");

  const [minROE, setMinROE] = useState("");

  const [minROCE, setMinROCE] = useState("");

  const [maxPE, setMaxPE] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await getCompanies();
        setCompanies(data || []);
      } catch (err) {
        console.log(err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  const sectors = useMemo(() => {
    const list = companies
      .map((c) => c.sector)
      .filter(Boolean);

    return ["All", ...new Set(list)];
  }, [companies]);

  const filtered = useMemo(() => {
    return companies.filter((c) => {
      const searchMatch =
        c.company_name
          ?.toLowerCase()
          .includes(search.toLowerCase()) ?? false;

      const sectorMatch =
        sector === "All" || c.sector === sector;

      const roeMatch =
        minROE === "" ||
        Number(c.roe_percentage) >= Number(minROE);

      const roceMatch =
        minROCE === "" ||
        Number(c.roce_percentage) >= Number(minROCE);

      const peMatch =
        maxPE === "" ||
        Number(c.pe_ratio) <= Number(maxPE);

      return (
        searchMatch &&
        sectorMatch &&
        roeMatch &&
        roceMatch &&
        peMatch
      );
    });
  }, [
    companies,
    search,
    sector,
    minROE,
    minROCE,
    maxPE,
  ]);

  return (
    <Layout>

      <h1>📈 AI Stock Screener</h1>

      <p>
        Filter stocks using financial metrics.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: 15,
          marginTop: 25,
        }}
      >
        <input
          placeholder="Search Company"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={sector}
          onChange={(e) => setSector(e.target.value)}
        >
          {sectors.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>

        <input
          type="number"
          placeholder="Minimum ROE"
          value={minROE}
          onChange={(e) => setMinROE(e.target.value)}
        />

        <input
          type="number"
          placeholder="Minimum ROCE"
          value={minROCE}
          onChange={(e) => setMinROCE(e.target.value)}
        />

        <input
          type="number"
          placeholder="Maximum P/E"
          value={maxPE}
          onChange={(e) => setMaxPE(e.target.value)}
        />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(320px,1fr))",
          gap: 20,
          marginTop: 30,
        }}
      >
        {loading ? (
          <h2>Loading...</h2>
        ) : (
          filtered.map((company) => (
            <div
              key={company.id}
              style={{
                background: "#fff",
                borderRadius: 12,
                padding: 20,
                boxShadow:
                  "0 5px 15px rgba(0,0,0,0.08)",
              }}
            >
              <h3>{company.company_name}</h3>

              <p>
                <b>Sector:</b> {company.sector}
              </p>

              <p>
                <b>ROE:</b>{" "}
                {company.roe_percentage}
              </p>

              <p>
                <b>ROCE:</b>{" "}
                {company.roce_percentage}
              </p>

              <p>
                <b>P/E:</b>{" "}
                {company.pe_ratio}
              </p>

              <p>
                <b>Book Value:</b>{" "}
                {company.book_value}
              </p>
            </div>
          ))
        )}
      </div>

    </Layout>
  );
}

export default StockScreener;