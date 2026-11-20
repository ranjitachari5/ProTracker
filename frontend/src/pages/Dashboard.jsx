
import { useEffect, useState } from 'react'
import { useAuth } from '../context/useAuth'
import { getDashboardStats } from '../services/dashboardService'

function Dashboard() {
  const { user, logout } = useAuth()

  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        const data = await getDashboardStats()
        setStats(data)
      } catch (err) {
        console.error('Dashboard error:', err)
        setError('Unable to load dashboard statistics.')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardStats()
  }, [])

  const statCards = [
    { title: 'Total Courses', value: stats?.total_courses ?? 0 },
    { title: 'Completed', value: stats?.completed_courses ?? 0 },
    { title: 'In Progress', value: stats?.in_progress_courses ?? 0 },
    { title: 'Not Started', value: stats?.not_started_courses ?? 0 },
  ]

  return (
    <div className="min-h-screen bg-slate-950 p-8 text-white">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">ProTracker Dashboard</h1>
          <p className="mt-2 text-slate-400">
            Welcome, {user.username}!
          </p>
        </div>

        <button
          onClick={logout}
          className="rounded-lg bg-red-600 px-5 py-2 font-semibold hover:bg-red-700"
        >
          Logout
        </button>
      </div>

      {loading && (
        <p className="mt-8 text-slate-400">
          Loading dashboard statistics...
        </p>
      )}

      {error && (
        <p className="mt-8 text-red-400">{error}</p>
      )}

      {!loading && !error && stats && (
        <>
          <div className="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {statCards.map((card) => (
              <div
                key={card.title}
                className="rounded-xl border border-slate-800 bg-slate-900 p-6"
              >
                <p className="text-sm text-slate-400">{card.title}</p>
                <p className="mt-3 text-3xl font-bold">{card.value}</p>
              </div>
            ))}
          </div>

          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-lg font-semibold">Overall Progress</h2>

            <p className="mt-3 text-4xl font-bold">
              {stats.overall_progress}%
            </p>

            <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-blue-500"
                style={{ width: `${stats.overall_progress}%` }}
              />
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard
