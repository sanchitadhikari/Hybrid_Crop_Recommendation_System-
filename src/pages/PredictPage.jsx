import { useMemo, useState } from "react";
import { predictCrop } from "../api";

const fields = [
  { key: "N", label: "Nitrogen (N)", min: 0, max: 200, step: 0.1 },
  { key: "P", label: "Phosphorus (P)", min: 0, max: 200, step: 0.1 },
  { key: "K", label: "Potassium (K)", min: 0, max: 250, step: 0.1 },
  { key: "temperature", label: "Temperature (C)", min: -10, max: 60, step: 0.1 },
  { key: "humidity", label: "Humidity (%)", min: 0, max: 100, step: 0.1 },
  { key: "ph", label: "Soil pH", min: 0, max: 14, step: 0.1 },
  { key: "rainfall", label: "Rainfall (mm)", min: 0, max: 500, step: 0.1 },
];

const initialForm = {
  N: 90,
  P: 42,
  K: 43,
  temperature: 21,
  humidity: 82,
  ph: 6.5,
  rainfall: 203,
};

function PredictPage() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const validationMessage = useMemo(() => {
    if (form.ph < 4.5 || form.ph > 8.5) return "pH outside common comfort range (4.5-8.5).";
    if (form.humidity < 20) return "Low humidity may reduce prediction reliability.";
    return "Inputs are in a healthy range.";
  }, [form]);

  const onChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: Number(value) }));
  };

  const onPredict = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const pred = await predictCrop(form);
      setResult(pred);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="grid">
      <section className="card form-card">
        <h2>Field Inputs</h2>
        <form onSubmit={onPredict}>
          {fields.map((f) => (
            <label key={f.key}>
              <span>{f.label}</span>
              <input
                type="number"
                min={f.min}
                max={f.max}
                step={f.step}
                value={form[f.key]}
                onChange={(e) => onChange(f.key, e.target.value)}
                required
              />
            </label>
          ))}
          <p className="hint">{validationMessage}</p>
          <button type="submit" disabled={loading}>
            {loading ? "Running model..." : "Recommend Crop"}
          </button>
        </form>
        {error ? <p className="error">{error}</p> : null}
      </section>

      <section className="card result-card">
        <h2>Prediction</h2>
        {!result ? (
          <p className="muted">Submit inputs to view recommendation.</p>
        ) : (
          <>
            <div className="big-crop">{result.crop}</div>
            <div className="stats">
              <div>
                <span>Confidence</span>
                <strong>{result.confidence}%</strong>
              </div>
              <div>
                <span>Uncertainty</span>
                <strong>{result.uncertainty}</strong>
              </div>
            </div>
            <p className="hint">{result.validation_hint}</p>
          </>
        )}
      </section>
    </main>
  );
}

export default PredictPage;
