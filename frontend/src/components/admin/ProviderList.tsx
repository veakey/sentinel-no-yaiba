import { useTranslation } from 'react-i18next'
import { mockProviders } from '@/services/mockData'
import { Plus, Edit, Trash2, Power } from 'lucide-react'

export default function ProviderList() {
  const { t } = useTranslation()

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">{t('admin.providers')}</h2>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors">
          <Plus className="w-4 h-4" />
          {t('admin.addProvider')}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mockProviders.map((provider) => (
          <div key={provider.guid} className="glass-strong rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-1">{provider.name}</h3>
                <p className="text-sm text-white/60">{provider.type}</p>
              </div>
              <div className={`w-3 h-3 rounded-full ${provider.is_active ? 'bg-green-500' : 'bg-gray-500'}`} />
            </div>

            <div className="space-y-2 mb-4">
              <p className="text-sm text-white/80">
                <span className="text-white/60">URL:</span> {provider.base_url}
              </p>
              <p className="text-sm text-white/80">
                <span className="text-white/60">Status:</span>{' '}
                {provider.is_active ? 'Actif' : 'Inactif'}
              </p>
            </div>

            <div className="flex gap-2">
              <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors">
                <Edit className="w-4 h-4" />
                {t('common.edit')}
              </button>
              <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors">
                <Power className="w-4 h-4" />
                {t('admin.testConnection')}
              </button>
              <button className="px-4 py-2 glass rounded-lg text-red-400 hover:bg-red-500/20 transition-colors">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

