import type { ResearchResponse } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function researchCompany(
  companyInput: string
): Promise<ResearchResponse> {
  const response = await fetch(`${API_BASE_URL}/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      company_input: companyInput,
    }),
  });

  if (!response.ok) {
    let message = "Research request failed. Please try again.";

    try {
      const errorBody = await response.json();
      const detail =
        typeof errorBody.detail === "string"
          ? errorBody.detail
          : JSON.stringify(errorBody.detail);

      if (
        detail.includes("rate_limit_exceeded") ||
        detail.includes("Rate limit")
      ) {
        message =
          "The free AI model limit has been reached. Please try again after a few minutes.";
      } else {
        message = detail || message;
      }
    } catch {
      // keep default message
    }

    throw new Error(message);
  }

  return response.json();
}