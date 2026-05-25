import DragonCard from './DragonCard'

export default function DragonList({ dragons }: any) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {dragons.map((dragon: any) => (
        <DragonCard key={dragon.name} dragon={dragon} />
      ))}
    </div>
  )
}