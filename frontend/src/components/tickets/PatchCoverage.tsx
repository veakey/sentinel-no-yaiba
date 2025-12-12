import { useTranslation } from 'react-i18next'

export default function PatchCoverage() {
  const { t } = useTranslation()

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-2">{t('tickets.patchCoverage')}</h3>
      <p className="text-xs text-white/60 mb-4">{t('tickets.scoreBasedOnLast30Days')}</p>
      
      <div className="mb-4">
        <p className="text-3xl font-bold text-white mb-2">0%</p>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-white/70">{t('tickets.fullyPatched')}</span>
          <span className="text-white">0 | 0%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-white/70">{t('tickets.oneMissingPatch')}</span>
          <span className="text-white">0 | 0%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-white/70">{t('tickets.twoThreeMissingPatches')}</span>
          <span className="text-white">0 | 0%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-white/70">{t('tickets.fourFiveMissingPatches')}</span>
          <span className="text-white">0 | 0%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-white/70">{t('tickets.moreThanFiveMissingPatches')}</span>
          <span className="text-white">0 | 0%</span>
        </div>
      </div>

      <p className="text-xs text-white/60">{t('tickets.noDataForMostAffectedMachines')}</p>
    </div>
  )
}

