export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-blue-600">Employee Tracker</h1>
      </header>
      <main>{children}</main>
    </div>
  )
}

