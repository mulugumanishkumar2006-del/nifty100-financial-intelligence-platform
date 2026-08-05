import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// ======================================================
// Compare Companies
// ======================================================

export const compareCompanies = async (
  company1,
  company2
) => {
  try {
    const { data } = await axios.get(
      `${API}/comparison`,
      {
        params: {
          company1,
          company2,
        },
      }
    );

    return data;
  } catch (err) {
    console.error(
      "Comparison Error:",
      err
    );

    return [];
  }
};