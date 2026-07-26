function ProfitLossTable({data}) {


if(!data || data.length===0){

return (

<div className="card">

<h2>📈 Profit & Loss</h2>

<p>No Data Available</p>

</div>

)

}


return (

<div className="card">


<h2>📈 Profit & Loss</h2>


<table>


<thead>

<tr>

<th>Year</th>

<th>Sales</th>

<th>Operating Profit</th>

<th>Net Profit</th>

<th>EPS</th>


</tr>

</thead>


<tbody>


{
data.map((item,index)=>(

<tr key={index}>

<td>{item.year}</td>

<td>{item.sales}</td>

<td>{item.operating_profit}</td>

<td>{item.net_profit}</td>

<td>{item.eps}</td>


</tr>

))

}


</tbody>


</table>


</div>


)

}


export default ProfitLossTable;