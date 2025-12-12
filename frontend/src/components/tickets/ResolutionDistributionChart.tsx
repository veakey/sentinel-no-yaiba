import { useTranslation } from 'react-i18next'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface ResolutionData {
  timeframe: string
  percentage: number
  color: string
}

export default function ResolutionDistributionChart() {
  const { t } = useTranslation()

  const resolutionData: ResolutionData[] = [
    { timeframe: '0-5 heures', percentage: 39, color: '#22c55e' },
    { timeframe: '5-24 heures', percentage: 14, color: '#0ea5e9' },
    { timeframe: '1-7 jours', percentage: 25, color: '#eab308' },
    { timeframe: '7-30 jours', percentage: 14, color: '#f97316' },
    { timeframe: 'Plus de 30 jours', percentage: 8, color: '#ef4444' },
  ]

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-4">{t('tickets.ticketsResolutionDelay')}</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={resolutionData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="timeframe"
            tick={{ fill: 'rgba(255,255,255,0.7)' }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} domain={[0, 100]} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
            formatter={(value: number) => `${value}%`}
          />
          <Bar dataKey="percentage" radius={[8, 8, 0, 0]}>
            {resolutionData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

