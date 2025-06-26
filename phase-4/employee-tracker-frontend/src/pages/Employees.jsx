import Layout from '../components/Layout'

export default function Employees() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4">👤 Welcome, {user.name || 'Employee'}</h2>
      <p className="text-gray-700">This is your personal dashboard.</p>
    </Layout>
  )
}

