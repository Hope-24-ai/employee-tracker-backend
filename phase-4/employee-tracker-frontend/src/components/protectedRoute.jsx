import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ allowedRoles, children }) {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  if (!user?.role || !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
