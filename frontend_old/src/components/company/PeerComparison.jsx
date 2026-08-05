import { useEffect, useState } from "react";
import { getPeerComparison } from "../../services/companyService";

function PeerComparison({ company }) {
  const [peers, setPeers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPeers() {
      if (!company?.id) return;

      try {
        const data = await getPeerComparison(company.id);
        setPeers(data || []);
      } catch (err) {
        console.error("Peer Comparison Error:", err);
        setPeers([]);
      } finally {
        setLoading(false);
      }
    }

    loadPeers();
  }, [company]);

  return (
    <div
      style={{
        background: "#ffffff",
        marginTop: "30px",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
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

      {loading ? (
        <p>Loading peer companies...</p>
      ) : peers.length === 0 ? (
        <p>No peer companies found.</p>
      ) : (
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
                <th style={{ padding: "12px" }}>Company</th>
                <th>Market Cap</th>
                <th>ROE %</th>
                <th>ROCE %</th>
                <th>Sector</th>
              </tr>
            </thead>

            <tbody>
              {peers.map((peer) => (
                <tr
                  key={peer.id}
                  style={{
                    borderBottom: "1px solid #e5e7eb",
                  }}
                >
                  <td style={{ padding: "12px" }}>
                    {peer.company_name}
                  </td>

                  <td>
                    ₹
                    {peer.market_cap
                      ? Number(peer.market_cap).toLocaleString()
                      : "-"}
                  </td>

                  <td>
                    {peer.roe_percentage ?? "-"}%
                  </td>

                  <td>
                    {peer.roce_percentage ?? "-"}%
                  </td>

                  <td>
                    {peer.broad_sector ?? "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default PeerComparison;