import { useTranslation } from 'react-i18next'
import type { Threat } from '@/types'
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

const severityColors = {
  critical: 'border-red-500 bg-red-500/10',
  high: 'border-orange-500 bg-orange-500/10',
  medium: 'border-yellow-500 bg-yellow-500/10',
  low: 'border-green-500 bg-green-500/10',
}

const statusIcons = {
  active: AlertTriangle,
  resolved: CheckCircle,
  pending: Clock,
}

export default function ThreatCard({ threat }: { threat: Threat }) {
  const { t } = useTranslation()
  const StatusIcon = statusIcons[threat.status]

  return (
    <div className={`glass-strong rounded-xl p-6 border-l-4 ${severityColors[threat.severity]}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{threat.title}</h3>
          <p className="text-sm text-white/60 mb-3">{threat.description}</p>
        </div>
        <StatusIcon className="w-5 h-5 text-white/60" />
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        <span className="px-2 py-1 text-xs glass rounded">
          {t(`threats.${threat.severity}`)}
        </span>
        <span className="px-2 py-1 text-xs glass rounded">
          {t(`threats.${threat.status}`)}
        </span>
        <span className="px-2 py-1 text-xs glass rounded">
          {threat.provider}
        </span>
      </div>

      <div className="text-xs text-white/50">
        <p>{t('threats.detectedAt')}: {format(new Date(threat.detectedAt), 'PPpp', { locale: fr })}</p>
        {threat.resolvedAt && (
          <p>{t('threats.resolvedAt')}: {format(new Date(threat.resolvedAt), 'PPpp', { locale: fr })}</p>
        )}
      </div>
    </div>
  )
}

