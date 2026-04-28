import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { DEMO_CREDENTIALS, loginUser } from "../auth";

function LoginPage({ onAuthChange }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      if (!email.trim() || !password.trim()) {
        throw new Error("Email and password are required.");
      }

      const user = loginUser({ email, password });
      onAuthChange(user);
      navigate("/predict");
    } catch (err) {
      setError(err.message || "Login failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="single-grid auth-wrap">
      <section className="card auth-card">
        <h2>Login</h2>
        <p className="muted">Access your crop recommendation dashboard.</p>
        <p className="hint">
          Demo login: {DEMO_CREDENTIALS.email} / {DEMO_CREDENTIALS.password}
        </p>
        <button
          type="button"
          onClick={() => {
            setEmail(DEMO_CREDENTIALS.email);
            setPassword(DEMO_CREDENTIALS.password);
          }}
        >
          Use Demo Credentials
        </button>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              required
            />
          </label>

          <label>
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </label>

          <button type="submit" disabled={submitting}>
            {submitting ? "Signing in..." : "Login"}
          </button>
        </form>

        {error ? <p className="error">{error}</p> : null}

        <p className="muted auth-alt">
          New user? <Link to="/signup">Create an account</Link>
        </p>
      </section>
    </main>
  );
}

export default LoginPage;
