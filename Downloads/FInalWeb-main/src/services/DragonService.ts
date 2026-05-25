const API_URL = "https://pokeapi.co/api/v2"

// Trae la lista de dragones
export async function fetchDragons() {
  const respuesta = await fetch(`${API_URL}/type/dragon`)

  if (!respuesta.ok) {
    throw new Error("Error al cargar los dragones")
  }

  const datos = await respuesta.json()
  // datos.pokemon es un array de { pokemon: { name, url } }
  return datos.pokemon.map((p: any) => p.pokemon)
}

// Trae el detalle de un dragón por su nombre
export async function fetchDragonDetail(name: string) {
  const respuesta = await fetch(`${API_URL}/pokemon/${name}`)

  if (!respuesta.ok) {
    throw new Error("No se encontró el dragón")
  }

  return await respuesta.json()
}