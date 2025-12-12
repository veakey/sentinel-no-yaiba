import CircularProgress from './CircularProgress'
import { useTranslation } from 'react-i18next'

interface LoadingSpinnerProps {
  size?: number
  text?: string
  fullScreen?: boolean
}

export default function LoadingSpinner({
  size = 48,
  text,
  fullScreen = false,
}: LoadingSpinnerProps) {
  const { t } = useTranslation()

  const content = (
    <div className="flex flex-col items-center justify-center gap-4">
      <CircularProgress size={size} />
      {text && <p className="text-white/60 text-sm">{text}</p>}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm z-50">
        {content}
      </div>
    )
  }

  return (
    <div className="flex items-center justify-center py-12">
      {content}
    </div>
  )
}

