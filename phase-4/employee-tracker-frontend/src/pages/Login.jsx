import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Login() {
  const { register, handleSubmit } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/login`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log("Login response:", result); // 👈 Added here to log backend response

      if (response.ok) {
        localStorage.setItem("user", JSON.stringify(result));
        toast.success(result.greeting || `Welcome ${result.name}!`);
        navigate(result.role === "admin" ? "/dashboard" : "/employee-home");
      } else {
        toast.error(result.error || "Login failed");
      }
    } catch (error) {
      toast.error("Server error. Please try again.");
      console.error("Login fetch error:", error); //  Added here to log network or parsing errors
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-300 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-10 space-y-6 transition-all duration-300">
        <h2 className="text-4xl font-extrabold text-center text-gray-800 tracking-tight">
          Sign In
        </h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              {...register("email")}
              type="email"
              required
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              {...register("password")}
              type="password"
              required
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-xl shadow-md transition-all duration-300"
          >
            Log In
          </button>
        </form>
        <p className="text-xs text-center text-gray-400 pt-4">
          &copy; {new Date().getFullYear()} Employee Tracker App
        </p>
      </div>
    </div>
  );
}

