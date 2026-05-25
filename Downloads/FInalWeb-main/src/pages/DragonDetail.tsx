import { useParams, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { fetchDragonDetail } from '../services/DragonService'
import { useFavorites } from '../context/FavoritesContext'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'

export default function DragonDetail() {
  const { name } = useParams()
  const [dragon, setDragon] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { isFavorite, addFavorite, removeFavorite } = useFavorites()

  useEffect(() => {
    async function cargar() {
      try {
        const datos = await fetchDragonDetail(name!)
        setDragon(datos)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    cargar()
  }, [name])

  if (loading) return <Loader />
  if (error) return <ErrorMessage message={error} />
  if (!dragon) return null

  const esFavorito = isFavorite(dragon.name)

  function toggleFavorito() {
    if (esFavorito) {
      removeFavorite(dragon.name)
    } else {
      addFavorite({ name: dragon.name, url: '' })
    }
  }

  return (
    <div className="p-4">
      <Link to="/" className="text-yellow-400">← Volver</Link>

      <div className="text-center mt-4">
        <h1 className="text-3xl font-bold capitalize">{dragon.name}</h1>

        <img
          src={dragon.sprites?.front_default}
          alt={dragon.name}
          className="mx-auto w-48 h-48"
        />

        <button onClick={toggleFavorito} className="text-3xl mb-4">
          {esFavorito ? "❤️" : "🤍"}
        </button>

        <div className="mt-4">
          <p><strong>Altura:</strong> {dragon.height}</p>
          <p><strong>Peso:</strong> {dragon.weight}</p>
        </div>

        <div className="mt-4">
          <h2 className="font-bold">Tipos:</h2>
          <ul>
            {dragon.types?.map((t: any) => (
              <li key={t.type.name} className="capitalize">{t.type.name}</li>
            ))}
          </ul>
        </div>

        <div className="mt-4">
          <h2 className="font-bold">Estadísticas:</h2>
          <ul>
            {dragon.stats?.map((s: any) => (
              <li key={s.stat.name} className="capitalize">
                {s.stat.name}: {s.base_stat}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}