import { useTranslation } from 'react-i18next'
import { useEndpointStore } from '@/store/endpointStore'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { subDays, isAfter } from 'date-fns'

interface ActivityData {
  nameKey: string
  value: number
  color: string
}

export default function EndpointsByActivityChart() {
  const { t } = useTranslation()
  const { data } = useEndpointStore()
  
  const endpoints = data?.endpoints || []
  const now = new Date()
  const sevenDaysAgo = subDays(now, 7)
  const thirtyDaysAgo = subDays(now, 30)
  
  let active7Days = 0
  let offline30Days = 0
  let inactive30Days = 0
  
  endpoints.forEach((endpoint: any) => {
    const lastSeen = endpoint.last_seen || endpoint.last_sync || endpoint.updated_at
    if (!lastSeen) {
      inactive30Days++
      return
    }
    
    try {
      const lastSeenDate = new Date(lastSeen)
      if (isAfter(lastSeenDate, sevenDaysAgo)) {
        active7Days++
      } else if (isAfter(lastSeenDate, thirtyDaysAgo)) {
        offline30Days++
      } else {
        inactive30Days++
      }
    } catch {
      inactive30Days++
    }
  })
  
  const activityData: ActivityData[] = [
    { nameKey: 'endpoints.activeSynced7Days', value: active7Days, color: '#06b6d4' },
    { nameKey: 'endpoints.offlineSynced30Days', value: offline30Days, color: '#9333ea' },
    { nameKey: 'endpoints.inactiveSynced30Days', value: inactive30Days, color: '#0ea5e9' },
  ].filter(item => item.value > 0) // Only show non-zero values

  const totalEndpoints = activityData.reduce((sum, item) => sum + item.value, 0)

  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={activityData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={5}
            dataKey="value"
            label={false}
          >
            {activityData.map((entry, index) => (
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
        {activityData.map((item) => (
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

