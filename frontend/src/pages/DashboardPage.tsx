import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useThreatsStore } from '@/store/threatsStore'
import { useWebSocket } from '@/hooks/useWebSocket'
import StatCard from '@/components/dashboard/StatCard'
import ThreatChart from '@/components/dashboard/ThreatChart'
import { Shield, AlertTriangle, CheckCircle, Clock } from 'lucide-react'

export default function DashboardPage() {
  const { t } = useTranslation()
  const { threats, isLoading, lastUpdate, fetchThreats, getThreatsByStatus } = useThreatsStore()
  const { isConnected } = useWebSocket()

  useEffect(() => {
    fetchThreats()
  }, [fetchThreats])

  const activeThreats = getThreatsByStatus('active')
  const resolvedThreats = getThreatsByStatus('resolved')
  const pendingThreats = getThreatsByStatus('pending')

  const criticalThreats = threats.filter((t) => t.severity === 'critical').length
  const highThreats = threats.filter((t) => t.severity === 'high').length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">{t('dashboard.title')}</h1>
          {isConnected && (
            <p className="text-sm text-green-400 mt-1">● Connecté en temps réel</p>
          )}
        </div>
        <button
          onClick={() => fetchThreats(true)}
          disabled={isLoading}
          className="px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors disabled:opacity-50"
        >
          {t('common.refresh')}
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-white/60">{t('common.loading')}</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title={t('dashboard.totalThreats')}
              value={threats.length}
              icon={Shield}
              color="blue"
            />
            <StatCard
              title={t('dashboard.activeThreats')}
              value={activeThreats.length}
              icon={AlertTriangle}
              color="red"
            />
            <StatCard
              title={t('dashboard.resolvedThreats')}
              value={resolvedThreats.length}
              icon={CheckCircle}
              color="green"
            />
            <StatCard
              title="En attente"
              value={pendingThreats.length}
              icon={Clock}
              color="yellow"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass-strong rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-4">{t('dashboard.bySeverity')}</h2>
              <ThreatChart
                data={[
                  { name: 'Critique', value: criticalThreats, color: '#ef4444' },
                  { name: 'Élevée', value: highThreats, color: '#f97316' },
                  { name: 'Moyenne', value: threats.filter((t) => t.severity === 'medium').length, color: '#eab308' },
                  { name: 'Faible', value: threats.filter((t) => t.severity === 'low').length, color: '#22c55e' },
                ]}
              />
            </div>

            <div className="glass-strong rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-4">{t('dashboard.byStatus')}</h2>
              <ThreatChart
                data={[
                  { name: 'Active', value: activeThreats.length, color: '#ef4444' },
                  { name: 'Résolue', value: resolvedThreats.length, color: '#22c55e' },
                  { name: 'En attente', value: pendingThreats.length, color: '#eab308' },
                ]}
              />
            </div>
          </div>

          {lastUpdate && (
            <div className="text-sm text-white/60 text-center">
              {t('dashboard.lastUpdate')}: {new Date(lastUpdate).toLocaleString('fr-FR')}
            </div>
          )}
        </>
      )}
    </div>
  )
}

