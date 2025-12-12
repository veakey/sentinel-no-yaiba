import { useDetectionStore } from '@/store/detectionStore'

interface FrequentThreatData {
  threatName: string
  detectionCount: number
  type: string
}

export default function FrequentThreatsTable() {
  const { data } = useDetectionStore()
  
  // Count threats by name
  const threats = data?.threats || []
  const threatCounts: Record<string, { count: number; type: string }> = {}
  
  threats.forEach((threat: any) => {
    const threatName = threat.threat_name || threat.name || threat.threat_name || 'Unknown'
    const threatType = threat.type || threat.threat_type || threat.category || 'Unknown'
    if (!threatCounts[threatName]) {
      threatCounts[threatName] = { count: 0, type: threatType }
    }
    threatCounts[threatName].count += 1
  })
  
  const frequentThreatsData: FrequentThreatData[] = Object.entries(threatCounts)
    .map(([threatName, { count, type }]) => ({
      threatName,
      detectionCount: count,
      type: type.length > 15 ? type.substring(0, 15) + '...' : type,
    }))
    .sort((a, b) => b.detectionCount - a.detectionCount)
    .slice(0, 10) // Top 10
  
  // Fill remaining rows to 10 if needed
  const displayData = [
    ...frequentThreatsData,
    ...Array(Math.max(0, 10 - frequentThreatsData.length)).fill({
      threatName: '-',
      detectionCount: '-',
      type: '-',
    }),
  ]

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/10">
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">Threat name</th>
            <th className="text-right py-3 px-4 text-sm font-semibold text-white/80">
              Detection count
            </th>
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">Type</th>
          </tr>
        </thead>
        <tbody>
          {displayData.map((row, index) => (
            <tr key={index} className="border-b border-white/5 hover:bg-white/5">
              <td className="py-3 px-4 text-sm text-white/90">{row.threatName}</td>
              <td className="py-3 px-4 text-sm text-white/90 text-right">
                {row.detectionCount}
              </td>
              <td className="py-3 px-4 text-sm text-white/90">{row.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

