import React from "react";

function CompanyComparison({ company }) {
  if (!company) return null;

  const metrics = [
    {
      title: "Market Cap",
      value: company.market_cap
        ? `₹${Number(company.market_cap).toLocaleString()} Cr`
        : "-",
      color: "#1d4ed8",
    },
    {
      title: "Sector",
      value: company.broad_sector || "-",
      color: "#0f766e",
    },
    {
      title: "Sub Sector",
      value: company.sub_sector || "-",
      color: "#0ea5e9",
    },
    {
      title: "Book Value",
      value: company.book_value ?? "-",
      color: "#2563eb",
    },
    {
      title: "Face Value",
      value: company.face_value ?? "-",
      color: "#ea580c",
    },
    {
      title: "ROE %",
      value:
        company.roe_percentage != null
          ? `${company.roe_percentage}%`
          : "-",
      color: "#16a34a",
    },
    {
      title: "ROCE %",
      value:
        company.roce_percentage != null
          ? `${company.roce_percentage}%`
          : "-",
      color: "#dc2626",
    },
    {
      title: "Website",
      value: company.website ? (
        <a
          href={company.website}
          target="_blank"
          rel="noreferrer"
          style={{
            color: "#2563eb",
            textDecoration: "none",
          }}
        >
          Visit
        </a>
      ) : (
        "-"
      ),
      color: "#7c3aed",
    },
  ];

  return (
    <div
      style={{
        marginTop: 35,
        background: "#ffffff",
        padding: 25,
        borderRadius: 15,
        boxShadow: "0 8px 20px rgba(0,0,0,.08)",
      }}
    >
      <h2
        style={{
          color: "#2563eb",
          marginBottom: 10,
        }}
      >
        📈 Company Snapshot
      </h2>

      <p
        style={{
          color: "#6b7280",
          marginBottom: 25,
        }}
      >
        Quick overview of the company's key financial indicators.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: 20,
        }}
      >
        {metrics.map((metric) => (
          <div
            key={metric.title}
            style={{
              background: "#f8fafc",
              padding: 20,
              borderRadius: 12,
              borderLeft: `6px solid ${metric.color}`,
              transition: "0.3s",
            }}
          >
            <h4
              style={{
                margin: 0,
                color: "#374151",
                fontSize: 15,
              }}
            >
              {metric.title}
            </h4>

            <div
              style={{
                marginTop: 12,
                fontSize: 22,
                fontWeight: "700",
                color: metric.color,
                wordBreak: "break-word",
              }}
            >
              {metric.value}
            </div>
          </div>
        ))}
      </div>

      {company.about_company && (
        <div
          style={{
            marginTop: 30,
            background: "#eff6ff",
            padding: 20,
            borderRadius: 12,
          }}
        >
          <h3
            style={{
              color: "#2563eb",
              marginBottom: 10,
            }}
          >
            About Company
          </h3>

          <p
            style={{
              lineHeight: 1.7,
              color: "#374151",
            }}
          >
            {company.about_company}
          </p>
        </div>
      )}
    </div>
  );
}

export default CompanyComparison;