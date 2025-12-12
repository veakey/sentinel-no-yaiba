import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface DayData {
  day: number
  month: string
  Website?: number
  Ransomware?: number
  PUP?: number
}

// Data from the image: October days 1,2,3,5,6,13 and November days 20,21,23,24,26
const dailyData: DayData[] = [
  { day: 1, month: 'Oct', Website: 1 },
  { day: 2, month: 'Oct', PUP: 1 },
  { day: 3, month: 'Oct', Website: 2 },
  { day: 5, month: 'Oct', PUP: 1 },
  { day: 6, month: 'Oct', Website: 2 },
  { day: 13, month: 'Oct', Website: 1 },
  { day: 20, month: 'Nov', Ransomware: 3 },
  { day: 21, month: 'Nov', Ransomware: 2 },
  { day: 23, month: 'Nov', Website: 1 },
  { day: 24, month: 'Nov', Website: 1 },
  { day: 26, month: 'Nov', Website: 2 },
]

// Fill all 30 days
const fullData: DayData[] = Array.from({ length: 30 }, (_, i) => {
  const day = i + 1
  const month = day <= 15 ? 'Oct' : 'Nov'
  const existing = dailyData.find((d) => d.day === day && d.month === month)
  return existing || { day, month }
})

export default function DetectionsPerDayChart() {
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
          <Bar dataKey="Website" stackId="a" fill="#1e40af" radius={[0, 0, 0, 0]} />
          <Bar dataKey="Ransomware" stackId="a" fill="#9333ea" radius={[0, 0, 0, 0]} />
          <Bar dataKey="PUP" stackId="a" fill="#06b6d4" radius={[0, 0, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-4 mt-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#1e40af]" />
          <span className="text-sm text-white/70">Website: 10</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#9333ea]" />
          <span className="text-sm text-white/70">Ransomware: 5</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#06b6d4]" />
          <span className="text-sm text-white/70">PUP: 2</span>
        </div>
      </div>
    </div>
  )
}

