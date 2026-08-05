import { useState, useEffect } from "react";

function CompanyFilters({
  companies,
  onFilter,
}) {

  const [search, setSearch] = useState("");

  const [sector, setSector] = useState("");

  const [sortBy, setSortBy] = useState("");

  useEffect(() => {

    let filtered = [...companies];

    // =============================
    // Search
    // =============================

    if (search !== "") {

      filtered = filtered.filter(company =>

        company.company_name
          ?.toLowerCase()
          .includes(search.toLowerCase())

      );

    }

    // =============================
    // Sector
    // =============================

    if (sector !== "") {

      filtered = filtered.filter(

        company =>
          company.broad_sector === sector

      );

    }

    // =============================
    // Sorting
    // =============================

    switch (sortBy) {

      case "market_cap":

        filtered.sort(
          (a, b) =>
            (b.market_cap || 0) -
            (a.market_cap || 0)
        );

        break;

      case "roe":

        filtered.sort(
          (a, b) =>
            (b.roe_percentage || 0) -
            (a.roe_percentage || 0)
        );

        break;

      case "roce":

        filtered.sort(
          (a, b) =>
            (b.roce_percentage || 0) -
            (a.roce_percentage || 0)
        );

        break;

      default:

        break;

    }

    onFilter(filtered);

  }, [

    companies,

    search,

    sector,

    sortBy

  ]);

  const sectors = [

    ...new Set(

      companies

        .map(

          company => company.broad_sector

        )

        .filter(Boolean)

    )

  ];

  return (

    <div

      style={{

        background:"#fff",

        padding:20,

        borderRadius:15,

        marginBottom:25,

        display:"flex",

        flexWrap:"wrap",

        gap:15,

        boxShadow:

          "0 8px 20px rgba(0,0,0,.08)"

      }}

    >

      <input

        placeholder="🔍 Search Company"

        value={search}

        onChange={(e)=>setSearch(e.target.value)}

        style={{

          flex:1,

          minWidth:250,

          padding:12,

          borderRadius:8,

          border:"1px solid #ddd"

        }}

      />

      <select

        value={sector}

        onChange={(e)=>setSector(e.target.value)}

      >

        <option value="">All Sectors</option>

        {sectors.map((sector)=>(
          <option

            key={sector}

            value={sector}

          >

            {sector}

          </option>
        ))}

      </select>

      <select

        value={sortBy}

        onChange={(e)=>setSortBy(e.target.value)}

      >

        <option value="">Sort By</option>

        <option value="market_cap">

          Market Cap

        </option>

        <option value="roe">

          ROE

        </option>

        <option value="roce">

          ROCE

        </option>

      </select>

    </div>

  );

}

export default CompanyFilters;