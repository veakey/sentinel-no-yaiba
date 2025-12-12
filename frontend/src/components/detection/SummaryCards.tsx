import { useTranslation } from 'react-i18next'
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

  const summaryData: SummaryCardData[] = [
    {
      labelKey: 'detection.blocked',
      count: 10,
      change: '↑ 11% change',
      changeType: 'increase',
      icon: Ban,
      iconColor: 'text-red-400',
    },
    {
      labelKey: 'detection.deleted',
      count: 0,
      change: 'No change',
      changeType: 'no-change',
      icon: X,
      iconColor: 'text-blue-400',
    },
    {
      labelKey: 'detection.found',
      count: 1,
      change: '↓ 94% change',
      changeType: 'decrease',
      icon: Search,
      iconColor: 'text-blue-400',
    },
    {
      labelKey: 'detection.quarantined',
      count: 6,
      change: '↑ 100% change',
      changeType: 'increase',
      icon: Target,
      iconColor: 'text-blue-400',
    },
    {
      labelKey: 'detection.restored',
      count: 0,
      change: 'No change',
      changeType: 'no-change',
      icon: RotateCcw,
      iconColor: 'text-blue-400',
    },
    {
      labelKey: 'detection.totalDetections',
      count: 17,
      change: '↓ 40% change',
      changeType: 'decrease',
      icon: AlertCircle,
      iconColor: 'text-red-400',
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

