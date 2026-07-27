function MarketOverview({ dashboard }) {


    return (

        <div
            style={{
                background:"#ffffff",
                padding:"25px",
                borderRadius:"15px",
                marginTop:"40px",
                boxShadow:
                "0 8px 20px rgba(0,0,0,0.08)"
            }}
        >


            <h2
                style={{
                    color:"#2563eb"
                }}
            >
                📊 Market Overview
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



                <OverviewCard
                    title="Listed Companies"
                    value={
                        dashboard?.companies ?? "-"
                    }
                />



                <OverviewCard
                    title="Total Revenue"
                    value={
                        dashboard
                        ?
                        `₹ ${Number(
                            dashboard.total_revenue
                        ).toLocaleString("en-IN")}`
                        :
                        "-"
                    }
                />



                <OverviewCard
                    title="Total Profit"
                    value={
                        dashboard
                        ?
                        `₹ ${Number(
                            dashboard.total_profit
                        ).toLocaleString("en-IN")}`
                        :
                        "-"
                    }
                />



                <OverviewCard
                    title="Market Sectors"
                    value={
                        dashboard?.total_sectors ?? "-"
                    }
                />


            </div>


        </div>

    );

}





function OverviewCard({
    title,
    value
}){


    return(

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



export default MarketOverview;