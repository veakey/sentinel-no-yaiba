import { useTranslation } from 'react-i18next'
import EndpointSummaryCards from '@/components/endpoints/EndpointSummaryCards'
import EndpointsByOSChart from '@/components/endpoints/EndpointsByOSChart'
import EndpointsByPolicyChart from '@/components/endpoints/EndpointsByPolicyChart'
import EndpointsByProtectionChart from '@/components/endpoints/EndpointsByProtectionChart'
import EndpointsByActivityChart from '@/components/endpoints/EndpointsByActivityChart'
import { Server } from 'lucide-react'

export default function EndpointSummaryPage() {
  const { t } = useTranslation()

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Server className="w-8 h-8 text-primary-400" />
        <h1 className="text-3xl font-bold text-white">{t('navigation.endpointSummary')}</h1>
      </div>

      {/* Summary Cards */}
      <div className="glass-strong rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-2">{t('endpoints.summary')}</h2>
        <p className="text-sm text-white/60 mb-4">
          {t('endpoints.summaryDescription')}
        </p>
        <EndpointSummaryCards />
      </div>

      {/* Charts Row 1 - Endpoints by OS and Protection Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('endpoints.byOS')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('endpoints.byOSDescription')}
          </p>
          <EndpointsByOSChart />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('endpoints.byProtectionStatus')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('endpoints.byProtectionStatusDescription')}
          </p>
          <EndpointsByProtectionChart />
        </div>
      </div>

      {/* Charts Row 2 - Endpoints by Policy and Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('endpoints.byPolicy')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('endpoints.byPolicyDescription')}
          </p>
          <EndpointsByPolicyChart />
        </div>

        <div className="glass-strong rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-2">{t('endpoints.byActivity')}</h2>
          <p className="text-sm text-white/60 mb-4">
            {t('endpoints.byActivityDescription')}
          </p>
          <EndpointsByActivityChart />
        </div>
      </div>
    </div>
  )
}

