import { useTranslation } from 'react-i18next'

interface ProtectionMetric {
  labelKey: string
  percentage: number
  count: string
  color: 'green' | 'blue'
}

export default function AntivirusProtection() {
  const { t } = useTranslation()

  const metrics: ProtectionMetric[] = [
    { labelKey: 'tickets.totalActiveDevicesProtected', percentage: 92, count: '26/28', color: 'green' },
    { labelKey: 'tickets.globalAntivirusCoverage', percentage: 92, count: '26/28', color: 'green' },
    { labelKey: 'tickets.microsoftDefenderAntivirus', percentage: 92, count: '26/28', color: 'blue' },
    { labelKey: 'tickets.malwarebytes', percentage: 21, count: '6/28', color: 'blue' },
  ]

  const getColorClass = (color: string) => {
    return color === 'green' ? 'bg-green-500' : 'bg-cyan-500'
  }

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-2">{t('tickets.antivirusProtection')}</h3>
      <p className="text-xs text-white/60 mb-4">{t('tickets.scoreBasedOnCurrentData')}</p>
      
      <div className="mb-4">
        <p className="text-3xl font-bold text-white mb-2">92%</p>
      </div>

      <div className="space-y-3">
        {metrics.map((metric) => (
          <div key={metric.labelKey}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm text-white/70">{t(metric.labelKey)}</span>
              <span className="text-sm font-semibold text-white">{metric.percentage}% ({metric.count})</span>
            </div>
            <div className="w-full bg-white/10 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getColorClass(metric.color)}`}
                style={{ width: `${metric.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap gap-3 mt-4 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded" />
          <span className="text-white/70">{t('tickets.integrity')}</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-cyan-500 rounded" />
          <span className="text-white/70">{t('tickets.informative')}</span>
        </div>
      </div>
    </div>
  )
}

