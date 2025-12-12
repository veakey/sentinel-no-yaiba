import { useTranslation } from 'react-i18next'
import { useEndpointStore } from '@/store/endpointStore'
import { subDays, isBefore } from 'date-fns'
import {
  Target,
  AlertTriangle,
  RefreshCw,
  Settings,
  AlertCircle,
  Server,
} from 'lucide-react'

interface SummaryCardData {
  labelKey: string
  value: number
  icon: React.ComponentType<{ className?: string }>
  iconColor: string
  bgColor: string
}

export default function EndpointSummaryCards() {
  const { t } = useTranslation()
  const { data } = useEndpointStore()
  
  const endpoints = data?.endpoints || []
  const summary = data?.summary || { total: 0 }
  
  // Calculate metrics from endpoints
  const now = new Date()
  const sevenDaysAgo = subDays(now, 7)
  
  let scanNeeded = 0
  let lastSynced7DaysAgo = 0
  let agentUpdateAvailable = 0
  let needsAttention = 0
  
  endpoints.forEach((endpoint: any) => {
    // Check if scan is needed (simplified logic)
    if (endpoint.scan_status === 'pending' || endpoint.scan_status === 'required') {
      scanNeeded++
    }
    
    // Check last sync
    const lastSync = endpoint.last_sync || endpoint.last_seen || endpoint.updated_at
    if (lastSync) {
      try {
        const lastSyncDate = new Date(lastSync)
        if (isBefore(lastSyncDate, sevenDaysAgo)) {
          lastSynced7DaysAgo++
        }
      } catch {
        // Skip invalid dates
      }
    }
    
    // Check agent update
    if (endpoint.agent_update_available || endpoint.update_available) {
      agentUpdateAvailable++
    }
    
    // Check if needs attention (has issues)
    if (endpoint.status === 'needs_attention' || endpoint.issues?.length > 0) {
      needsAttention++
    }
  })

  const summaryData: SummaryCardData[] = [
    {
      labelKey: 'endpoints.total',
      value: summary.total,
      icon: Server,
      iconColor: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
    },
    {
      labelKey: 'endpoints.scanNeeded',
      value: scanNeeded,
      icon: Target,
      iconColor: 'text-red-400',
      bgColor: 'bg-red-500/10',
    },
    {
      labelKey: 'endpoints.lastSynced7DaysAgo',
      value: lastSynced7DaysAgo,
      icon: RefreshCw,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.agentUpdateAvailable',
      value: agentUpdateAvailable,
      icon: Settings,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.needsAttention',
      value: needsAttention,
      icon: AlertCircle,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.protected',
      value: (summary as any).protection_status?.protected || 0,
      icon: AlertTriangle,
      iconColor: 'text-green-400',
      bgColor: 'bg-green-500/10',
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {summaryData.map((item) => {
        const Icon = item.icon
        return (
          <div key={item.labelKey} className={`glass rounded-lg p-4 ${item.bgColor}`}>
            <div className="flex items-center justify-between mb-3">
              <Icon className={`w-6 h-6 ${item.iconColor}`} />
            </div>
            <div className="mb-2">
              <p className="text-sm text-white/60 mb-1">{t(item.labelKey)}</p>
              <p className="text-2xl font-bold text-white">{item.value}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}

