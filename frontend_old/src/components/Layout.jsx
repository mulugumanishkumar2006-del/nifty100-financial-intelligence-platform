import Sidebar from "./Sidebar";


function Layout({children}) {


return (

<div

style={{

display:"flex",

minHeight:"100vh",

background:"#f8fafc"

}}

>


<Sidebar />



<main

className="fade-in"

style={{

flex:1,

padding:"30px",

overflowX:"hidden"

}}

>


{children}


</main>



</div>

);


}


export default Layout;