import { useTranslation } from 'react-i18next'

interface ThreatFiltersProps {
  filters: {
    severity?: string
    status?: string
    provider?: string
  }
  onFiltersChange: (filters: ThreatFiltersProps['filters']) => void
}

export default function ThreatFilters({ filters, onFiltersChange }: ThreatFiltersProps) {
  const { t } = useTranslation()

  const updateFilter = (key: keyof typeof filters, value: string) => {
    onFiltersChange({
      ...filters,
      [key]: value === '' ? undefined : value,
    })
  }

  return (
    <div className="glass-strong rounded-xl p-4 flex flex-wrap gap-4">
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          {t('threats.severity')}
        </label>
        <select
          value={filters.severity || ''}
          onChange={(e) => updateFilter('severity', e.target.value)}
          className="px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Toutes</option>
          <option value="critical">{t('threats.critical')}</option>
          <option value="high">{t('threats.high')}</option>
          <option value="medium">{t('threats.medium')}</option>
          <option value="low">{t('threats.low')}</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          {t('threats.status')}
        </label>
        <select
          value={filters.status || ''}
          onChange={(e) => updateFilter('status', e.target.value)}
          className="px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tous</option>
          <option value="active">{t('threats.active')}</option>
          <option value="resolved">{t('threats.resolved')}</option>
          <option value="pending">{t('threats.pending')}</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          {t('threats.provider')}
        </label>
        <select
          value={filters.provider || ''}
          onChange={(e) => updateFilter('provider', e.target.value)}
          className="px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tous</option>
          <option value="ninja">Ninja One</option>
          <option value="malwarebytes">Malwarebytes</option>
        </select>
      </div>
    </div>
  )
}

