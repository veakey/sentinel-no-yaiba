import { useTranslation } from 'react-i18next'

interface DiskUsage {
  device: string
  volume: string
  used: string
  total: string
  percentage: number
  status: 'green' | 'yellow' | 'red'
}

const mockDiskUsage: DiskUsage[] = [
  { device: 'PCD-128', volume: 'C:', used: '448.31 GB', total: '475.95 GB', percentage: 94, status: 'red' },
  { device: 'PC130', volume: 'C:', used: '421.10 GB', total: '455.50 GB', percentage: 92, status: 'red' },
  { device: 'PC-162', volume: 'D:', used: '17.94 GB', total: '20.61 GB', percentage: 87, status: 'yellow' },
  { device: 'PC132', volume: 'D:', used: '17.98 GB', total: '20.61 GB', percentage: 87, status: 'yellow' },
  { device: 'PCD-136', volume: 'D:', used: '17.94 GB', total: '20.61 GB', percentage: 87, status: 'yellow' },
  { device: 'PC130', volume: 'D:', used: '17.45 GB', total: '20.00 GB', percentage: 87, status: 'yellow' },
  { device: 'PCD-204', volume: 'C:', used: '343.36 GB', total: '475.95 GB', percentage: 72, status: 'green' },
  { device: 'PCD-223', volume: 'C:', used: '312.97 GB', total: '465.15 GB', percentage: 67, status: 'green' },
  { device: 'PC132', volume: 'C:', used: '256.08 GB', total: '454.18 GB', percentage: 56, status: 'green' },
  { device: 'PCL-249', volume: 'C:', used: '243.62 GB', total: '474.28 GB', percentage: 51, status: 'green' },
]

const getStatusColor = (status: string) => {
  switch (status) {
    case 'green':
      return 'bg-green-500'
    case 'yellow':
      return 'bg-yellow-500'
    case 'red':
      return 'bg-red-500'
    default:
      return 'bg-gray-500'
  }
}

export default function DiskUsageTable() {
  const { t } = useTranslation()

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/10">
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">
              {t('tickets.deviceName')}
            </th>
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">
              {t('tickets.volume')}
            </th>
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">
              {t('tickets.usedSpace')}
            </th>
            <th className="text-left py-3 px-4 text-sm font-semibold text-white/80">
              {t('tickets.visualBar')}
            </th>
          </tr>
        </thead>
        <tbody>
          {mockDiskUsage.map((row, index) => (
            <tr key={index} className="border-b border-white/5 hover:bg-white/5">
              <td className="py-3 px-4 text-sm text-white/90">{row.device}</td>
              <td className="py-3 px-4 text-sm text-white/90">{row.volume}</td>
              <td className="py-3 px-4 text-sm text-white/90">
                {row.used} / {row.total} | {row.percentage}%
              </td>
              <td className="py-3 px-4">
                <div className="w-full bg-white/10 rounded-full h-4 max-w-xs">
                  <div
                    className={`h-4 rounded-full ${getStatusColor(row.status)}`}
                    style={{ width: `${row.percentage}%` }}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex flex-wrap gap-4 mt-4 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-green-500 rounded" />
          <span className="text-white/70">{t('tickets.lessThan80Utilization')}</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-yellow-500 rounded" />
          <span className="text-white/70">{t('tickets.eightyTo89Utilization')}</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-red-500 rounded" />
          <span className="text-white/70">{t('tickets.ninetyPlusUtilization')}</span>
        </div>
      </div>
    </div>
  )
}

