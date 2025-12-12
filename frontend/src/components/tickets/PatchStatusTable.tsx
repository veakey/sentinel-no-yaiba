import { useTranslation } from 'react-i18next'

export default function PatchStatusTable() {
  const { t } = useTranslation()

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/10">
            <th rowSpan={2} className="text-left py-3 px-4 text-sm font-semibold text-white/80 border-r border-white/10">
              {t('tickets.devices')}
            </th>
            <th rowSpan={2} className="text-left py-3 px-4 text-sm font-semibold text-white/80 border-r border-white/10">
              OS
            </th>
            <th colSpan={4} className="text-center py-3 px-4 text-sm font-semibold text-white/80 border-r border-white/10">
              OS
            </th>
            <th colSpan={4} className="text-center py-3 px-4 text-sm font-semibold text-white/80">
              {t('tickets.thirdParty')}
            </th>
          </tr>
          <tr className="border-b border-white/10">
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.installed')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.approved')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.pending')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.failed')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.installed')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.approved')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80 border-r border-white/10">
              {t('tickets.pending')}
            </th>
            <th className="text-center py-2 px-4 text-xs font-semibold text-white/80">
              {t('tickets.failed')}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan={10} className="py-8 text-center text-white/60">
              {t('dashboard.noData')}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

