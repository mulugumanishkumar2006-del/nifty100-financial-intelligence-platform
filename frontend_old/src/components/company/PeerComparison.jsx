function PeerComparison() {
  const peers = [
    {
      company: "Reliance Industries",
      marketCap: "₹18.5 L Cr",
      roe: "9.8%",
      roce: "10.5%",
    },
    {
      company: "ONGC",
      marketCap: "₹3.4 L Cr",
      roe: "18.2%",
      roce: "19.6%",
    },
    {
      company: "IOC",
      marketCap: "₹2.7 L Cr",
      roe: "15.7%",
      roce: "17.4%",
    },
    {
      company: "BPCL",
      marketCap: "₹1.4 L Cr",
      roe: "21.4%",
      roce: "24.8%",
    },
  ];

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
            <th style={{ padding: "12px" }}>Company</th>
            <th>Market Cap</th>
            <th>ROE</th>
            <th>ROCE</th>
          </tr>
        </thead>

        <tbody>
          {peers.map((peer, index) => (
            <tr
              key={index}
              style={{
                borderBottom: "1px solid #e5e7eb",
              }}
            >
              <td style={{ padding: "12px" }}>
                {peer.company}
              </td>

              <td>{peer.marketCap}</td>

              <td>{peer.roe}</td>

              <td>{peer.roce}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PeerComparison;