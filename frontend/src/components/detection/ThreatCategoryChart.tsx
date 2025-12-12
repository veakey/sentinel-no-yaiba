import { useDetectionStore } from '@/store/detectionStore'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

interface ThreatCategoryData {
  category: string
  detections: number
  color: string
}

const COLORS = ['#1e40af', '#9333ea', '#06b6d4', '#ec4899', '#eab308', '#22c55e', '#6b7280']

export default function ThreatCategoryChart() {
  const { data } = useDetectionStore()
  
  // Group threats by category
  const threats = data?.threats || []
  const categoryCounts: Record<string, number> = {}
  
  threats.forEach((threat: any) => {
    const category = threat.category || threat.threat_type || threat.type || 'Unknown'
    categoryCounts[category] = (categoryCounts[category] || 0) + 1
  })
  
  const threatData: ThreatCategoryData[] = Object.entries(categoryCounts)
    .map(([category, detections], index) => ({
      category,
      detections: detections as number,
      color: COLORS[index % COLORS.length],
    }))
    .sort((a, b) => b.detections - a.detections) // Sort by detections descending
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={threatData.filter((d) => d.detections > 0)}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="category"
            tick={{ fill: 'rgba(255,255,255,0.7)' }}
            angle={-45}
            textAnchor="end"
            height={100}
          />
          <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} domain={[0, 10]} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey="detections" radius={[8, 8, 0, 0]}>
            {threatData
              .filter((d) => d.detections > 0)
              .map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-4 mt-4 justify-center">
        {threatData.map((item) => (
          <div key={item.category} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm text-white/70">{item.category}: {item.detections}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

