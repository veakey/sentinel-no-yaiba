import { useTranslation } from 'react-i18next'
import { Plus } from 'lucide-react'

const mockNewDevices = [
  'MGD-PCD026759',
  'vca01.labo.labomgd.ch',
  'MGD-PCD026759',
  'MGD-PCD026607',
  'PC-162',
  'PC132',
  'MGD-PCD026589',
  'MGD-PCD026588',
]

export default function NewDevicesList() {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <Plus className="w-5 h-5 text-primary-400" />
        <h2 className="text-xl font-semibold text-white">
          {t('tickets.newDevicesAdded')}
        </h2>
      </div>
      <div className="space-y-2">
        {mockNewDevices.map((device, index) => (
          <div key={`${device}-${index}`} className="glass rounded-lg p-3">
            <span className="text-sm text-white/90">{device}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

