import { Link } from "react-router-dom";

function HomePage() {
  return (
    <main className="single-grid">
      <section className="card hero-card">
        <p className="eyebrow">Hybrid Uncertainty-Aware</p>
        <h1>Precision Crop Advisor</h1>
        <p>
          Use soil and climate inputs to receive a reliable crop recommendation with
          confidence and model uncertainty.
        </p>
        <div className="cta-row">
          <Link className="button-link" to="/predict">
            Start Prediction
          </Link>
          <Link className="button-ghost" to="/insights">
            View SHAP Insights
          </Link>
        </div>
      </section>

      <section className="card feature-grid">
        <article>
          <h3>Fast Prediction</h3>
          <p>Get recommendation instantly from a trained stacking model.</p>
        </article>
        <article>
          <h3>Uncertainty Score</h3>
          <p>Understand confidence before taking farming decisions.</p>
        </article>
        <article>
          <h3>Explainable AI</h3>
          <p>Review feature-level SHAP importance used by the model.</p>
        </article>
      </section>
    </main>
  );
}

export default HomePage;
