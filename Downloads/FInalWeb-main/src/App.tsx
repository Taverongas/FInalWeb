import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import DragonDetail from './pages/DragonDetail'
import Favorites from './pages/Favorites'

function App() {
  return (
    <div>
      <nav className="bg-gray-800 text-white p-4 flex gap-4">
        <Link to="/">Inicio</Link>
        <Link to="/favorites">Favoritos</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dragon/:name" element={<DragonDetail />} />
        <Route path="/favorites" element={<Favorites />} />
      </Routes>
    </div>
  )
}

export default App