function BalanceSheetTable({data}){


if(!data || data.length===0){

return <p>No Balance Sheet Data</p>

}


return (

<div className="card">


<h2>📊 Balance Sheet</h2>


<table>

<thead>

<tr>

<th>Year</th>
<th>Total Assets</th>
<th>Total Liabilities</th>
<th>Equity</th>

</tr>

</thead>


<tbody>


{
data.map((item,index)=>(

<tr key={index}>

<td>{item.year}</td>

<td>{item.total_assets}</td>

<td>{item.total_liabilities}</td>

<td>{item.equity_capital}</td>


</tr>


))

}


</tbody>


</table>


</div>


)

}


export default BalanceSheetTable;