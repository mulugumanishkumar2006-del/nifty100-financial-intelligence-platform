import axios from "axios";

// ==========================================================
// API Configuration
// ==========================================================

const API_BASE_URL = "http://127.0.0.1:8000/api";

// ==========================================================
// AI Chat Service
// ==========================================================

export const askAI = async (question) => {
  // Validate question
  if (!question || !question.trim()) {
    throw new Error("Question is required.");
  }

  try {
    const response = await axios.post(
      `${API_BASE_URL}/chat/`,
      {
        question: question.trim(),
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    console.log("AI Chat Response:", response.data);

    return response.data;
  } catch (error) {
    console.error("AI Chat Error:", error);

    // ======================================================
    // Backend returned an HTTP error
    // ======================================================

    if (error.response) {
      console.error(
        "Status:",
        error.response.status
      );

      console.error(
        "Backend Response:",
        error.response.data
      );

      const detail =
        error.response.data?.detail ||
        error.response.data?.error ||
        error.response.data?.message;

      throw new Error(
        detail ||
          `AI service returned an error (${error.response.status}).`
      );
    }

    // ======================================================
    // Request was sent but backend did not respond
    // ======================================================

    if (error.request) {
      console.error(
        "No response received from backend:",
        error.request
      );

      throw new Error(
        "Unable to connect to the backend API. Make sure FastAPI is running on http://127.0.0.1:8000."
      );
    }

    // ======================================================
    // Axios configuration / request error
    // ======================================================

    throw new Error(
      error.message ||
        "Unable to generate AI response."
    );
  }
};