import Navbar from "../components/Navbar";

export default function EmployeeHome() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  return (
    <div>
      <Navbar user={user} />
      <div className="p-6">
        <h2 className="text-2xl font-semibold">Welcome, Employee</h2>
        {/* Limited access content */}
      </div>
    </div>
  );
}
