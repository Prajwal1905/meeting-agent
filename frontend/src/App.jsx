import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Upload from './pages/Upload'
import Results from './pages/Results'
import Search from './pages/Search'

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar />
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/results/:meetingId" element={<Results />} />
        <Route path="/search" element={<Search />} />
      </Routes>
    </div>
  )
}

export default App