function CompanyHeader({ company }) {
  return (
    <div
      style={{
        background: "linear-gradient(135deg,#2563eb,#1d4ed8)",
        color: "white",
        padding: "35px",
        borderRadius: "18px",
        marginBottom: "30px",
        boxShadow: "0 12px 30px rgba(37,99,235,0.25)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        <div>
          <h1
            style={{
              fontSize: "36px",
              marginBottom: "8px",
            }}
          >
            🏢 {company.company_name}
          </h1>

          <p
            style={{
              opacity: 0.9,
            }}
          >
            Company ID : {company.id}
          </p>

          {company.website && (
            <a
              href={company.website}
              target="_blank"
              rel="noreferrer"
              style={{
                color: "#ffffff",
                textDecoration: "underline",
              }}
            >
              🌐 Visit Website
            </a>
          )}
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2,160px)",
            gap: "15px",
            marginTop: "20px",
          }}
        >
          <Metric title="Book Value" value={company.book_value} />

          <Metric title="Face Value" value={company.face_value} />

          <Metric title="ROE %" value={company.roe_percentage} />

          <Metric title="ROCE %" value={company.roce_percentage} />
        </div>
      </div>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.15)",
        borderRadius: "12px",
        padding: "15px",
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontSize: "13px",
          opacity: 0.9,
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontSize: "24px",
          fontWeight: "700",
          marginTop: "8px",
        }}
      >
        {value ?? "-"}
      </div>
    </div>
  );
}

export default CompanyHeader;