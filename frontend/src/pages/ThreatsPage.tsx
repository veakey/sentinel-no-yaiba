import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useThreatsStore } from '@/store/threatsStore'
import ThreatCard from '@/components/threats/ThreatCard'
import ThreatFilters from '@/components/threats/ThreatFilters'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import type { Threat } from '@/types'

export default function ThreatsPage() {
  const { t } = useTranslation()
  const { threats, isLoading, fetchThreats } = useThreatsStore()
  const [filteredThreats, setFilteredThreats] = useState<Threat[]>(threats)
  const [filters, setFilters] = useState<{
    severity?: string
    status?: string
    provider?: string
  }>({})

  useEffect(() => {
    fetchThreats()
  }, [fetchThreats])

  useEffect(() => {
    let filtered = [...threats]

    if (filters.severity) {
      filtered = filtered.filter((t) => t.severity === filters.severity)
    }
    if (filters.status) {
      filtered = filtered.filter((t) => t.status === filters.status)
    }
    if (filters.provider) {
      filtered = filtered.filter((t) => t.provider === filters.provider)
    }

    setFilteredThreats(filtered)
  }, [threats, filters])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">{t('threats.title')}</h1>
        <button
          onClick={() => fetchThreats(true)}
          disabled={isLoading}
          className="px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors disabled:opacity-50"
        >
          {t('common.refresh')}
        </button>
      </div>

      <ThreatFilters filters={filters} onFiltersChange={setFilters} />

      {isLoading ? (
        <LoadingSpinner text={t('common.loading')} />
      ) : filteredThreats.length === 0 ? (
        <div className="text-center py-12 text-white/60">{t('dashboard.noData')}</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredThreats.map((threat) => (
            <ThreatCard key={threat.id} threat={threat} />
          ))}
        </div>
      )}
    </div>
  )
}

