import { useTranslation } from 'react-i18next'
import { mockSecurityReports } from '@/services/mockData'
import ReportCard from '@/components/reports/ReportCard'
import { FileText } from 'lucide-react'

export default function ReportsPage() {
  const { t } = useTranslation()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <FileText className="w-8 h-8 text-white" />
          <h1 className="text-3xl font-bold text-white">Rapports de sécurité</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockSecurityReports.map((report) => (
          <ReportCard key={report.id} report={report} />
        ))}
      </div>
    </div>
  )
}

