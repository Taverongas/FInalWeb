export default function SearchBar({ onSearch }: any) {
  return (
    <input
      type="text"
      placeholder="Buscar dragón..."
      onChange={(e) => onSearch(e.target.value)}
      className="w-full p-2 border rounded mb-4"
    />
  )
}