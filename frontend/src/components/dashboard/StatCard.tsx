import { LucideIcon } from 'lucide-react'

interface StatCardProps {
  title: string
  value: number
  icon: LucideIcon
  color: 'blue' | 'red' | 'green' | 'yellow'
}

const colorClasses = {
  blue: 'bg-blue-500/20 border-blue-500/50 text-blue-200',
  red: 'bg-red-500/20 border-red-500/50 text-red-200',
  green: 'bg-green-500/20 border-green-500/50 text-green-200',
  yellow: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-200',
}

export default function StatCard({ title, value, icon: Icon, color }: StatCardProps) {
  return (
    <div className={`glass-strong rounded-xl p-6 border ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium opacity-80">{title}</p>
        <Icon className="w-5 h-5 opacity-60" />
      </div>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  )
}

