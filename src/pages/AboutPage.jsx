function AboutPage() {
  return (
    <main className="single-grid">
      <section className="card">
        <h2>About This Project</h2>
        <p>
          Hybrid Crop Advisor is an AI-assisted decision support system for precision
          farming. It analyzes soil nutrients and weather conditions to recommend the
          most suitable crop from 22 classes.
        </p>
        <p>
          The goal is to help reduce trial-and-error crop planning by providing faster,
          data-driven recommendations that can be reviewed with confidence and
          explainability insights.
        </p>

        <h3>How It Works</h3>
        <p>
          You provide 7 field signals: Nitrogen (N), Phosphorus (P), Potassium (K),
          temperature, humidity, pH, and rainfall. The backend applies preprocessing and
          feeds them into a trained hybrid stacking model to generate prediction outputs.
        </p>

        <h3>What You Get</h3>
        <ul>
          <li>Top crop recommendation for the given input conditions</li>
          <li>Confidence and uncertainty scores for better decision support</li>
          <li>Insights visuals including SHAP importance and EDA charts</li>
        </ul>

        <h3>Model and Tech Stack</h3>
        <ul>
          <li>Modeling: Stacking ensemble with tree/boosting-based learners</li>
          <li>API: FastAPI backend for prediction and insight endpoints</li>
          <li>Frontend: React multi-page application with protected access</li>
          <li>Explainability: SHAP-based global feature importance</li>
        </ul>

        <h3>Responsible Use</h3>
        <p>
          Recommendations should be used as decision support, not as the only source of
          truth. For best outcomes, combine model output with local agronomy knowledge,
          seasonal context, and soil testing reports.
        </p>
      </section>
    </main>
  );
}

export default AboutPage;
