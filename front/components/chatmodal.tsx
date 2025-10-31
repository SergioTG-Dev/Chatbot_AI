
import { useRef, useState } from 'react'
import { RealtimeChat } from './rasachat'
import QuickActions from './quick-actions'
import SystemStatus from './system-status'
import AppointmentModal from './appointment-modal'

interface ChatModalProps {
  onClose: () => void;
}

export default function ChatModal({ onClose }: ChatModalProps) {
  const tempRoomName = 'CiviBot-Main-Session'
  const tempUsername = 'Ciudadano'

  const sendFnRef = useRef<((content: string) => void) | null>(null)
  const [isSendingQuickAction, setIsSendingQuickAction] = useState(false)
  const [showAppointmentModal, setShowAppointmentModal] = useState(false)
  const handleQuickAction = async (payload: string) => {
    // Intercepta la acción de solicitar turno para abrir un modal local
    if (payload === '/consult_appointment') {
      setShowAppointmentModal(true)
      return
    }
    if (sendFnRef.current) {
      try {
        setIsSendingQuickAction(true)
        await sendFnRef.current(payload)
      } finally {
        setIsSendingQuickAction(false)
      }
    }
  }

  const handleAppointmentSubmit = async (data: { dni: string; departmentId: string; departmentName: string; date: string; time: string; reason: string }) => {
    setShowAppointmentModal(false)
    
    try {
      // 0) Validar que el DNI exista en el backend y obtener datos del ciudadano
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'
      const dniCheck = await fetch(`/api/citizens/${data.dni}`, { cache: 'no-store' })
      if (!dniCheck.ok) {
        const err = await dniCheck.json().catch(() => ({}))
        const detail = err?.body?.detail || 'DNI no encontrado. Debes registrarte antes de solicitar turno.'
        if (sendFnRef.current) {
          sendFnRef.current(`❌ ${detail}`)
          sendFnRef.current('ℹ️ Puedes registrarte proporcionando tu DNI, nombre y correo en el sistema.')
        }
        return
      }
      
      const citizenData = await dniCheck.json()
      
      // 0.1) Obtener datos completos del departamento (incluyendo dirección)
      const deptResponse = await fetch(`/api/departments/${data.departmentId}`, { cache: 'no-store' })
      let departmentData = null
      if (deptResponse.ok) {
        departmentData = await deptResponse.json()
      }

      // 1) Obtener procedimientos del departamento usando el ID enviado por el modal
      // Usar proxy de Next.js para procedimientos del departamento
      const deptProceduresResp = await fetch(`/api/departments/${data.departmentId}/procedures`, { cache: 'no-store' })
      if (!deptProceduresResp.ok) {
        const text = await deptProceduresResp.text().catch(() => '')
        console.warn('Procedimientos no disponibles:', deptProceduresResp.status, text)
        if (sendFnRef.current) {
          sendFnRef.current('❌ No se pudieron obtener los trámites del departamento seleccionado. Intenta más tarde.')
          sendFnRef.current('📞 Si necesitas asistencia inmediata, contacta al 4323-9400.')
        }
        return
      }
      const deptProcedures = await deptProceduresResp.json()

      if (!Array.isArray(deptProcedures) || deptProcedures.length === 0) {
        if (sendFnRef.current) {
          sendFnRef.current('ℹ️ El departamento seleccionado no tiene trámites disponibles en este momento.')
          sendFnRef.current('📞 Puedes llamar al 4323-9400 para más información.')
        }
        return
      }

      // 3) Elegir procedimiento por mapeo explícito motivo→trámite dentro del departamento
      const removeAccents = (s: string) => s?.normalize('NFD').replace(/\p{Diacritic}/gu, '')
      const norm = (s: any) => (typeof s === 'string' ? removeAccents(s.toLowerCase()) : '')

      const reason = norm(data.reason)

      // Tabla de mapeos por palabras clave → nombre del trámite
      const mappings: { [key: string]: string } = {
        // Registro Civil y DNI
        'dni': 'Solicitud de DNI',
        'documento': 'Solicitud de DNI',
        'reposicion': 'Solicitud de DNI',
        'extravio': 'Solicitud de DNI',
        'perdi': 'Solicitud de DNI',
        'partida': 'Partidas de Nacimiento',
        'nacimiento': 'Partidas de Nacimiento',
        'pasaporte': 'Pasaporte',
        // Licencias
        'licencia': 'Licencia de Conducir',
        'conducir': 'Licencia de Conducir',
        'sacar licencia': 'Licencia de Conducir',
        'renovacion': 'Renovación de Licencia',
        'renovar': 'Renovación de Licencia',
        'vencio': 'Renovación de Licencia',
        'duplicado': 'Duplicado de Licencia',
        // Impuestos
        'agip': 'AGIP – Impuestos',
        'impuesto': 'AGIP – Impuestos',
        'rentas': 'AGIP – Impuestos',
        'habilitacion': 'Habilitación Comercial',
        'habilitacion comercial': 'Habilitación Comercial',
        'comercio': 'Habilitación Comercial',
      }

      const tryMapByName = () => {
        // Orden de chequeo: coincidencia de frases completas, luego tokens individuales
        const keys = Object.keys(mappings)
        // Primero frases con espacio
        for (const k of keys.filter((x) => x.includes(' '))) {
          if (reason.includes(k)) {
            const expected = mappings[k]
            const found = deptProcedures.find((p: any) => norm(p?.name) === norm(expected))
            if (found) return found
          }
        }
        // Luego palabras
        for (const k of keys.filter((x) => !x.includes(' '))) {
          if (reason.includes(k)) {
            const expected = mappings[k]
            const found = deptProcedures.find((p: any) => norm(p?.name) === norm(expected))
            if (found) return found
          }
        }
        return null
      }

      let selectedProcedure = tryMapByName()
      // Fallback: tokens dentro del nombre del trámite
      if (!selectedProcedure) {
        const reasonTokens = reason.split(/[^a-z0-9]+/).filter((w: string) => w.length >= 3)
        selectedProcedure = deptProcedures.find((proc: any) => {
          const procName = norm(proc?.name)
          return reasonTokens.some((tk: string) => procName.includes(tk))
        })
      }
      if (!selectedProcedure) {
        selectedProcedure = deptProcedures[0]
      }
      
      if (!selectedProcedure) {
        throw new Error('No se encontró el procedimiento para el departamento seleccionado')
      }
      
      // Crear el turno en el backend
      const appointmentData = {
        procedure_id: selectedProcedure.id,
        citizen_dni: data.dni,
        scheduled_at: `${data.date}T${data.time}:00.000Z`
      }
      
      // Usar el proxy de Next.js para evitar CORS y uniformar errores
      const turnoResponse = await fetch(`/api/turnos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData)
      })
      
      if (!turnoResponse.ok) {
        const errorData = await turnoResponse.json()
        throw new Error(errorData.detail || 'Error al crear el turno')
      }
      
      const turnoCreated = await turnoResponse.json()
      
      // Mensajes de éxito con iconos
      const citizenName = `${citizenData.first_name} ${citizenData.last_name}`
      
      // Intentar obtener dirección del departamento; si falta, hacer fallback al listado
      let officeAddress: string | null = departmentData?.address || null
      if (!officeAddress) {
        try {
          const listResp = await fetch('/api/departments', { cache: 'no-store' })
          if (listResp.ok) {
            const list = await listResp.json().catch(() => [])
            const found = Array.isArray(list) ? list.find((d: any) => String(d?.id) === String(data.departmentId)) : null
            officeAddress = found?.address || null
          }
        } catch {}
      }
      const addressText = officeAddress || 'Dirección no disponible'

      // Preparar link de Google Maps usando la dirección si está disponible; si no, usar el nombre del depto
      const mapsQuery = officeAddress ? officeAddress : `${data.departmentName} Buenos Aires`
      const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(mapsQuery)}`

      const success = `✅ Turno solicitado exitosamente para ${citizenName}!`
      const details = `📋 Detalles: • Trámite: ${selectedProcedure.name} • Departamento: ${data.departmentName} • Oficina ${data.departmentName}: ${addressText} • Fecha: ${data.date} • Hora: ${data.time} • Número de confirmación: #${String(turnoCreated.id).substring(0, 8)}`
      const mapLine = `🗺️ Mapa: ${mapsUrl}`
      const followup = '📞 Si necesitas reprogramar, contacta al 4323-9400'

      if (sendFnRef.current) {
        // Enviamos los mensajes como si fueran del bot
        sendFnRef.current(success)
        sendFnRef.current(details)
        sendFnRef.current(mapLine)
        sendFnRef.current(followup)
      }
    } catch (error) {
      console.error('Error creating appointment:', error)
      
      // Mensaje de error con icono
      const errorMsg = `❌ Error al crear el turno: ${error instanceof Error ? error.message : 'Error desconocido'}`
      const fallbackMsg = '📞 Por favor, contacta al 4323-9400 para solicitar tu turno manualmente'
      
      if (sendFnRef.current) {
        sendFnRef.current(errorMsg)
        sendFnRef.current(fallbackMsg)
      }
    }
  }

  return (
    <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 z-50 h-[600px] w-[1000px] rounded-xl shadow-2xl bg-slate-50 flex flex-col overflow-hidden">
      <div className="bg-blue-50 text-slate-800 p-4 flex justify-between items-center border-b border-blue-100">
        <div className="flex items-center gap-3">
          <span className="text-lg font-bold text-blue-800">ChatBot Municipal</span>
          <span className="text-xs opacity-80">Ciudad Autónoma de Buenos Aires</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={onClose} className="ml-2 text-slate-500 hover:text-slate-700">&times;</button>
        </div>
      </div>

      <div className="flex-1 min-h-0 grid grid-cols-3 gap-4 p-4">
        {/* Panel de chat (izquierda, ocupa 2 columnas) */}
        <div className="col-span-2 bg-white rounded-xl shadow flex flex-col overflow-hidden">
          <div className="bg-blue-700 text-white p-3">
            <h3 className="font-semibold">Soy CiviBot el Asistente Virtual</h3>
            <p className="text-xs opacity-90">¿En qué puedo ayudarte hoy?</p>
          </div>
          <div className="flex-1 min-h-0">
            <RealtimeChat
              roomName={tempRoomName}
              username={tempUsername}
              exposeSendMessage={(fn) => {
                sendFnRef.current = fn
              }}
            />
          </div>
        </div>

        {/* Menú lateral (derecha) */}
        <div className="flex flex-col gap-4">
          <QuickActions onAction={handleQuickAction} loading={isSendingQuickAction} />
          <SystemStatus />
        </div>
      </div>

      {showAppointmentModal && (
        <AppointmentModal
          onClose={() => setShowAppointmentModal(false)}
          onSubmit={handleAppointmentSubmit}
        />
      )}
    </div>
  )
}