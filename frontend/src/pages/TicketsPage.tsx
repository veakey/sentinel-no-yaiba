import { useTranslation } from 'react-i18next'
import { Ticket } from 'lucide-react'
import IntegrityScoreCards from '@/components/tickets/IntegrityScoreCards'
import SystemOverviewCards from '@/components/tickets/SystemOverviewCards'
import DeviceTypeChart from '@/components/tickets/DeviceTypeChart'
import OSDistributionChart from '@/components/tickets/OSDistributionChart'
import ResolutionDurationMetrics from '@/components/tickets/ResolutionDurationMetrics'
import ResolutionDistributionChart from '@/components/tickets/ResolutionDistributionChart'
import TechnicianInterventionsChart from '@/components/tickets/TechnicianInterventionsChart'
import DevicesWithMostAlerts from '@/components/tickets/DevicesWithMostAlerts'
import NewDevicesList from '@/components/tickets/NewDevicesList'
import InfectedDevicesList from '@/components/tickets/InfectedDevicesList'
import LowDiskSpaceDevices from '@/components/tickets/LowDiskSpaceDevices'
import ManagementSummary from '@/components/tickets/ManagementSummary'
import DiskUsageTable from '@/components/tickets/DiskUsageTable'
import PatchStatusTable from '@/components/tickets/PatchStatusTable'
import ErrorBoundary from '@/components/common/ErrorBoundary'

export default function TicketsPage() {
  const { t } = useTranslation()

  return (
    <ErrorBoundary>
      <div className="space-y-6">
        <div className="flex items-center gap-3 mb-6">
          <Ticket className="w-8 h-8 text-primary-400" />
          <h1 className="text-3xl font-bold text-white">{t('tickets.title')}</h1>
        </div>

        {/* Integrity Score Section */}
        <ErrorBoundary>
          <div className="glass-strong rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-2">{t('tickets.integrityScore')}</h2>
            <IntegrityScoreCards />
          </div>
        </ErrorBoundary>

        {/* System Overview Section */}
        <ErrorBoundary>
          <div className="glass-strong rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">{t('tickets.systemOverview')}</h2>
            <SystemOverviewCards />
          </div>
        </ErrorBoundary>

        {/* Charts Row - Device Type and OS */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ErrorBoundary>
            <div className="glass-strong rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-2">{t('tickets.deviceTypeOverview')}</h2>
              <DeviceTypeChart />
            </div>
          </ErrorBoundary>

          <ErrorBoundary>
            <div className="glass-strong rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-2">{t('tickets.osOverview')}</h2>
              <OSDistributionChart />
            </div>
          </ErrorBoundary>
        </div>

        {/* Resolution Duration Section */}
        <ErrorBoundary>
          <div className="glass-strong rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">{t('tickets.resolutionDuration')}</h2>
            <ResolutionDurationMetrics />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
              <ResolutionDistributionChart />
              <TechnicianInterventionsChart />
            </div>
          </div>
        </ErrorBoundary>

        {/* Management Summary */}
        <ErrorBoundary>
          <ManagementSummary />
        </ErrorBoundary>

        {/* Devices Lists */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ErrorBoundary>
            <DevicesWithMostAlerts />
          </ErrorBoundary>
          <ErrorBoundary>
            <NewDevicesList />
          </ErrorBoundary>
        </div>

        {/* Infected and Low Disk Space */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ErrorBoundary>
            <InfectedDevicesList />
          </ErrorBoundary>
          <ErrorBoundary>
            <LowDiskSpaceDevices />
          </ErrorBoundary>
        </div>

        {/* Disk Usage Table */}
        <ErrorBoundary>
          <div className="glass-strong rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-2">{t('tickets.mainVolumesByDiskUsage')}</h2>
            <p className="text-sm text-white/60 mb-4">{t('tickets.scoreBasedOnCurrentData')}</p>
            <DiskUsageTable />
          </div>
        </ErrorBoundary>

        {/* Patch Status Table */}
        <ErrorBoundary>
          <div className="glass-strong rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-2">{t('tickets.patchStatusByDevice')}</h2>
            <PatchStatusTable />
          </div>
        </ErrorBoundary>
      </div>
    </ErrorBoundary>
  )
}

