import { useDetectionStore } from '@/store/detectionStore'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { format, parseISO, startOfDay } from 'date-fns'

interface DayData {
  day: number
  month: string
  [category: string]: number | string
}

export default function DetectionsPerDayChart() {
  const { data } = useDetectionStore()
  
  const threats = data?.threats || []
  
  // Group threats by day and category
  const dailyCounts: Record<string, Record<string, number>> = {}
  const categories = new Set<string>()
  
  threats.forEach((threat: any) => {
    const detectedAt = threat.detected_at || threat.created_at || threat.timestamp
    if (!detectedAt) return
    
    try {
      const date = parseISO(detectedAt)
      const dayKey = format(startOfDay(date), 'yyyy-MM-dd')
      const category = threat.category || threat.threat_type || threat.type || 'Unknown'
      
      categories.add(category)
      
      if (!dailyCounts[dayKey]) {
        dailyCounts[dayKey] = {}
      }
      dailyCounts[dayKey][category] = (dailyCounts[dayKey][category] || 0) + 1
    } catch {
      // Skip invalid dates
    }
  })
  
  // Get last 30 days
  const last30Days = Array.from({ length: 30 }, (_, i) => {
    const date = new Date()
    date.setDate(date.getDate() - (29 - i))
    const day = date.getDate()
    const month = format(date, 'MMM')
    const dayKey = format(startOfDay(date), 'yyyy-MM-dd')
    const existing = dailyCounts[dayKey]
    
    const data: DayData = { day, month }
    categories.forEach(category => {
      data[category] = existing?.[category] || 0
    })
    return data
  })
  
  const fullData = last30Days
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={fullData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="day"
            tick={{ fill: 'rgba(255,255,255,0.7)' }}
            label={{ value: 'Day', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.7)' }}
          />
          <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
          />
          <Legend />
          {Array.from(categories).map((category, index) => {
            const colors = ['#1e40af', '#9333ea', '#06b6d4', '#ec4899', '#eab308', '#22c55e', '#6b7280']
            return (
              <Bar key={category} dataKey={category} stackId="a" fill={colors[index % colors.length]} radius={[0, 0, 0, 0]} />
            )
          })}
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-4 mt-4 justify-center">
        {Array.from(categories).map((category, index) => {
          const colors = ['#1e40af', '#9333ea', '#06b6d4', '#ec4899', '#eab308', '#22c55e', '#6b7280']
          const total = fullData.reduce((sum, day) => sum + ((day[category] as number) || 0), 0)
          return (
            <div key={category} className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: colors[index % colors.length] }} />
              <span className="text-sm text-white/70">{category}: {total}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

