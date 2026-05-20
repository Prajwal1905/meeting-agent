import { useLocation, useNavigate } from 'react-router-dom'

export default function Results() {
  const { state } = useLocation()
  const navigate = useNavigate()

  if (!state) {
    navigate('/')
    return null
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <button onClick={() => navigate('/')} className="text-gray-400 hover:text-white text-sm mb-8 transition">
        ← Back to Upload
      </button>

      <h1 className="text-3xl font-bold mb-8">Meeting Results</h1>

      <Section title="📋 Summary">
        <ul className="space-y-2">
          {state.summary.split('\n').filter(l => l.trim()).map((line, i) => (
            <li key={i} className="text-gray-300 text-sm leading-relaxed">{line.replace(/^-\s*/, '')}</li>
          ))}
        </ul>
      </Section>

      <Section title="✅ Action Items">
        {state.action_items.length === 0 ? (
          <p className="text-gray-500 text-sm">No action items found</p>
        ) : (
          <div className="space-y-3">
            {state.action_items.map((item, i) => (
              <div key={i} className="bg-gray-800 rounded-xl p-4">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-violet-400 font-medium text-sm">{item.person}</span>
                  <span className="text-gray-500 text-xs">{item.deadline}</span>
                </div>
                <p className="text-gray-300 text-sm">{item.task}</p>
              </div>
            ))}
          </div>
        )}
      </Section>

      <Section title="🏛️ Decisions">
        {state.decisions.length === 0 ? (
          <p className="text-gray-500 text-sm">No decisions found</p>
        ) : (
          <div className="space-y-3">
            {state.decisions.map((d, i) => (
              <div key={i} className="bg-gray-800 rounded-xl p-4">
                <p className="text-gray-300 text-sm">{d.decision}</p>
                <p className="text-gray-500 text-xs mt-1">by {d.made_by}</p>
              </div>
            ))}
          </div>
        )}
      </Section>

      <Section title="📧 Email Draft">
        <pre className="text-gray-300 text-sm whitespace-pre-wrap leading-relaxed font-sans">
          {state.email_draft}
        </pre>
      </Section>
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div className="mb-8">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        {children}
      </div>
    </div>
  )
}