import { useState } from "react";
import { BrowserRouter, NavLink, Navigate, Route, Routes } from "react-router-dom";
import { getSessionUser, logoutUser } from "./auth";
import AboutPage from "./pages/AboutPage";
import HomePage from "./pages/HomePage";
import InsightsPage from "./pages/InsightsPage";
import LoginPage from "./pages/LoginPage";
import PredictPage from "./pages/PredictPage";
import SignupPage from "./pages/SignupPage";

function ProtectedRoute({ isAuthenticated, children }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  const [sessionUser, setSessionUser] = useState(getSessionUser());

  const handleLogout = () => {
    logoutUser();
    setSessionUser(null);
  };

  return (
    <BrowserRouter>
      <div className="page">
        <header className="topbar">
          <div className="brand">Crop Advisor</div>
          <nav className="navlinks">
            {sessionUser ? (
              <>
                <NavLink to="/" end>
                  Home
                </NavLink>
                <NavLink to="/predict">Predict</NavLink>
                <NavLink to="/insights">Insights</NavLink>
                <NavLink to="/about">About</NavLink>
              </>
            ) : null}
            {!sessionUser ? <NavLink to="/login">Login</NavLink> : null}
            {!sessionUser ? <NavLink to="/signup">Sign Up</NavLink> : null}
            {sessionUser ? (
              <button className="nav-logout" onClick={handleLogout} type="button">
                Logout
              </button>
            ) : null}
          </nav>
        </header>

        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute isAuthenticated={!!sessionUser}>
                <HomePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/predict"
            element={
              <ProtectedRoute isAuthenticated={!!sessionUser}>
                <PredictPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/insights"
            element={
              <ProtectedRoute isAuthenticated={!!sessionUser}>
                <InsightsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/about"
            element={
              <ProtectedRoute isAuthenticated={!!sessionUser}>
                <AboutPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/login"
            element={
              sessionUser ? <Navigate to="/" replace /> : <LoginPage onAuthChange={setSessionUser} />
            }
          />
          <Route
            path="/signup"
            element={
              sessionUser ? <Navigate to="/" replace /> : <SignupPage onAuthChange={setSessionUser} />
            }
          />
          <Route path="*" element={<Navigate to={sessionUser ? "/" : "/login"} replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
