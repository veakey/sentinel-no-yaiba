import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'
import LanguageSwitcher from '@/components/common/LanguageSwitcher'

export default function Header() {
  const { t } = useTranslation()
  const { user } = useAuthStore()

  return (
    <header className="h-16 glass border-b border-white/10 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-white">
          {t('auth.welcome')}, {user?.username}
        </h2>
        <span className="text-sm text-white/60">({user?.role})</span>
      </div>
      <LanguageSwitcher />
    </header>
  )
}

