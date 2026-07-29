const API = "http://127.0.0.1:8000";

export async function getFinancialRatios() {
  const response = await fetch(
    `${API}/financial-ratios`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch financial ratios");
  }

  return response.json();
}