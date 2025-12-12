import { useTranslation } from 'react-i18next'
import {
  Target,
  Briefcase,
  Power,
  AlertTriangle,
  Square,
  RefreshCw,
  Settings,
  AlertCircle,
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

  const summaryData: SummaryCardData[] = [
    {
      labelKey: 'endpoints.scanNeeded',
      value: 37,
      icon: Target,
      iconColor: 'text-red-400',
      bgColor: 'bg-red-500/10',
    },
    {
      labelKey: 'endpoints.remediationRequired',
      value: 0,
      icon: Briefcase,
      iconColor: 'text-green-400',
      bgColor: 'bg-green-500/10',
    },
    {
      labelKey: 'endpoints.restartRequired',
      value: 0,
      icon: Power,
      iconColor: 'text-red-400',
      bgColor: 'bg-red-500/10',
    },
    {
      labelKey: 'endpoints.suspiciousActivity',
      value: 0,
      icon: AlertTriangle,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.endpointsIsolated',
      value: 0,
      icon: Square,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.lastSynced7DaysAgo',
      value: 33,
      icon: RefreshCw,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.agentUpdateAvailable',
      value: 6,
      icon: Settings,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
    },
    {
      labelKey: 'endpoints.needsAttention',
      value: 4,
      icon: AlertCircle,
      iconColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
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

