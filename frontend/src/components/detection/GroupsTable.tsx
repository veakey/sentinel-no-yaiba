interface GroupData {
  group: string
  detectedThreats: number
}

const groupsData: GroupData[] = [
  { group: 'EDR Postes', detectedThreats: 14 },
  { group: 'EDR Serveurs', detectedThreats: 2 },
  { group: 'Default', detectedThreats: 1 },
]

export default function GroupsTable() {
  // Fill remaining rows to 10
  const displayData = [
    ...groupsData,
    ...Array(10 - groupsData.length).fill({ group: '-', detectedThreats: '-' }),
  ]

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/10">
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">Group</th>
            <th className="text-right py-3 px-4 text-sm font-semibold text-white/80">
              Number of detected threats
            </th>
          </tr>
        </thead>
        <tbody>
          {displayData.map((row, index) => (
            <tr key={index} className="border-b border-white/5 hover:bg-white/5">
              <td className="py-3 px-4 text-sm text-white/90">{row.group}</td>
              <td className="py-3 px-4 text-sm text-white/90 text-right">
                {row.detectedThreats}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

