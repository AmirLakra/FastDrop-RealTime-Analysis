const apiBaseUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function buildQuery(filters = {}) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, value);
    }
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

export async function fetchDashboard(filters = {}) {
  const response = await fetch(`${apiBaseUrl}/api/dashboard${buildQuery(filters)}`);
  if (!response.ok) {
    throw new Error("Unable to load dashboard data.");
  }
  return response.json();
}

export async function fetchCities() {
  const response = await fetch(`${apiBaseUrl}/api/cities`);
  if (!response.ok) {
    throw new Error("Unable to load cities.");
  }
  return response.json();
}

