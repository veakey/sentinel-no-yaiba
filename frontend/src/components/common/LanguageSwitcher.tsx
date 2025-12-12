import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'

export default function LanguageSwitcher() {
  const { i18n } = useTranslation()

  const languages = [
    { code: 'fr', label: 'FR' },
    { code: 'en', label: 'EN' },
  ]

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang)
  }

  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-white/60" />
      {languages.map((lang) => (
        <button
          key={lang.code}
          onClick={() => changeLanguage(lang.code)}
          className={`px-3 py-1 rounded text-sm glass-hover ${
            i18n.language === lang.code
              ? 'bg-white/20 text-white'
              : 'text-white/60 hover:text-white'
          }`}
        >
          {lang.label}
        </button>
      ))}
    </div>
  )
}

