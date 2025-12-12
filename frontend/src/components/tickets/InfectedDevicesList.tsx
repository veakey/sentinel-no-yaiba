import { useTranslation } from 'react-i18next'
import { AlertTriangle } from 'lucide-react'

export default function InfectedDevicesList() {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-red-400" />
        <h2 className="text-xl font-semibold text-white">
          {t('tickets.infectedDevices')}
        </h2>
      </div>
      <div className="text-center py-8">
        <p className="text-white/60">{t('tickets.noDeviceFound')}</p>
      </div>
    </div>
  )
}

