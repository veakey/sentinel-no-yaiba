import { useTranslation } from 'react-i18next'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface OSData {
  name: string
  count: number
  color: string
}

export default function OSDistributionChart() {
  const { t } = useTranslation()

  const osData: OSData[] = [
    { name: 'Windows 10 Professional Edition', count: 13, color: '#06b6d4' },
    { name: 'Windows 11 Professional Edition', count: 13, color: '#9333ea' },
    { name: 'Unknown', count: 1, color: '#dc2626' },
    { name: 'VMware Photon OS/Linux', count: 1, color: '#0ea5e9' },
    { name: 'Windows 7 Professional Edition', count: 1, color: '#22c55e' },
  ]

  const total = osData.reduce((sum, item) => sum + item.count, 0)

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={osData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="name"
            tick={false}
            axisLine={false}
          />
          <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
          />
          <Bar dataKey="count" radius={[8, 8, 0, 0]}>
            {osData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-col gap-2 mt-4">
        <div className="text-sm text-white/70 mb-2">
          <span className="font-semibold">{t('tickets.total')}:</span> {total}
        </div>
        <div className="flex flex-wrap gap-4">
          {osData.map((item) => (
            <div key={item.name} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-sm text-white/70">
                {item.name}: {item.count}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

