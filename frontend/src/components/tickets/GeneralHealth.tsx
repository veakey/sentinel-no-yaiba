import { useTranslation } from 'react-i18next'

interface HealthMetric {
  labelKey: string
  score: number
  color: 'green' | 'yellow' | 'red'
}

export default function GeneralHealth() {
  const { t } = useTranslation()

  const metrics: HealthMetric[] = [
    { labelKey: 'tickets.patchCoverage', score: 0, color: 'red' },
    { labelKey: 'tickets.antivirusProtection', score: 92, color: 'green' },
    { labelKey: 'tickets.hardDriveIntegrity', score: 88, color: 'green' },
    { labelKey: 'tickets.serverAvailability', score: 100, color: 'green' },
  ]

  const getColorClass = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-500'
      case 'yellow':
        return 'bg-yellow-500'
      case 'red':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-4">{t('tickets.generalHealth')}</h3>
      <div className="mb-4">
        <p className="text-3xl font-bold text-white mb-2">70%</p>
      </div>
      <div className="space-y-3">
        {metrics.map((metric) => (
          <div key={metric.labelKey}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm text-white/70">{t(metric.labelKey)}</span>
              <span className="text-sm font-semibold text-white">{metric.score}%</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getColorClass(metric.color)}`}
                style={{ width: `${metric.score}%` }}
              />
            </div>
          </div>
        ))}
      </div>
      <div className="flex flex-wrap gap-3 mt-4 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded" />
          <span className="text-white/70">{t('tickets.healthy')}</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-yellow-500 rounded" />
          <span className="text-white/70">{t('tickets.attentionRequired')}</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-red-500 rounded" />
          <span className="text-white/70">{t('tickets.defective')}</span>
        </div>
      </div>
    </div>
  )
}

