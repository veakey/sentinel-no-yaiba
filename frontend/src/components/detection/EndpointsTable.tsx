interface EndpointData {
  endpoint: string
  detectedThreats: number
}

const endpointsData: EndpointData[] = [
  { endpoint: 'MGD-PCD026593.labo.labomgd.ch', detectedThreats: 5 },
  { endpoint: 'MGD-PCL026631.labo.labomgd.ch', detectedThreats: 4 },
  { endpoint: 'MGD-PCL026678', detectedThreats: 2 },
  { endpoint: 'MGDLAB2.labo.labomgd.ch', detectedThreats: 2 },
  { endpoint: 'MGD-PCL026506.labo.labomgd.ch', detectedThreats: 1 },
  { endpoint: 'MGD-PCL026740.labo.labomgd.ch', detectedThreats: 1 },
  { endpoint: 'MGD-PCD026588.labo.labomgd.ch', detectedThreats: 1 },
  { endpoint: 'MGD-PCL026760', detectedThreats: 1 },
]

export default function EndpointsTable() {
  // Fill remaining rows to 10
  const displayData = [
    ...endpointsData,
    ...Array(10 - endpointsData.length).fill({ endpoint: '-', detectedThreats: '-' }),
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

