import { useTranslation } from 'react-i18next'
import { AlertTriangle } from 'lucide-react'

interface DeviceAlert {
  device: string
  alerts: number
}

const mockDevices: DeviceAlert[] = [
  { device: 'JadeOnline PROD', alerts: 10 },
  { device: 'PC130', alerts: 2 },
  { device: 'PCD-223', alerts: 1 },
  { device: 'MGD-PCL026717', alerts: 1 },
  { device: 'MGD-PCL026530', alerts: 1 },
  { device: 'PCD-128', alerts: 1 },
  { device: 'MGD-PCD026614', alerts: 1 },
]

export default function DevicesWithMostAlerts() {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-primary-400" />
        <h2 className="text-xl font-semibold text-white">
          {t('tickets.devicesWithMostAlerts')}
        </h2>
      </div>
      <div className="space-y-2">
        {mockDevices.map((item) => (
          <div key={item.device} className="flex items-center justify-between glass rounded-lg p-3">
            <span className="text-sm text-white/90">{item.device}</span>
            <span className="text-sm font-semibold text-white">{item.alerts} {t('tickets.alerts')}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

