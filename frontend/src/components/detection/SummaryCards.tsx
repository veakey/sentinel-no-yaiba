import { useTranslation } from 'react-i18next'
import { useDetectionStore } from '@/store/detectionStore'
import { Ban, X, Search, Target, RotateCcw, AlertCircle } from 'lucide-react'

interface SummaryCardData {
  labelKey: string
  count: number
  change: string
  changeType: 'increase' | 'decrease' | 'no-change'
  icon: React.ComponentType<{ className?: string }>
  iconColor: string
}

export default function SummaryCards() {
  const { t } = useTranslation()
  const { data } = useDetectionStore()

  const summary = data?.summary || {
    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
  }

  const summaryData: SummaryCardData[] = [
    {
      labelKey: 'detection.totalDetections',
      count: summary.total,
      change: '—',
      changeType: 'no-change',
      icon: AlertCircle,
      iconColor: 'text-red-400',
    },
    {
      labelKey: 'detection.critical',
      count: summary.critical,
      change: '—',
      changeType: 'no-change',
      icon: Ban,
      iconColor: 'text-red-400',
    },
    {
      labelKey: 'detection.high',
      count: summary.high,
      change: '—',
      changeType: 'no-change',
      icon: Target,
      iconColor: 'text-orange-400',
    },
    {
      labelKey: 'detection.medium',
      count: summary.medium,
      change: '—',
      changeType: 'no-change',
      icon: Search,
      iconColor: 'text-yellow-400',
    },
    {
      labelKey: 'detection.low',
      count: summary.low,
      change: '—',
      changeType: 'no-change',
      icon: X,
      iconColor: 'text-blue-400',
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      {summaryData.map((item) => {
        const Icon = item.icon
        const changeColor =
          item.changeType === 'increase'
            ? 'text-green-400'
            : item.changeType === 'decrease'
            ? 'text-red-400'
            : 'text-white/60'

        return (
          <div key={item.labelKey} className="glass rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <Icon className={`w-6 h-6 ${item.iconColor}`} />
            </div>
            <div className="mb-2">
              <p className="text-sm text-white/60 mb-1">{t(item.labelKey)}</p>
              <p className="text-2xl font-bold text-white">{item.count}</p>
            </div>
            <p className={`text-xs ${changeColor}`}>{item.change}</p>
          </div>
        )
      })}
    </div>
  )
}

