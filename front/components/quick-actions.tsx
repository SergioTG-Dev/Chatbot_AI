'use client'

import { Button } from '@/components/ui/button'
import { Loader2 } from 'lucide-react'

interface QuickActionsProps {
  onAction: (payload: string) => void
  loading?: boolean
}

export default function QuickActions({ onAction, loading = false }: QuickActionsProps) {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
        Acciones Rápidas
        {loading && <Loader2 className="size-4 text-blue-600 animate-spin" aria-label="Enviando" />}
      </h3>
      <div className="space-y-2">
        {/* Intenta forzar intents de Rasa usando payloads */}
        <Button variant="outline" className="w-full justify-start" disabled={loading} onClick={() => onAction('/consult_appointment')}>
          📅 Solicitar Turno
        </Button>
        <Button variant="outline" className="w-full justify-start" disabled={loading} onClick={() => onAction('/ask_faq')}>
          📄 Consultar Trámites
        </Button>
        <Button variant="outline" className="w-full justify-start" disabled={loading} onClick={() => onAction('/request_contact_info')}>
          📞 Contactar Funcionario
        </Button>
        <Button variant="outline" className="w-full justify-start" disabled={loading} onClick={() => onAction('/report_emergency')}>
          🚨 Reportar Emergencia
        </Button>
      </div>
    </div>
  )
}