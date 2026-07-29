import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// Get all stock prices
export async function getStockPrices() {
  const response = await axios.get(`${API}/stock-prices`);
  return response.data;
}

// Latest prices
export async function getLatestStockPrices(limit = 100) {
  const response = await axios.get(
    `${API}/stock-prices?limit=${limit}`
  );

  return response.data;
}

// Company history
export async function getCompanyHistory(id) {
  const response = await axios.get(
    `${API}/stock-prices/company/${id}`
  );

  return response.data;
}

// Latest price of company
export async function getLatestPrice(id) {
  const response = await axios.get(
    `${API}/stock-prices/latest/${id}`
  );

  return response.data;
}

// Total records
export async function getTotalStockRecords() {
  const response = await axios.get(
    `${API}/stock-prices/stats/count`
  );

  return response.data;
}