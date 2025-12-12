import { useDetectionStore } from '@/store/detectionStore'

interface GroupData {
  group: string
  detectedThreats: number
}

export default function GroupsTable() {
  const { data } = useDetectionStore()
  
  // Count threats per group
  const threats = data?.threats || []
  const groups = data?.groups || []
  const groupCounts: Record<string, number> = {}
  
  threats.forEach((threat: any) => {
    const groupId = threat.group_id || threat.group?.id
    const group = groups.find((g: any) => g.id === groupId)
    const groupName = group?.name || threat.group?.name || 'Unknown'
    groupCounts[groupName] = (groupCounts[groupName] || 0) + 1
  })
  
  const groupsData: GroupData[] = Object.entries(groupCounts)
    .map(([group, detectedThreats]) => ({
      group,
      detectedThreats: detectedThreats as number,
    }))
    .sort((a, b) => b.detectedThreats - a.detectedThreats)
    .slice(0, 10) // Top 10
  
  // Fill remaining rows to 10 if needed
  const displayData = [
    ...groupsData,
    ...Array(Math.max(0, 10 - groupsData.length)).fill({ group: '-', detectedThreats: '-' }),
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

