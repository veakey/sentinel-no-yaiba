import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useProvidersStore } from '@/store/providersStore'
import { Plus, Edit, Trash2, Power, Loader2 } from 'lucide-react'
import ProviderForm from './ProviderForm'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import type { Provider } from '@/services/api'

export default function ProviderList() {
  const { t } = useTranslation()
  const { providers, isLoading, error, fetchProviders, deleteProvider } = useProvidersStore()
  const [showForm, setShowForm] = useState(false)
  const [editingProvider, setEditingProvider] = useState<Provider | undefined>()

  useEffect(() => {
    fetchProviders()
  }, [fetchProviders])

  const handleAdd = () => {
    setEditingProvider(undefined)
    setShowForm(true)
  }

  const handleEdit = (provider: Provider) => {
    setEditingProvider(provider)
    setShowForm(true)
  }

  const handleDelete = async (guid: string) => {
    if (confirm(t('admin.deleteProvider') + ' ?')) {
      try {
        await deleteProvider(guid)
      } catch (error) {
        console.error('Failed to delete provider:', error)
      }
    }
  }

  const handleFormSave = async () => {
    setShowForm(false)
    await fetchProviders()
  }

  const handleFormClose = () => {
    setShowForm(false)
    setEditingProvider(undefined)
  }

  if (isLoading && providers.length === 0) {
    return <LoadingSpinner />
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">{t('admin.providers')}</h2>
        <button
          onClick={handleAdd}
          className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('admin.addProvider')}
        </button>
      </div>

      {error && (
        <div className="glass-strong rounded-xl p-4 bg-red-500/20 border border-red-500/50">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {providers.length === 0 && !isLoading ? (
        <div className="glass-strong rounded-xl p-8 text-center">
          <p className="text-white/60">{t('dashboard.noData')}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {providers.map((provider) => (
            <div key={provider.guid} className="glass-strong rounded-xl p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">{provider.name}</h3>
                  <p className="text-sm text-white/60 capitalize">{provider.type}</p>
                </div>
                <div className={`w-3 h-3 rounded-full ${provider.is_active ? 'bg-green-500' : 'bg-gray-500'}`} />
              </div>

              <div className="space-y-2 mb-4">
                {provider.base_url && (
                  <p className="text-sm text-white/80">
                    <span className="text-white/60">URL:</span> {provider.base_url}
                  </p>
                )}
                <p className="text-sm text-white/80">
                  <span className="text-white/60">Status:</span>{' '}
                  {provider.is_active ? 'Actif' : 'Inactif'}
                </p>
                {provider.config?.client_id && (
                  <p className="text-sm text-white/80">
                    <span className="text-white/60">Auth:</span> OAuth2
                  </p>
                )}
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(provider)}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors"
                >
                  <Edit className="w-4 h-4" />
                  {t('common.edit')}
                </button>
                <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors">
                  <Power className="w-4 h-4" />
                  {t('admin.testConnection')}
                </button>
                <button
                  onClick={() => handleDelete(provider.guid)}
                  className="px-4 py-2 glass rounded-lg text-red-400 hover:bg-red-500/20 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showForm && (
        <ProviderForm
          provider={editingProvider}
          onClose={handleFormClose}
          onSave={handleFormSave}
        />
      )}
    </div>
  )
}

