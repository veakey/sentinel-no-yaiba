import { useTranslation } from 'react-i18next'
import SummaryCards from '@/components/detection/SummaryCards'
import EndpointsTable from '@/components/detection/EndpointsTable'
import ThreatCategoryChart from '@/components/detection/ThreatCategoryChart'
import FrequentThreatsTable from '@/components/detection/FrequentThreatsTable'
import GroupsTable from '@/components/detection/GroupsTable'
import DetectionsPerDayChart from '@/components/detection/DetectionsPerDayChart'
import { Shield } from 'lucide-react'

export default function DetectionSummaryPage() {
  const { t } = useTranslation()

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Shield className="w-8 h-8 text-primary-400" />
        <h1 className="text-3xl font-bold text-white">{t('navigation.detectionSummary')}</h1>
      </div>

      {/* Summary Cards */}
      <div className="glass-strong rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-2">{t('detection.summary')}</h2>
        <p className="text-sm text-white/60 mb-4">
          {t('detection.summaryDescription')}
        </p>
        <SummaryCards />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('detection.byThreatCategory')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('detection.byThreatCategoryDescription')}
          </p>
          <ThreatCategoryChart />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('detection.perDay')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('detection.perDayDescription')}
          </p>
          <DetectionsPerDayChart />
        </div>
      </div>

      {/* Tables Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('detection.endpointsWithMostDetections')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('detection.endpointsWithMostDetectionsDescription')}
          </p>
          <EndpointsTable />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('detection.byGroup')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('detection.byGroupDescription')}
          </p>
          <GroupsTable />
        </div>
      </div>

      {/* Frequent Threats Table */}
      <div className="glass-strong rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-2">{t('detection.mostFrequentThreats')}</h2>
        <p className="text-sm text-white/60 mb-4">
          {t('detection.mostFrequentThreatsDescription')}
        </p>
        <FrequentThreatsTable />
      </div>
    </div>
  )
}

