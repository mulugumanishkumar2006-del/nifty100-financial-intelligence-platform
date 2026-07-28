import { NavLink } from "react-router-dom";
import { FaSearchDollar } from "react-icons/fa";
import {
  FaChartLine,
  FaBuilding,
  FaChartBar,
  FaPercentage,
  FaDatabase,
} from "react-icons/fa";
import { FaBalanceScale } from "react-icons/fa";

function Sidebar() {


  const menuStyle = ({ isActive }) => ({
    display: "flex",
    alignItems: "center",
    gap: "12px",

    padding: "14px 18px",

    marginBottom: "12px",

    borderRadius: "12px",

    textDecoration: "none",

    color: isActive
      ? "#ffffff"
      : "#cbd5e1",

    background: isActive
      ? "linear-gradient(135deg,#2563eb,#1d4ed8)"
      : "transparent",

    fontWeight: "600",

    fontSize: "15px",

    transition: "all 0.3s ease",

    boxShadow: isActive
      ? "0 8px 20px rgba(37,99,235,0.35)"
      : "none",
  });



  return (

    <aside

      style={{

        width:"260px",

        minHeight:"100vh",

        background:"#0f172a",

        color:"#ffffff",

        padding:"25px",

        display:"flex",

        flexDirection:"column",

        boxSizing:"border-box",

      }}

    >



      {/* Logo */}

      <div

        style={{

          textAlign:"center",

          marginBottom:"40px",

        }}

      >

        <h2

          style={{

            margin:0,

            color:"#60a5fa",

            fontSize:"24px",

          }}

        >

          📈 NIFTY100

        </h2>


        <p

          style={{

            color:"#94a3b8",

            fontSize:"13px",

            marginTop:"8px",

          }}

        >

          Financial Intelligence

        </p>


      </div>





      {/* Menu */}


      <nav>


        <NavLink

          to="/"

          style={menuStyle}

        >

          <FaChartLine />

          Dashboard

        </NavLink>




        <NavLink

          to="/companies"

          style={menuStyle}

        >

          <FaBuilding />

          Companies

        </NavLink>





        <NavLink

          to="/analytics"

          style={menuStyle}

        >

          <FaChartBar />

          Analytics

        </NavLink>





        <NavLink

          to="/financial-ratios"

          style={menuStyle}

        >

          <FaPercentage />

          Financial Ratios

        </NavLink>





        <NavLink

          to="/stock-prices"

          style={menuStyle}

        >

          <FaDatabase />

          Stock Prices

        </NavLink>


      </nav>


      <NavLink
  to="/stock-screener"
  style={menuStyle}
>
  <FaSearchDollar />
  Stock Screener
</NavLink>
<NavLink
  to="/compare"
  style={menuStyle}
>
  <FaBalanceScale />
  Compare
</NavLink>

      {/* Footer */}


      <div

        style={{

          marginTop:"auto",

          textAlign:"center",

          color:"#64748b",

          fontSize:"12px",

          paddingTop:"30px",

        }}

      >

        Version 1.0

        <br/>

        Bluestock FinTech Internship


      </div>



    </aside>


  );

}


export default Sidebar;