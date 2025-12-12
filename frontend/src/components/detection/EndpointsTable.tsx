import { useDetectionStore } from '@/store/detectionStore'

interface EndpointData {
  endpoint: string
  detectedThreats: number
}

export default function EndpointsTable() {
  const { data } = useDetectionStore()
  
  // Count threats per endpoint
  const threats = data?.threats || []
  const endpointCounts: Record<string, number> = {}
  
  threats.forEach((threat: any) => {
    const endpointId = threat.endpoint_id || threat.endpoint?.id || threat.endpoint_id
    const endpointName = threat.endpoint?.name || threat.endpoint_name || `Endpoint ${endpointId}` || 'Unknown'
    endpointCounts[endpointName] = (endpointCounts[endpointName] || 0) + 1
  })
  
  const endpointsData: EndpointData[] = Object.entries(endpointCounts)
    .map(([endpoint, detectedThreats]) => ({
      endpoint,
      detectedThreats: detectedThreats as number,
    }))
    .sort((a, b) => b.detectedThreats - a.detectedThreats)
    .slice(0, 10) // Top 10
  
  // Fill remaining rows to 10 if needed
  const displayData = [
    ...endpointsData,
    ...Array(Math.max(0, 10 - endpointsData.length)).fill({ endpoint: '-', detectedThreats: '-' }),
  ]

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/10">
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">Endpoint</th>
            <th className="text-right py-3 px-4 text-sm font-semibold text-white/80">
              Number of detected threats
            </th>
          </tr>
        </thead>
        <tbody>
          {displayData.map((row, index) => (
            <tr key={index} className="border-b border-white/5 hover:bg-white/5">
              <td className="py-3 px-4 text-sm text-white/90">{row.endpoint}</td>
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

