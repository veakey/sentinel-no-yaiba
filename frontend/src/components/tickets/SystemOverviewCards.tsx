import { useTranslation } from 'react-i18next'
import { Package, Cpu, Monitor, Bell, Zap } from 'lucide-react'

export default function SystemOverviewCards() {
  const { t } = useTranslation()

  return (
    <div className="space-y-6">
      {/* First Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Package className="w-5 h-5 text-primary-400" />
            <h3 className="font-semibold text-white">{t('tickets.software')}</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.added')}</span>
              <span className="text-sm font-semibold text-white">6</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.deleted')}</span>
              <span className="text-sm font-semibold text-white">3</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.updated')}</span>
              <span className="text-sm font-semibold text-white">376</span>
            </div>
          </div>
        </div>

        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Cpu className="w-5 h-5 text-primary-400" />
            <h3 className="font-semibold text-white">{t('tickets.hardware')}</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.added')}</span>
              <span className="text-sm font-semibold text-white">61</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.deleted')}</span>
              <span className="text-sm font-semibold text-white">39</span>
            </div>
          </div>
        </div>
      </div>

      {/* Second Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Monitor className="w-5 h-5 text-primary-400" />
            <h3 className="font-semibold text-white">Teamviewer</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.devices')}</span>
              <span className="text-sm font-semibold text-white">0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-white/70">{t('tickets.sessions')}</span>
              <span className="text-sm font-semibold text-white">0</span>
            </div>
          </div>
        </div>

        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Bell className="w-5 h-5 text-primary-400" />
            <h3 className="font-semibold text-white">{t('tickets.triggeredAlerts')}</h3>
          </div>
          <p className="text-3xl font-bold text-white">17</p>
        </div>

        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Zap className="w-5 h-5 text-primary-400" />
            <h3 className="font-semibold text-white">{t('tickets.executedActions')}</h3>
          </div>
          <p className="text-3xl font-bold text-white">33</p>
        </div>
      </div>
    </div>
  )
}

