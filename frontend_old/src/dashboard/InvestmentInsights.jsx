function InvestmentInsights({dashboard}){


    let insight =
        "Market analysis available";



    if(
        dashboard?.average_roe > 15 &&
        dashboard?.average_roce > 15
    ){

        insight =
        "Strong profitability and capital efficiency";

    }


    else if(
        dashboard?.average_roe < 10
    ){

        insight =
        "Low average return indicators";

    }



    return(


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
                💡 Investment Insights
            </h2>


            <p
                style={{
                    fontSize:"18px"
                }}
            >
                {insight}
            </p>


        </div>


    );


}



export default InvestmentInsights;