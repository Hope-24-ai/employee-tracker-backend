import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import EmployeeHome from "./pages/EmployeeHome";
import ProtectedRoute from "./components/protectedRoute";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Public route for login */}
        <Route path="/" element={<Login />} />

        {/* Protected route for admin */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Protected route for employee */}
        <Route
          path="/employee-home"
          element={
            <ProtectedRoute allowedRoles={["employee"]}>
              <EmployeeHome />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}
