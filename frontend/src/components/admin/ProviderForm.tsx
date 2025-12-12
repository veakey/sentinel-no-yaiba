import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { X, Loader2 } from 'lucide-react'
import { useProvidersStore } from '@/store/providersStore'
import type { Provider, ProviderCreateRequest, ProviderUpdateRequest } from '@/services/api'

interface ProviderFormProps {
  provider?: Provider
  onClose: () => void
  onSave: () => void
}

export default function ProviderForm({ provider, onClose, onSave }: ProviderFormProps) {
  const { t } = useTranslation()
  const { createProvider, updateProvider, isLoading } = useProvidersStore()
  const [providerType, setProviderType] = useState<'ninja' | 'malwarebytes'>(provider?.type || 'malwarebytes')
  const [apiKey, setApiKey] = useState<string>('')
  const [formData, setFormData] = useState<ProviderCreateRequest | ProviderUpdateRequest>({
    name: provider?.name || '',
    type: provider?.type || 'malwarebytes',
    base_url: provider?.base_url || '',
    config: {
      client_id: (provider as any)?.config?.client_id || '',
      client_secret: (provider as any)?.config?.client_secret || '',
    },
    is_active: provider?.is_active ?? true,
  })

  const [authMethod, setAuthMethod] = useState<'oauth' | 'api_key'>(
    (provider as any)?.config?.client_id ? 'oauth' : 'api_key'
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      // Prepare data based on auth method
      const submitData: ProviderCreateRequest | ProviderUpdateRequest = {
        name: formData.name,
        base_url: formData.base_url || undefined,
        is_active: formData.is_active,
      }

      // Add type only for create requests
      if (!provider) {
        (submitData as ProviderCreateRequest).type = providerType
      }

      if (providerType === 'malwarebytes' && authMethod === 'oauth') {
        submitData.config = {
          client_id: formData.config?.client_id,
          client_secret: formData.config?.client_secret,
        }
      } else if (providerType === 'malwarebytes' && authMethod === 'api_key') {
        submitData.api_key = apiKey
      } else if (providerType === 'ninja') {
        submitData.api_key = apiKey
      }

      if (provider) {
        await updateProvider(provider.guid, submitData)
      } else {
        await createProvider(submitData as ProviderCreateRequest)
      }
      
      onSave()
    } catch (error) {
      console.error('Failed to save provider:', error)
      // Error is handled by the store
    }
  }

  const handleChange = (field: string, value: any) => {
    if (field === 'client_id' || field === 'client_secret') {
      setFormData((prev) => ({
        ...prev,
        config: {
          ...prev.config,
          [field]: value,
        },
      }))
    } else {
      setFormData((prev) => ({
        ...prev,
        [field]: value,
      }))
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="glass-strong rounded-xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">
            {provider ? t('admin.editProvider') : t('admin.addProvider')}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-white/80 mb-2">
              {t('admin.providerName')}
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-white/80 mb-2">
              {t('admin.providerType')}
            </label>
            <select
              value={providerType}
              onChange={(e) => {
                const newType = e.target.value as 'ninja' | 'malwarebytes'
                setProviderType(newType)
                handleChange('type', newType)
              }}
              className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              disabled={!!provider}
            >
              <option value="malwarebytes">Malwarebytes</option>
              <option value="ninja">Ninja One</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-white/80 mb-2">
              {t('admin.baseUrl')}
            </label>
            <input
              type="text"
              value={formData.base_url || ''}
              onChange={(e) => handleChange('base_url', e.target.value)}
              placeholder="https://api.malwarebytes.com"
              className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {providerType === 'malwarebytes' && (
            <div>
              <label className="block text-sm font-medium text-white/80 mb-2">
                Méthode d'authentification
              </label>
              <div className="flex gap-4 mb-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    value="oauth"
                    checked={authMethod === 'oauth'}
                    onChange={() => setAuthMethod('oauth')}
                    className="w-4 h-4"
                  />
                  <span className="text-white">OAuth2 (Client ID / Secret)</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    value="api_key"
                    checked={authMethod === 'api_key'}
                    onChange={() => setAuthMethod('api_key')}
                    className="w-4 h-4"
                  />
                  <span className="text-white">API Key (Legacy)</span>
                </label>
              </div>

              {authMethod === 'oauth' ? (
                <>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-white/80 mb-2">
                      Client ID
                    </label>
                    <input
                      type="text"
                      value={formData.config?.client_id || ''}
                      onChange={(e) => handleChange('client_id', e.target.value)}
                      className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      required={authMethod === 'oauth'}
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-white/80 mb-2">
                      Client Secret
                    </label>
                    <input
                      type="password"
                      value={formData.config?.client_secret || ''}
                      onChange={(e) => handleChange('client_secret', e.target.value)}
                      className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      required={authMethod === 'oauth'}
                    />
                  </div>
                </>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    {t('admin.apiKey')}
                  </label>
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    required={authMethod === 'api_key'}
                  />
                </div>
              )}
            </div>
          )}

          {providerType === 'ninja' && (
            <div>
              <label className="block text-sm font-medium text-white/80 mb-2">
                {t('admin.apiKey')}
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full px-4 py-2 glass rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>
          )}

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_active"
              checked={formData.is_active}
              onChange={(e) => handleChange('is_active', e.target.checked)}
              className="w-4 h-4"
            />
            <label htmlFor="is_active" className="text-sm text-white/80">
              {t('admin.isActive')}
            </label>
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="flex-1 px-4 py-2 glass rounded-lg text-white hover:bg-white/10 transition-colors disabled:opacity-50"
            >
              {t('common.cancel')}
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  {t('common.loading')}
                </>
              ) : (
                t('common.save')
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

