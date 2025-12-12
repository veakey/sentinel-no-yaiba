import { useTranslation } from 'react-i18next'
import type { Ticket } from '@/types'
import { AlertCircle, Clock, CheckCircle, XCircle, Tag } from 'lucide-react'
import { format } from 'date-fns'
import { fr } from 'date-fns/locale'

const statusConfig = {
  open: { icon: AlertCircle, color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/50' },
  in_progress: { icon: Clock, color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/50' },
  resolved: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/50' },
  closed: { icon: XCircle, color: 'text-gray-400', bg: 'bg-gray-500/10', border: 'border-gray-500/50' },
}

const priorityColors = {
  low: 'bg-green-500/20 text-green-300',
  medium: 'bg-yellow-500/20 text-yellow-300',
  high: 'bg-orange-500/20 text-orange-300',
  critical: 'bg-red-500/20 text-red-300',
}

export default function TicketCard({ ticket }: { ticket: Ticket }) {
  const { t } = useTranslation()
  const status = statusConfig[ticket.status]
  const StatusIcon = status.icon

  return (
    <div className={`glass-strong rounded-xl p-6 border-l-4 ${status.border}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{ticket.title}</h3>
          <p className="text-sm text-white/60 mb-3">{ticket.description}</p>
        </div>
        <StatusIcon className={`w-5 h-5 ${status.color}`} />
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        <span className={`px-2 py-1 text-xs rounded ${priorityColors[ticket.priority]}`}>
          {ticket.priority}
        </span>
        <span className={`px-2 py-1 text-xs glass rounded ${status.bg} ${status.color}`}>
          {ticket.status}
        </span>
        {ticket.tags?.map((tag) => (
          <span key={tag} className="px-2 py-1 text-xs glass rounded flex items-center gap-1">
            <Tag className="w-3 h-3" />
            {tag}
          </span>
        ))}
      </div>

      <div className="text-xs text-white/50 space-y-1">
        <p>Créé: {format(new Date(ticket.createdAt), 'PPpp', { locale: fr })}</p>
        <p>Mis à jour: {format(new Date(ticket.updatedAt), 'PPpp', { locale: fr })}</p>
        {ticket.assignedTo && <p>Assigné à: {ticket.assignedTo}</p>}
      </div>
    </div>
  )
}

