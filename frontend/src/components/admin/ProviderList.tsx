import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useProvidersStore } from '@/store/providersStore'
import { providersApi } from '@/services/api'
import { Plus, Edit, Trash2, Power, Loader2, CheckCircle, XCircle } from 'lucide-react'
import ProviderForm from './ProviderForm'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import type { Provider } from '@/services/api'

export default function ProviderList() {
  const { t } = useTranslation()
  const { providers, isLoading, error, fetchProviders, deleteProvider } = useProvidersStore()
  const [showForm, setShowForm] = useState(false)
  const [editingProvider, setEditingProvider] = useState<Provider | undefined>()
  const [testingProvider, setTestingProvider] = useState<string | null>(null)
  const [testResult, setTestResult] = useState<{ guid: string; success: boolean; message: string } | null>(null)

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

  const handleTestConnection = async (guid: string) => {
    setTestingProvider(guid)
    setTestResult(null)
    try {
      const result = await providersApi.testProviderConnection(guid)
      // Success: 200 OK
      setTestResult({ guid, success: true, message: result.message })
      // Clear result after 5 seconds
      setTimeout(() => setTestResult(null), 5000)
    } catch (error: any) {
      // Error: Use HTTP status code to determine success/failure
      const statusCode = error.response?.status
      const isSuccess = statusCode >= 200 && statusCode < 300
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to test connection'
      
      setTestResult({
        guid,
        success: isSuccess,
        message: errorMessage,
      })
      setTimeout(() => setTestResult(null), 5000)
    } finally {
      setTestingProvider(null)
    }
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

              {testResult?.guid === provider.guid && (
                <div
                  className={`mb-4 p-3 rounded-lg flex items-center gap-2 ${
                    testResult.success
                      ? 'bg-green-500/20 border border-green-500/50'
                      : 'bg-red-500/20 border border-red-500/50'
                  }`}
                >
                  {testResult.success ? (
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-400" />
                  )}
                  <p className={`text-sm ${testResult.success ? 'text-green-400' : 'text-red-400'}`}>
                    {testResult.message}
                  </p>
                </div>
              )}

              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(provider)}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 h-10 glass rounded-lg text-white hover:bg-white/10 transition-colors"
                >
                  <Edit className="w-4 h-4" />
                  {t('common.edit')}
                </button>
                <button
                  onClick={() => handleTestConnection(provider.guid)}
                  disabled={testingProvider === provider.guid}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 h-10 glass rounded-lg text-white hover:bg-white/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {testingProvider === provider.guid ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      {t('common.loading')}
                    </>
                  ) : (
                    <>
                      <Power className="w-4 h-4" />
                      {t('admin.testConnection')}
                    </>
                  )}
                </button>
                <button
                  onClick={() => handleDelete(provider.guid)}
                  className="flex items-center justify-center px-4 py-2 h-10 glass rounded-lg text-red-400 hover:bg-red-500/20 transition-colors"
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

