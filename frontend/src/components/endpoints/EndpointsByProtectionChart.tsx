import { useTranslation } from 'react-i18next'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

interface ProtectionData {
  nameKey: string
  value: number
  color: string
}

export default function EndpointsByProtectionChart() {
  const { t } = useTranslation()

  const protectionData: ProtectionData[] = [
    { nameKey: 'endpoints.protected', value: 140, color: '#0ea5e9' },
  ]

  const totalEndpoints = protectionData.reduce((sum, item) => sum + item.value, 0)

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={protectionData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={0}
            dataKey="value"
            label={false}
          >
            {protectionData.map((entry, index) => (
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
        {protectionData.map((item) => (
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

