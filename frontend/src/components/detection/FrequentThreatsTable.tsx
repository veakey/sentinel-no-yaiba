interface FrequentThreatData {
  threatName: string
  detectionCount: number
  type: string
}

const frequentThreatsData: FrequentThreatData[] = [
  { threatName: 'Riskware', detectionCount: 5, type: 'Outbound Co...' },
  { threatName: 'Malware.Ransom.Agent.Generic', detectionCount: 5, type: 'File' },
  { threatName: 'Phishing', detectionCount: 2, type: 'Outbound Co...' },
  { threatName: 'Pup.Optional.Simplytech', detectionCount: 2, type: 'File' },
  { threatName: 'Fraud', detectionCount: 2, type: 'Outbound Co...' },
  { threatName: 'Trojan', detectionCount: 1, type: 'Outbound Co...' },
]

export default function FrequentThreatsTable() {
  // Fill remaining rows to 10
  const displayData = [
    ...frequentThreatsData,
    ...Array(10 - frequentThreatsData.length).fill({
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

