import { useState } from 'react'
import axios from 'axios'

const API = 'http://127.0.0.1:8001'

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    setSearched(true)
    try {
      const res = await axios.post(`${API}/api/search`, { query })
      setResults(res.data.results)
    } catch (e) {
      setResults([])
    }
    setLoading(false)
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-16">
      <h1 className="text-3xl font-bold mb-2">Search Meetings</h1>
      <p className="text-gray-400 mb-8">Ask anything about your past meetings</p>

      <div className="flex gap-3 mb-8">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSearch()}
          placeholder="What was decided about the app theme?"
          className="flex-1 bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 text-sm outline-none focus:border-violet-500 transition"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-violet-600 hover:bg-violet-700 px-6 py-3 rounded-xl text-sm font-medium transition disabled:opacity-50"
        >
          {loading ? '...' : 'Search'}
        </button>
      </div>

      {searched && results.length === 0 && !loading && (
        <p className="text-gray-500 text-sm">No results found</p>
      )}

      <div className="space-y-4">
        {results.map((r, i) => (
          <div key={i} className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-violet-400 font-medium uppercase">{r.type}</span>
              <span className="text-xs text-gray-500">score: {r.score}</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">{r.text}</p>
            <p className="text-gray-600 text-xs mt-2">Meeting: {r.meeting_id}</p>
          </div>
        ))}
      </div>
    </div>
  )
}