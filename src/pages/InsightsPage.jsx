import { useEffect, useState } from "react";
import {
  getCorrelationHeatmapUrl,
  getCropDistributionImageUrl,
  getShapGlobal,
  getShapImageUrl,
} from "../api";

function InsightsPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        const data = await getShapGlobal();
        if (mounted) setItems(data.items || []);
      } catch (err) {
        if (mounted) setError(err.message || "Failed to load SHAP data.");
      } finally {
        if (mounted) setLoading(false);
      }
    }

    load();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <main className="single-grid">
      <section className="card">
        <h2>Global SHAP Feature Importance</h2>
        <p className="muted">Higher value means stronger impact on model predictions.</p>

        <div className="insight-gallery">
          <figure className="insight-image-wrap">
            <img
              src={getShapImageUrl()}
              alt="Global SHAP feature importance chart"
              className="insight-image"
              loading="lazy"
            />
            <figcaption>Global SHAP Importance</figcaption>
          </figure>

          <figure className="insight-image-wrap">
            <img
              src={getCorrelationHeatmapUrl()}
              alt="Feature correlation heatmap"
              className="insight-image"
              loading="lazy"
            />
            <figcaption>Feature Correlation Heatmap</figcaption>
          </figure>

          <figure className="insight-image-wrap">
            <img
              src={getCropDistributionImageUrl()}
              alt="Crop class distribution chart"
              className="insight-image"
              loading="lazy"
            />
            <figcaption>Crop Distribution (EDA)</figcaption>
          </figure>
        </div>

        {loading ? <p>Loading SHAP insights...</p> : null}
        {error ? <p className="error">{error}</p> : null}

        {!loading && !error ? (
          <ul className="shap-list">
            {items.map((item) => (
              <li key={item.feature}>
                <span>{item.feature}</span>
                <strong>{item.importance.toFixed(4)}</strong>
              </li>
            ))}
          </ul>
        ) : null}
      </section>
    </main>
  );
}

export default InsightsPage;
