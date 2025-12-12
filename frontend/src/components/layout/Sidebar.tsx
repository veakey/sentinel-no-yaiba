import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { LayoutDashboard, Shield, Settings, LogOut } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

export default function Sidebar() {
  const { t } = useTranslation()
  const { user, logout } = useAuthStore()

  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: t('navigation.dashboard') },
    { path: '/threats', icon: Shield, label: t('navigation.threats') },
  ]

  if (user?.role === 'admin') {
    navItems.push({ path: '/admin', icon: Settings, label: t('navigation.admin') })
  }

  return (
    <aside className="w-64 glass-strong border-r border-white/10 flex flex-col">
      <div className="p-6 border-b border-white/10">
        <h1 className="text-2xl font-bold text-white">Sentinel</h1>
        <p className="text-sm text-white/60">no Yaiba</p>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg glass-hover ${
                isActive
                  ? 'bg-white/10 text-white border border-white/20'
                  : 'text-white/70 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-white/10">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg glass-hover text-white/70 hover:text-white"
        >
          <LogOut className="w-5 h-5" />
          <span>{t('common.logout')}</span>
        </button>
      </div>
    </aside>
  )
}

