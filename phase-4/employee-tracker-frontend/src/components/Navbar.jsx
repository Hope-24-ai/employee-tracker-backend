// src/components/Navbar.jsx
// src/components/Navbar.jsx
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Navbar() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="bg-white shadow-md px-6 py-4 flex justify-between items-center sticky top-0 z-50"
    >
      <h1 className="text-xl font-bold text-blue-600 tracking-wide">Employee Tracker</h1>

      {user?.email ? (
        <div className="flex items-center gap-4">
          <p className="text-sm text-gray-700 capitalize">
            {user.role} logged in
          </p>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleLogout}
            className="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-full shadow hover:shadow-lg transition-all duration-300"
          >
            Logout
          </motion.button>
        </div>
      ) : null}
    </motion.nav>
  );
}
