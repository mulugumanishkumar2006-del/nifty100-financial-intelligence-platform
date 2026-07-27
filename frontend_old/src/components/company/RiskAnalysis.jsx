function RiskAnalysis({ company }) {


  const profitLoss =
    company?.profit_loss || [];


  const balanceSheet =
    company?.balance_sheet || [];


  const cashFlow =
    company?.cash_flow || [];



  // ===============================
  // Debt Risk
  // ===============================

  let debtRisk = "Low";


  const latestBalance =
    balanceSheet[
      balanceSheet.length - 1
    ];


  if (
    latestBalance &&
    latestBalance.total_debt > 100000
  ) {

    debtRisk = "High";

  }
  else if (
    latestBalance &&
    latestBalance.total_debt > 50000
  ) {

    debtRisk = "Medium";

  }




  // ===============================
  // Profit Stability
  // ===============================

  let profitRisk = "Low";


  if(profitLoss.length > 1){


    const profits =
      profitLoss.map(
        item => item.net_profit
      );


    const negativeYears =
      profits.filter(
        p => p < 0
      ).length;



    if(negativeYears >= 2){

      profitRisk="High";

    }
    else if(negativeYears===1){

      profitRisk="Medium";

    }

  }




  // ===============================
  // Cash Flow Risk
  // ===============================


  let cashRisk="Low";


  const latestCashFlow =
    cashFlow[
      cashFlow.length-1
    ];


  if(
    latestCashFlow &&
    latestCashFlow.free_cash_flow < 0
  ){

    cashRisk="High";

  }





  // ===============================
  // Overall Risk
  // ===============================


  let riskGrade="LOW";


  const risks=[
    debtRisk,
    profitRisk,
    cashRisk
  ];


  const highRisk =
    risks.filter(
      r=>r==="High"
    ).length;



  const mediumRisk =
    risks.filter(
      r=>r==="Medium"
    ).length;



  if(highRisk>=2){

    riskGrade="HIGH";

  }
  else if(
    highRisk===1 ||
    mediumRisk>=2
  ){

    riskGrade="MEDIUM";

  }





  return (

    <div
      style={{
        background:"#ffffff",
        padding:"25px",
        borderRadius:"15px",
        marginTop:"30px",
        boxShadow:
        "0 8px 20px rgba(0,0,0,0.08)"
      }}
    >


      <h2
        style={{
          color:"#dc2626"
        }}
      >
        ⚠️ Risk Analysis
      </h2>



      <div
        style={{
          display:"grid",
          gridTemplateColumns:
          "repeat(auto-fit,minmax(220px,1fr))",
          gap:"20px",
          marginTop:"20px"
        }}
      >


        <RiskCard
          title="Debt Risk"
          value={debtRisk}
        />


        <RiskCard
          title="Profit Stability"
          value={profitRisk}
        />


        <RiskCard
          title="Cash Flow Risk"
          value={cashRisk}
        />


        <RiskCard
          title="Overall Risk"
          value={riskGrade}
        />


      </div>


    </div>

  );

}





function RiskCard({
  title,
  value
}){


  let color="#16a34a";


  if(value==="Medium")
    color="#f59e0b";


  if(
    value==="High" ||
    value==="HIGH"
  )
    color="#dc2626";



  return(

    <div
      style={{
        background:"#f9fafb",
        padding:"20px",
        borderRadius:"12px",
        borderLeft:
        `6px solid ${color}`
      }}
    >


      <h3>
        {title}
      </h3>


      <h2
        style={{
          color:color
        }}
      >
        {value}
      </h2>


    </div>

  );

}


export default RiskAnalysis;