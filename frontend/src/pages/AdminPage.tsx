import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'
import { Navigate } from 'react-router-dom'
import ProviderList from '@/components/admin/ProviderList'

export default function AdminPage() {
  const { t } = useTranslation()
  const { user } = useAuthStore()

  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">{t('admin.title')}</h1>
      <ProviderList />
    </div>
  )
}

