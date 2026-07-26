import "./RevenueRanking.css";

function RevenueRanking({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="ranking-card">
        <h2>Top Revenue Companies</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="ranking-card">
      <h2>🏆 Top Revenue Companies</h2>

      <table className="ranking-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Company</th>
            <th>Revenue</th>
          </tr>
        </thead>

        <tbody>
          {data.map((company, index) => (
            <tr key={index}>
              <td>#{index + 1}</td>

              <td>{company.company_name}</td>

              <td>
                ₹{" "}
                {Number(company.sales).toLocaleString(
                  "en-IN",
                  {
                    maximumFractionDigits: 0,
                  }
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RevenueRanking;