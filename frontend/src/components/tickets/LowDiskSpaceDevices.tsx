import { useTranslation } from 'react-i18next'
import { HardDrive } from 'lucide-react'

interface LowDiskDevice {
  device: string
  space: string
}

const mockLowDiskDevices: LowDiskDevice[] = [
  { device: 'vca01.labo.labomgd.ch (/boot/efi)', space: '8.03 MB' },
  { device: 'vca01.labo.labomgd.ch (/boot)', space: '403.75 MB' },
  { device: 'vca01.labo.labomgd.ch (/storage/netdump)', space: '914.74 MB' },
  { device: 'PC130 (D:)', space: '2.55 GB' },
  { device: 'PC132 (D:)', space: '2.62 GB' },
]

export default function LowDiskSpaceDevices() {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <HardDrive className="w-5 h-5 text-yellow-400" />
        <h2 className="text-xl font-semibold text-white">
          {t('tickets.devicesWithLowDiskSpace')}
        </h2>
      </div>
      <div className="space-y-2">
        {mockLowDiskDevices.map((item, index) => (
          <div key={index} className="flex items-center justify-between glass rounded-lg p-3">
            <span className="text-sm text-white/90">{item.device}</span>
            <span className="text-sm font-semibold text-white">{item.space}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

