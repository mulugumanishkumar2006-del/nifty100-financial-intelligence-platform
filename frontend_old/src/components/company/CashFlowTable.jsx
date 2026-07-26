function CashFlowTable({data}){


if(!data || data.length===0){

return <p>No Cash Flow Data</p>

}


return (

<div className="card">


<h2>💰 Cash Flow</h2>


<table>


<thead>

<tr>

<th>Year</th>
<th>Operating</th>
<th>Investing</th>
<th>Financing</th>

</tr>

</thead>



<tbody>


{
data.map((item,index)=>(


<tr key={index}>

<td>{item.year}</td>

<td>{item.operating_cash_flow}</td>

<td>{item.investing_cash_flow}</td>

<td>{item.financing_cash_flow}</td>


</tr>


))

}


</tbody>


</table>


</div>


)


}


export default CashFlowTable;