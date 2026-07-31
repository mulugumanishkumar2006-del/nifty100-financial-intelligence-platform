import { Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Companies from "./pages/Companies";
import CompanyDetails from "./pages/CompanyDetails";
import Analytics from "./pages/Analytics";
import FinancialRatios from "./pages/FinancialRatios";
import StockPrices from "./pages/StockPrices";
import StockScreener from "./pages/StockScreener";
import CompareCompanies from "./pages/CompareCompanies";
import Intelligence from "./pages/Intelligence";

function App() {
  return (
    <Routes>
      {/* Dashboard */}
      <Route
        path="/"
        element={<Dashboard />}
      />

      {/* Companies */}
      <Route
        path="/companies"
        element={<Companies />}
      />

      {/* Company Details */}
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

      {/* Stock Screener */}
      <Route
        path="/stock-screener"
        element={<StockScreener />}
      />

      {/* Compare Companies */}
      <Route
        path="/compare"
        element={<CompareCompanies />}
      />

      {/* AI Intelligence */}
      <Route
        path="/intelligence"
        element={<Intelligence />}
      />

      {/* 404 Redirect */}
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