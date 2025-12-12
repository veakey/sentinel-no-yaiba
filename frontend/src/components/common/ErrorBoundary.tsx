import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
          <div className="glass-strong rounded-xl p-8 max-w-md">
            <h2 className="text-2xl font-bold text-white mb-4">Une erreur s'est produite</h2>
            <p className="text-white/70 mb-4">
              {this.state.error?.message || 'Une erreur inattendue s\'est produite'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition"
            >
              Recharger la page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

