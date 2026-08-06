import { Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Companies from "./pages/Companies";
import CompanyDetails from "./pages/CompanyDetails";
import Analytics from "./pages/Analytics";
import FinancialRatios from "./pages/FinancialRatios";
import StockPrices from "./pages/StockPrices";
import StockScreener from "./pages/StockScreener";
import CompanyComparisonPage from "./pages/CompanyComparisonPage";
import Intelligence from "./pages/Intelligence";
import AIInsights from "./pages/AIInsights";
import Portfolio from "./pages/Portfolio";

function App() {
  return (
    <Routes>

      {/* ================= Dashboard ================= */}

      <Route
        path="/"
        element={<Dashboard />}
      />

      {/* ================= Companies ================= */}

      <Route
        path="/companies"
        element={<Companies />}
      />

      {/* ================= Company Details ================= */}

      <Route
        path="/company/:id"
        element={<CompanyDetails />}
      />

      {/* ================= Analytics ================= */}

      <Route
        path="/analytics"
        element={<Analytics />}
      />

      {/* ================= Financial Ratios ================= */}

      <Route
        path="/financial-ratios"
        element={<FinancialRatios />}
      />

      {/* ================= Stock Prices ================= */}

      <Route
        path="/stock-prices"
        element={<StockPrices />}
      />

      {/* ================= Stock Screener ================= */}

      <Route
        path="/stock-screener"
        element={<StockScreener />}
      />

      {/* ================= Company Comparison ================= */}

      <Route
        path="/comparison"
        element={<CompanyComparisonPage />}
      />

      {/* ================= AI Intelligence ================= */}

      <Route
        path="/intelligence"
        element={<Intelligence />}
      />

      {/* ================= AI Insights (Day 22) ================= */}

      <Route
        path="/ai-insights"
        element={<AIInsights />}
      />

      {/* ================= Portfolio ================= */}

      <Route
        path="/portfolio"
        element={<Portfolio />}
      />

      {/* ================= 404 ================= */}

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