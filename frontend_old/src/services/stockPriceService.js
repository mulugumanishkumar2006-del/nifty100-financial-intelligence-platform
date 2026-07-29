import axios from "axios";

const API = "http://127.0.0.1:8000";

/*
-----------------------------------------
Get All Stock Prices
-----------------------------------------
*/

export async function getStockPrices() {
  const response = await axios.get(`${API}/stock-prices`);
  return response.data;
}

/*
-----------------------------------------
Latest Stock Prices
-----------------------------------------
*/

export async function getLatestStockPrices() {
  const response = await axios.get(
    `${API}/stock-prices/latest`
  );
  return response.data;
}

/*
-----------------------------------------
Top Gainers
-----------------------------------------
*/

export async function getTopGainers() {
  const response = await axios.get(
    `${API}/stock-prices/top-gainers`
  );
  return response.data;
}

/*
-----------------------------------------
Top Losers
-----------------------------------------
*/

export async function getTopLosers() {
  const response = await axios.get(
    `${API}/stock-prices/top-losers`
  );
  return response.data;
}

/*
-----------------------------------------
Highest Volume
-----------------------------------------
*/

export async function getHighestVolume() {
  const response = await axios.get(
    `${API}/stock-prices/highest-volume`
  );
  return response.data;
}