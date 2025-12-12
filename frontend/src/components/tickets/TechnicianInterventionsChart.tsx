import { useTranslation } from 'react-i18next'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface InterventionData {
  count: string
  percentage: number
  color: string
}

export default function TechnicianInterventionsChart() {
  const { t } = useTranslation()

  const interventionData: InterventionData[] = [
    { count: '0', percentage: 93, color: '#22c55e' },
    { count: '1', percentage: 5, color: '#0ea5e9' },
    { count: '2', percentage: 2, color: '#eab308' },
    { count: '3-5', percentage: 1, color: '#f97316' },
    { count: 'Supérieure à 5', percentage: 0, color: '#ef4444' },
  ]

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-4">{t('tickets.technicianInterventions')}</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={interventionData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="count"
            tick={{ fill: 'rgba(255,255,255,0.7)' }}
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
            {interventionData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

