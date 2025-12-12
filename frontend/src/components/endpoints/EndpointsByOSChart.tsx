import { useTranslation } from 'react-i18next'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface OSData {
  nameKey: string
  value: number
  color: string
}

export default function EndpointsByOSChart() {
  const { t } = useTranslation()

  const osData: OSData[] = [
    { nameKey: 'endpoints.windows', value: 128, color: '#9333ea' },
    { nameKey: 'endpoints.linux', value: 12, color: '#0ea5e9' },
  ]

  const totalEndpoints = osData.reduce((sum, item) => sum + item.value, 0)

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={osData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={5}
            dataKey="value"
            label={false}
          >
            {osData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
          />
          <text
            x="50%"
            y="50%"
            textAnchor="middle"
            dominantBaseline="middle"
            className="text-2xl font-bold fill-white"
          >
            {totalEndpoints} {t('endpoints.total')}
          </text>
        </PieChart>
      </ResponsiveContainer>
      <div className="flex flex-col gap-2 mt-4">
        {osData.map((item) => (
          <div key={item.nameKey} className="flex items-center gap-3">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <div className="flex items-center gap-2">
              <span className="text-sm text-white/70 font-semibold">{t(item.nameKey)}:</span>
              <span className="text-sm text-white/90">{item.value}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

