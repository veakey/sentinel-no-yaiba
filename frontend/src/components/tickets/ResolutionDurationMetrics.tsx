import { useTranslation } from 'react-i18next'
import { Clock, CheckCircle, MessageSquare } from 'lucide-react'

export default function ResolutionDurationMetrics() {
  const { t } = useTranslation()

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <Clock className="w-5 h-5 text-primary-400" />
          <h3 className="font-semibold text-white">{t('tickets.averageResolutionTime')}</h3>
        </div>
        <p className="text-lg font-semibold text-white">6 {t('tickets.days')} 2 {t('tickets.hours')} 36 {t('tickets.minutes')}</p>
      </div>

      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <CheckCircle className="w-5 h-5 text-primary-400" />
          <h3 className="font-semibold text-white">{t('tickets.firstTimeResolution')}</h3>
        </div>
        <p className="text-lg font-semibold text-white">49.02%</p>
      </div>

      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <MessageSquare className="w-5 h-5 text-primary-400" />
          <h3 className="font-semibold text-white">{t('tickets.firstResponseTime')}</h3>
        </div>
        <p className="text-lg font-semibold text-white">2 {t('tickets.days')} 12 {t('tickets.hours')} 34 {t('tickets.minutes')}</p>
      </div>
    </div>
  )
}

