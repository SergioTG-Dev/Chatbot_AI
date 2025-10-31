'use client'

export default function SystemStatus() {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h3 className="text-lg font-semibold mb-3">Estado del Sistema</h3>
      <div className="space-y-2 text-sm">
        <div className="flex items-center justify-between">
          <span>Chatbot</span>
          <span className="flex items-center gap-2 text-green-600">
            <span className="w-2 h-2 rounded-full bg-green-600" /> Activo
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span>Turnos Online</span>
          <span className="flex items-center gap-2 text-green-600">
            <span className="w-2 h-2 rounded-full bg-green-600" /> Disponible
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span>Derivaciones</span>
          <span className="flex items-center gap-2 text-green-600">
            <span className="w-2 h-2 rounded-full bg-green-600" /> Operativo
          </span>
        </div>
      </div>
    </div>
  )
}