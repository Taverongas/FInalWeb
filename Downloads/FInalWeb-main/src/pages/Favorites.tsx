import { useFavorites } from '../context/FavoritesContext'
import DragonList from '../components/DragonList'
import EmptyState from '../components/EmptyState'

export default function Favorites() {
    const { favorites } = useFavorites()

    return (
        <div className="p-4">
            <h1 className="text-2xl mb-4">Mis Favoritos</h1>
            {favorites.length === 0 ? <EmptyState /> : <DragonList dragons={favorites} />}
        </div>
    )
}