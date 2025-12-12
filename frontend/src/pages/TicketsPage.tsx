import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { mockTickets } from '@/services/mockData'
import TicketCard from '@/components/tickets/TicketCard'
import TicketFilters from '@/components/tickets/TicketFilters'
import type { Ticket } from '@/types'

export default function TicketsPage() {
  const { t } = useTranslation()
  const [tickets] = useState<Ticket[]>(mockTickets)
  const [filteredTickets, setFilteredTickets] = useState<Ticket[]>(tickets)
  const [filters, setFilters] = useState<{
    status?: string
    priority?: string
  }>({})

  const handleFiltersChange = (newFilters: typeof filters) => {
    setFilters(newFilters)
    let filtered = [...tickets]

    if (newFilters.status) {
      filtered = filtered.filter((t) => t.status === newFilters.status)
    }
    if (newFilters.priority) {
      filtered = filtered.filter((t) => t.priority === newFilters.priority)
    }

    setFilteredTickets(filtered)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Tickets</h1>
      </div>

      <TicketFilters filters={filters} onFiltersChange={handleFiltersChange} />

      {filteredTickets.length === 0 ? (
        <div className="text-center py-12 text-white/60">{t('dashboard.noData')}</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {filteredTickets.map((ticket) => (
            <TicketCard key={ticket.id} ticket={ticket} />
          ))}
        </div>
      )}
    </div>
  )
}

