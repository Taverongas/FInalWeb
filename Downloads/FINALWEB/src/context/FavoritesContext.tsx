import { createContext, useContext, useState } from 'react'

const FavoritesContext = createContext<any>(null)

export function FavoritesProvider({ children }: any) {
  const [favorites, setFavorites] = useState<any[]>([])

  
  function addFavorite(dragon: any) {

    const yaEsta = favorites.some((f) => f.name === dragon.name)
    if (yaEsta) return

    setFavorites([...favorites, dragon])
  }

  
  function removeFavorite(dragonName: string) {
    setFavorites(favorites.filter((f) => f.name !== dragonName))
  }

  
  function isFavorite(dragonName: string) {
    return favorites.some((f) => f.name === dragonName)
  }

  const value = {
    favorites,
    addFavorite,
    removeFavorite,
    isFavorite,
  }

  return (
    <FavoritesContext.Provider value={value}>
      {children}
    </FavoritesContext.Provider>
  )
}

export function useFavorites() {
  const context = useContext(FavoritesContext)
  if (!context) {
    throw new Error('useFavorites debe usarse dentro de FavoritesProvider')
  }
  return context
}