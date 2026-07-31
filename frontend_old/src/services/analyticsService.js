// ==========================================
// Revenue Trend
// ==========================================

export const getRevenueTrend = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/analytics/revenue-trend/${companyId}`
    );

    return response.data;
  } catch (error) {
    console.error("Revenue Trend Error:", error);
    return [];
  }
};

// ==========================================
// Profit Trend
// ==========================================

export const getProfitTrend = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/analytics/profit-trend/${companyId}`
    );

    return response.data;
  } catch (error) {
    console.error("Profit Trend Error:", error);
    return [];
  }
};

// ==========================================
// Market Cap
// ==========================================

export const getMarketCap = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/companies/${companyId}`
    );

    return response.data;
  } catch (error) {
    console.error("Market Cap Error:", error);
    return null;
  }
};

// ==========================================
// Financial Ratios
// ==========================================

export const getFinancialRatios = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/financial-ratios/${companyId}`
    );

    return response.data;
  } catch (error) {
    console.error("Financial Ratios Error:", error);
    return null;
  }
};