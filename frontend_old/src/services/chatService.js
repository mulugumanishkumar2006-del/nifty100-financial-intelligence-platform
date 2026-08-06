import axios from "axios";

const API = "http://127.0.0.1:8000/api/chat";

// ==========================================================
// Ask AI
// ==========================================================

export const askAI = async (question) => {
  try {
    const response = await axios.post(`${API}/`, {
      question,
    });

    return response.data;
  } catch (error) {
    console.error("AI Chat Error:", error);
    throw error;
  }
};