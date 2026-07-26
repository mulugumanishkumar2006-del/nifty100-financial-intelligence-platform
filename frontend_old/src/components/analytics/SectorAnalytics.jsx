import "./RevenueRanking.css";

function SectorAnalytics({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="ranking-card">
        <h2>Sector Analytics</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="ranking-card">
      <h2>🏭 Sector Performance</h2>

      <table className="ranking-table">
        <thead>
          <tr>
            <th>Sector</th>
            <th>Companies</th>
          </tr>
        </thead>

        <tbody>
          {data.map((sector, index) => (
            <tr key={index}>
              <td>{sector.broad_sector}</td>

              <td>{sector.companies}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SectorAnalytics;