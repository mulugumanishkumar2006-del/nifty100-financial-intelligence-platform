import { Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Companies from "./pages/Companies";
import CompanyDetails from "./pages/CompanyDetails";
import Analytics from "./pages/Analytics";
import FinancialRatios from "./pages/FinancialRatios";
import StockPrices from "./pages/StockPrices";


function App() {

  return (

    <Routes>

      {/* Dashboard */}
      <Route
        path="/"
        element={<Dashboard />}
      />


      {/* Companies List */}
      <Route
        path="/companies"
        element={<Companies />}
      />


      {/* Single Company Details */}
      <Route
        path="/company/:id"
        element={<CompanyDetails />}
      />


      {/* Analytics */}
      <Route
        path="/analytics"
        element={<Analytics />}
      />


      {/* Financial Ratios */}
      <Route
        path="/financial-ratios"
        element={<FinancialRatios />}
      />


      {/* Stock Prices */}
      <Route
        path="/stock-prices"
        element={<StockPrices />}
      />


      {/* Unknown Routes */}
      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>

  );

}


export default App;