import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

interface PolicyData {
  policy: string
  endpoints: number
  color: string
}

const policyData: PolicyData[] = [
  { policy: 'EDR Postes', endpoints: 99, color: '#0ea5e9' },
  { policy: 'EDR Serveurs', endpoints: 25, color: '#9333ea' },
  { policy: 'Default Policy', endpoints: 11, color: '#06b6d4' },
  { policy: 'Serveurs RDS (Sans Behavior)', endpoints: 3, color: '#6b7280' },
  { policy: 'Serveurs Web', endpoints: 2, color: '#22c55e' },
]

export default function EndpointsByPolicyChart() {
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

