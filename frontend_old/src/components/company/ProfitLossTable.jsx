function ProfitLossTable({data}){


if(!data){

return(
<div>
<h2>📈 Profit & Loss</h2>
<p>No Data Available</p>
</div>
)

}


return(

<div className="financial-card">


<h2>📈 Profit & Loss</h2>


<p>
Sales :
{data.sales}
</p>


<p>
Operating Profit :
{data.operating_profit}
</p>


<p>
Net Profit :
{data.net_profit}
</p>


<p>
EPS :
{data.eps}
</p>


<p>
Dividend :
{data.dividend_payout}
</p>


</div>

)

}


export default ProfitLossTable;