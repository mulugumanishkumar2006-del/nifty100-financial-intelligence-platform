function GrowthAnalysis({ company }) {


  const profitLoss =
    company?.profit_loss || [];



  if (profitLoss.length < 2) {

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

        <h2>
          📈 Growth Analysis
        </h2>

        <p>
          Not enough financial data
        </p>


      </div>

    );

  }



  const latest =
    profitLoss[profitLoss.length - 1];


  const previous =
    profitLoss[profitLoss.length - 2];



  function calculateGrowth(
    current,
    old
  ){

    if(!old || old===0)
      return 0;


    return (
      ((current-old)/old)*100
    ).toFixed(2);

  }



  const revenueGrowth =
    calculateGrowth(
      latest.sales,
      previous.sales
    );


  const profitGrowth =
    calculateGrowth(
      latest.net_profit,
      previous.net_profit
    );


  const epsGrowth =
    calculateGrowth(
      latest.eps,
      previous.eps
    );



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
          color:"#2563eb"
        }}
      >
        📈 Growth Analysis
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


        <GrowthCard
          title="Revenue Growth"
          value={`${revenueGrowth}%`}
        />


        <GrowthCard
          title="Profit Growth"
          value={`${profitGrowth}%`}
        />


        <GrowthCard
          title="EPS Growth"
          value={`${epsGrowth}%`}
        />


        <GrowthCard
          title="Latest Year"
          value={latest.year}
        />


      </div>


    </div>

  );

}




function GrowthCard({
  title,
  value
}) {


  return (

    <div
      style={{
        background:"#f8fafc",
        padding:"20px",
        borderRadius:"12px",
        borderLeft:
        "5px solid #2563eb"
      }}
    >

      <h3>
        {title}
      </h3>


      <h2
        style={{
          color:"#2563eb"
        }}
      >
        {value}
      </h2>


    </div>

  );

}


export default GrowthAnalysis;