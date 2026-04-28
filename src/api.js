const API_BASE_URL = "https://hybrid-crop-recommendation-system.onrender.com";;

export function getShapImageUrl() {
  return `${API_BASE_URL}/insights/shap-image`;
}

export function getCorrelationHeatmapUrl() {
  return `${API_BASE_URL}/insights/correlation-heatmap-image`;
}

export function getCropDistributionImageUrl() {
  return `${API_BASE_URL}/insights/crop-distribution-image`;
}

export async function predictCrop(payload) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ error: "Prediction failed" }));
    throw new Error(err.error || "Prediction failed");
  }

  return response.json();
}

export async function getShapGlobal() {
  const response = await fetch(`${API_BASE_URL}/shap/global`);
  if (!response.ok) {
    throw new Error("Unable to fetch SHAP global data");
  }
  return response.json();
}
