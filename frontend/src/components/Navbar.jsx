import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-white">
          🧠 MeetingMind
        </Link>
        <div className="flex gap-6">
          <Link to="/" className="text-gray-400 hover:text-white transition">
            Upload
          </Link>
          <Link to="/search" className="text-gray-400 hover:text-white transition">
            Search
          </Link>
        </div>
      </div>
    </nav>
  )
}