// src/pages/Dashboard.jsx 
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

export default function Dashboard() {
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate("/");
    }
  }, []);

  function handleLogout() {
    localStorage.removeItem("user");
    navigate("/");
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Welcome, {user?.name}!</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
        >
          Logout
        </button>
      </div>
      {/* Add more dashboard content here */}
    </div>
  );
}



