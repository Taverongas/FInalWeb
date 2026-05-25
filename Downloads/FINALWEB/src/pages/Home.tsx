import { useState, useEffect } from 'react'
import SearchBar from '../components/SearchBar'
import DragonList from '../components/DragonList'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'
import EmptyState from '../components/EmptyState'
import { fetchDragons } from '../services/DragonService'

export default function Home() {
  const [dragons, setDragons] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')

  
  useEffect(() => {
    async function cargar() {
      try {
        const datos = await fetchDragons()
        setDragons(datos)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    cargar()
  }, [])

  
  const filtrados = dragons.filter((d) =>
    d.name.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <Loader />
  if (error) return <ErrorMessage message={error} />

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">DragonDex</h1>
      <SearchBar onSearch={setSearch} />
      {filtrados.length === 0 ? (
        <EmptyState />
      ) : (
        <DragonList dragons={filtrados} />
      )}
    </div>
  )
}