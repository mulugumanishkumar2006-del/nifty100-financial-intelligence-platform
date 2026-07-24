const BASE_URL = "http://127.0.0.1:8000";

export async function getDashboard() {
  const response = await fetch(`${BASE_URL}/api/dashboard`);
  return await response.json();
}

export async function getLatestYear() {
  const response = await fetch(`${BASE_URL}/api/latest-year`);
  return await response.json();
}

export async function getTopRevenue() {
  const response = await fetch(`${BASE_URL}/api/top-revenue`);
  return await response.json();
}

export async function getTopProfit() {
  const response = await fetch(`${BASE_URL}/api/top-profit`);
  return await response.json();
}

export async function getSectorDistribution() {
  const response = await fetch(`${BASE_URL}/api/sector-distribution`);
  return await response.json();
}