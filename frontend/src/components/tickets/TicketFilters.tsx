import { useTranslation } from 'react-i18next'

interface TicketFiltersProps {
  filters: {
    status?: string
    priority?: string
  }
  onFiltersChange: (filters: TicketFiltersProps['filters']) => void
}

export default function TicketFilters({ filters, onFiltersChange }: TicketFiltersProps) {
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
        <label className="block text-sm font-medium text-white/80 mb-2">Statut</label>
        <select
          value={filters.status || ''}
          onChange={(e) => updateFilter('status', e.target.value)}
          className="px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Tous</option>
          <option value="open">Ouvert</option>
          <option value="in_progress">En cours</option>
          <option value="resolved">Résolu</option>
          <option value="closed">Fermé</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">Priorité</label>
        <select
          value={filters.priority || ''}
          onChange={(e) => updateFilter('priority', e.target.value)}
          className="px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Toutes</option>
          <option value="low">Faible</option>
          <option value="medium">Moyenne</option>
          <option value="high">Élevée</option>
          <option value="critical">Critique</option>
        </select>
      </div>
    </div>
  )
}

