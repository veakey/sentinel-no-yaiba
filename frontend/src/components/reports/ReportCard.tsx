import { useTranslation } from 'react-i18next'
import type { SecurityReport } from '@/types'
import { FileText, Calendar, Shield, AlertTriangle, CheckCircle } from 'lucide-react'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

export default function ReportCard({ report }: { report: SecurityReport }) {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6 glass-hover">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary-400" />
          <h3 className="text-lg font-semibold text-white">{report.title}</h3>
        </div>
        <span className="px-2 py-1 text-xs glass rounded text-white/60">
          {report.type}
        </span>
      </div>

      <div className="space-y-3 mb-4">
        <div className="flex items-center gap-2 text-sm text-white/60">
          <Calendar className="w-4 h-4" />
          <span>
            {format(new Date(report.period.start), 'dd MMM', { locale: fr })} -{' '}
            {format(new Date(report.period.end), 'dd MMM yyyy', { locale: fr })}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div className="glass rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <Shield className="w-4 h-4 text-blue-400" />
              <span className="text-xs text-white/60">Total</span>
            </div>
            <p className="text-lg font-bold text-white">{report.summary.totalThreats}</p>
          </div>

          <div className="glass rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <AlertTriangle className="w-4 h-4 text-red-400" />
              <span className="text-xs text-white/60">Critiques</span>
            </div>
            <p className="text-lg font-bold text-red-400">{report.summary.criticalThreats}</p>
          </div>

          <div className="glass rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span className="text-xs text-white/60">Résolues</span>
            </div>
            <p className="text-lg font-bold text-green-400">{report.summary.resolvedThreats}</p>
          </div>

          <div className="glass rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <AlertTriangle className="w-4 h-4 text-yellow-400" />
              <span className="text-xs text-white/60">Actives</span>
            </div>
            <p className="text-lg font-bold text-yellow-400">{report.summary.activeThreats}</p>
          </div>
        </div>
      </div>

      <div className="text-xs text-white/50">
        Généré le: {format(new Date(report.generatedAt), 'PPpp', { locale: fr })}
      </div>
    </div>
  )
}

