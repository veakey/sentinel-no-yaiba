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
        <h1 className="text-3xl font-bold text-white">Detection Summary</h1>
      </div>

      {/* Summary Cards */}
      <div className="glass-strong rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-2">Summary</h2>
        <p className="text-sm text-white/60 mb-4">
          Threats detected in this reporting period and their status.
        </p>
        <SummaryCards />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">Detections by threat category</h2>
          <p className="text-sm text-white/60 mb-4">
            The various threats your endpoints encountered. These threats may harm your endpoints and compromise your data.
          </p>
          <ThreatCategoryChart />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">Detections per day</h2>
          <p className="text-sm text-white/60 mb-4">
            Detections from the most recent 30 days of the reporting period to help discover and monitor trends.
          </p>
          <DetectionsPerDayChart />
        </div>
      </div>

      {/* Tables Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">Endpoints with most detections</h2>
          <p className="text-sm text-white/60 mb-4">
            The 10 endpoints with the most detections. Monitor these endpoints closely to mitigate the risk to your network.
          </p>
          <EndpointsTable />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">Detections by group</h2>
          <p className="text-sm text-white/60 mb-4">
            The 10 groups with the most detections. Monitor these endpoints closely to mitigate the risk to your network.
          </p>
          <GroupsTable />
        </div>
      </div>

      {/* Frequent Threats Table */}
      <div className="glass-strong rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-2">Most frequently detected threats</h2>
        <p className="text-sm text-white/60 mb-4">
          The 10 most common threats detected, including those blocked, quarantined, deleted, found, and restored.
        </p>
        <FrequentThreatsTable />
      </div>
    </div>
  )
}

