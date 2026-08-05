import { useEffect, useState } from "react";
import {
  getCompaniesBySector,
  getCompanyRatios,
} from "../../services/companyService";

function PeerComparison({ company }) {
  const [peers, setPeers] = useState([]);

  useEffect(() => {
    async function loadPeers() {
      if (!company?.id || !company?.broad_sector) return;

      try {
        // Get companies in same sector
        const companies = await getCompaniesBySector(
          company.broad_sector
        );

        const peerData = [];

        for (const item of companies) {
          const ratios = await getCompanyRatios(item.id);

          peerData.push({
            company: item.company_name,
            roe:
              ratios?.[0]?.return_on_equity_pct ?? "-",
            assetTurnover:
              ratios?.[0]?.asset_turnover ?? "-",
            debt:
              ratios?.[0]?.debt_to_equity ?? "-",
            margin:
              ratios?.[0]?.net_profit_margin_pct ?? "-",
          });
        }

        setPeers(peerData);
      } catch (err) {
        console.error(err);
      }
    }

    loadPeers();
  }, [company]);

  if (peers.length === 0) {
    return (
      <div
        style={{
          background: "#ffffff",
          marginTop: "30px",
          padding: "25px",
          borderRadius: "15px",
          boxShadow:
            "0 8px 20px rgba(0,0,0,0.08)",
        }}
      >
        <h2>👥 Peer Comparison</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#ffffff",
        marginTop: "30px",
        padding: "25px",
        borderRadius: "15px",
        boxShadow:
          "0 8px 20px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "20px",
          color: "#2563eb",
        }}
      >
        👥 Peer Comparison
      </h2>

      <div
        style={{
          overflowX: "auto",
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
                color: "#fff",
              }}
            >
              <th style={{ padding: "12px" }}>
                Company
              </th>

              <th>ROE %</th>

              <th>Net Margin %</th>

              <th>Debt/Equity</th>

              <th>Asset Turnover</th>
            </tr>
          </thead>

          <tbody>
            {peers.map((peer, index) => (
              <tr
                key={index}
                style={{
                  borderBottom:
                    "1px solid #e5e7eb",
                }}
              >
                <td style={{ padding: "12px" }}>
                  {peer.company}
                </td>

                <td>{peer.roe}</td>

                <td>{peer.margin}</td>

                <td>{peer.debt}</td>

                <td>{peer.assetTurnover}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PeerComparison;