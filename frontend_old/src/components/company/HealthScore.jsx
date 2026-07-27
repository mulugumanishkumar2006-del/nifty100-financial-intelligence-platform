function HealthScore({ company }) {


  const calculateScore = () => {

    let score = 0;


    if(company?.roe_percentage > 15)
      score += 25;


    if(company?.roce_percentage > 15)
      score += 25;


    if(company?.book_value > 100)
      score += 25;


    if(company?.net_profit > 0)
      score += 25;


    return score;

  };


  const score = calculateScore();



  return (

    <div
      style={{
        background:"#ffffff",
        padding:"25px",
        borderRadius:"15px",
        marginTop:"30px",
        boxShadow:"0 8px 20px rgba(0,0,0,0.08)"
      }}
    >

      <h2>
        ⭐ Financial Health Score
      </h2>


      <h1
        style={{
          color:
          score >=75
          ? "green"
          : score >=50
          ? "orange"
          : "red"
        }}
      >
        {score}/100
      </h1>


      <p>
        Based on profitability,
        efficiency and valuation metrics
      </p>


    </div>

  );

}


export default HealthScore;