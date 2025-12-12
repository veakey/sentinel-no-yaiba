import { useTranslation } from 'react-i18next'
import { Shield, Eye, Server, HardDrive } from 'lucide-react'

interface IntegrityCard {
  titleKey: string
  score: number
  descriptionKey?: string
  icon: React.ComponentType<{ className?: string }>
}

export default function IntegrityScoreCards() {
  const { t } = useTranslation()

  const cards: IntegrityCard[] = [
    {
      titleKey: 'tickets.totalScore',
      score: 92,
      icon: Shield,
    },
    {
      titleKey: 'tickets.proactiveMonitoring',
      score: 85,
      descriptionKey: 'tickets.proactiveMonitoringDescription',
      icon: Eye,
    },
    {
      titleKey: 'tickets.serverAvailability',
      score: 100,
      descriptionKey: 'tickets.serverAvailabilityDescription',
      icon: Server,
    },
    {
      titleKey: 'tickets.hardDriveIntegrity',
      score: 92,
      descriptionKey: 'tickets.hardDriveIntegrityDescription',
      icon: HardDrive,
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div key={card.titleKey} className="glass rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <Icon className="w-6 h-6 text-primary-400" />
              <h3 className="text-lg font-semibold text-white">{t(card.titleKey)}</h3>
            </div>
            <div className="mb-3">
              <p className="text-3xl font-bold text-white mb-2">{card.score}%</p>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div
                  className="bg-primary-500 h-2 rounded-full transition-all"
                  style={{ width: `${card.score}%` }}
                />
              </div>
            </div>
            {card.descriptionKey && (
              <p className="text-sm text-white/60">{t(card.descriptionKey)}</p>
            )}
          </div>
        )
      })}
    </div>
  )
}

