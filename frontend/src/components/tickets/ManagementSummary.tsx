import { useTranslation } from 'react-i18next'
import GeneralHealth from './GeneralHealth'
import PatchCoverage from './PatchCoverage'
import AntivirusProtection from './AntivirusProtection'

export default function ManagementSummary() {
  const { t } = useTranslation()

  return (
    <div className="glass-strong rounded-xl p-6">
      <h2 className="text-xl font-semibold text-white mb-6">{t('tickets.managementSummary')}</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GeneralHealth />
        <PatchCoverage />
        <AntivirusProtection />
      </div>
    </div>
  )
}

