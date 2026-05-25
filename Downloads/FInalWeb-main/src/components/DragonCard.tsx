import { Link } from 'react-router-dom'
import { useFavorites } from '../context/FavoritesContext'

export default function DragonCard({ dragon }: any) {
  const { isFavorite, addFavorite, removeFavorite } = useFavorites()
  const esFavorito = isFavorite(dragon.name)

  function toggleFavorito() {
    if (esFavorito) {
      removeFavorite(dragon.name)
    } else {
      addFavorite(dragon)
    }
  }

  return (
    <div className="bg-white p-4 rounded shadow text-center">
      <Link to={`/dragon/${dragon.name}`}>
        <h3 className="font-bold capitalize text-lg">{dragon.name}</h3>
      </Link>
      <button onClick={toggleFavorito} className="mt-2 text-2xl">
        {esFavorito ? "❤️" : "🤍"}
      </button>
    </div>
  )
}