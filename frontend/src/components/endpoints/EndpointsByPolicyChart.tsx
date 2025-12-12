import { useEndpointStore } from '@/store/endpointStore'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

interface PolicyData {
  policy: string
  endpoints: number
  color: string
}

const COLORS = ['#0ea5e9', '#9333ea', '#06b6d4', '#6b7280', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6']

export default function EndpointsByPolicyChart() {
  const { data } = useEndpointStore()
  
  const policyDistribution = data?.summary?.policy_distribution || {}
  
  const policyData: PolicyData[] = Object.entries(policyDistribution)
    .map(([policy, endpoints], index) => ({
      policy,
      endpoints: endpoints as number,
      color: COLORS[index % COLORS.length],
    }))
    .sort((a, b) => b.endpoints - a.endpoints) // Sort by endpoints descending
  return (
    <div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={policyData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis type="number" tick={{ fill: 'rgba(255,255,255,0.7)' }} />
          <YAxis
            dataKey="policy"
            type="category"
            tick={{ fill: 'rgba(255,255,255,0.7)' }}
            width={150}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(0,0,0,0.8)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey="endpoints" radius={[0, 8, 8, 0]}>
            {policyData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-4 mt-4 justify-center">
        {policyData.map((item) => (
          <div key={item.policy} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm text-white/70">
              {item.policy}: {item.endpoints}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

