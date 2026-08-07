import axios from "axios";

// ======================================================
// Chart API Base URL
// ======================================================

const API = "http://127.0.0.1:8000/api/charts";

// ======================================================
// Revenue Trend
// GET /api/charts/revenue/{companyId}
// ======================================================

export const getRevenueTrend = async (companyId) => {
  try {
    if (!companyId) {
      console.warn("Revenue Trend: companyId is missing");
      return [];
    }

    const { data } = await axios.get(
      `${API}/revenue/${encodeURIComponent(companyId)}`
    );

    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error(
      `Revenue Trend Error for ${companyId}:`,
      err
    );

    return [];
  }
};

// ======================================================
// ROE Trend
// GET /api/charts/roe/{companyId}
// ======================================================

export const getROETrend = async (companyId) => {
  try {
    if (!companyId) {
      console.warn("ROE Trend: companyId is missing");
      return [];
    }

    const { data } = await axios.get(
      `${API}/roe/${encodeURIComponent(companyId)}`
    );

    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error(
      `ROE Trend Error for ${companyId}:`,
      err
    );

    return [];
  }
};

// ======================================================
// Market Cap
// GET /api/charts/market-cap
// ======================================================

export const getMarketCap = async () => {
  try {
    const { data } = await axios.get(
      `${API}/market-cap`
    );

    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Market Cap Error:", err);

    return [];
  }
};

// ======================================================
// Sector Distribution
// GET /api/charts/sector-distribution
// ======================================================

export const getSectorDistribution = async () => {
  try {
    const { data } = await axios.get(
      `${API}/sector-distribution`
    );

    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error(
      "Sector Distribution Error:",
      err
    );

    return [];
  }
};

// ======================================================
// Stock Price History
// GET /api/charts/stock-history/{companyId}
// ======================================================

export const getStockHistory = async (companyId) => {
  try {
    if (!companyId) {
      console.warn("Stock History: companyId is missing");
      return [];
    }

    const { data } = await axios.get(
      `${API}/stock-history/${encodeURIComponent(companyId)}`
    );

    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error(
      `Stock History Error for ${companyId}:`,
      err
    );

    return [];
  }
};

// ======================================================
// Load All Company Charts
// Optional helper for Dashboard
// ======================================================

export const getCompanyCharts = async (companyId) => {
  try {
    if (!companyId) {
      console.warn("Company Charts: companyId is missing");

      return {
        revenue: [],
        roe: [],
        stockHistory: [],
      };
    }

    const [
      revenue,
      roe,
      stockHistory,
    ] = await Promise.all([
      getRevenueTrend(companyId),
      getROETrend(companyId),
      getStockHistory(companyId),
    ]);

    return {
      revenue,
      roe,
      stockHistory,
    };
  } catch (err) {
    console.error(
      `Company Charts Error for ${companyId}:`,
      err
    );

    return {
      revenue: [],
      roe: [],
      stockHistory: [],
    };
  }
};

// ======================================================
// Load Dashboard Charts
// ======================================================

export const getDashboardCharts = async (
  companyId
) => {
  try {
    const [
      revenue,
      roe,
      marketCap,
      sectorDistribution,
      stockHistory,
    ] = await Promise.all([
      getRevenueTrend(companyId),
      getROETrend(companyId),
      getMarketCap(),
      getSectorDistribution(),
      getStockHistory(companyId),
    ]);

    return {
      revenue,
      roe,
      marketCap,
      sectorDistribution,
      stockHistory,
    };
  } catch (err) {
    console.error(
      "Dashboard Charts Error:",
      err
    );

    return {
      revenue: [],
      roe: [],
      marketCap: [],
      sectorDistribution: [],
      stockHistory: [],
    };
  }
};