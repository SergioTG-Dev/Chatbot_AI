"use client"

import { useEffect, useMemo, useState } from 'react'
import { Button } from '@/components/ui/button'

interface AppointmentModalProps {
  onClose: () => void
  onSubmit: (data: { dni: string; departmentId: string; departmentName: string; date: string; time: string; reason: string }) => void
}

const ALLOWED_TIMES = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"] as const

export default function AppointmentModal({ onClose, onSubmit }: AppointmentModalProps) {
  const todayStr = useMemo(() => {
    const d = new Date()
    const yyyy = d.getFullYear()
    const mm = String(d.getMonth() + 1).padStart(2, '0')
    const dd = String(d.getDate()).padStart(2, '0')
    return `${yyyy}-${mm}-${dd}`
  }, [])

  const [departments, setDepartments] = useState<any[]>([])
  const [dni, setDni] = useState('')
  const [deptId, setDeptId] = useState<string>('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [reason, setReason] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [proceduresCheckMsg, setProceduresCheckMsg] = useState<string | null>(null)
  const [checkingProcedures, setCheckingProcedures] = useState(false)

  useEffect(() => {
    const loadDepartments = async () => {
      try {
        // Usa siempre el proxy de Next.js
        const resp = await fetch('/api/departments', { cache: 'no-store' })
        if (!resp.ok) {
          const text = await resp.text().catch(() => '')
          console.warn('Departamentos no disponibles:', resp.status, text)
          setDepartments([])
          setDeptId('')
          setError('No se pudo cargar la lista de departamentos. Intenta más tarde.')
          return
        }
        const data = await resp.json()
        const list = Array.isArray(data) ? data : []
        setDepartments(list)
        if (list.length > 0) {
          setDeptId(list[0].id)
        } else {
          setError('No hay departamentos disponibles por el momento.')
        }
      } catch (e) {
        console.error('Error loading departments:', e)
        setError('No se pudo cargar la lista de departamentos. Intenta más tarde.')
      }
    }
    loadDepartments()
  }, [])

  // Aviso: verificar si el departamento seleccionado tiene trámites
  useEffect(() => {
    const checkProcedures = async () => {
      if (!deptId) {
        setProceduresCheckMsg(null)
        return
      }
      setCheckingProcedures(true)
      setProceduresCheckMsg(null)
      try {
        const resp = await fetch(`/api/departments/${deptId}/procedures`, { cache: 'no-store' })
        if (!resp.ok) {
          const text = await resp.text().catch(() => '')
          console.warn('Verificación de trámites falló:', resp.status, text)
          setProceduresCheckMsg('No se pudieron verificar los trámites del departamento. Intenta más tarde.')
          return
        }
        const data = await resp.json()
        if (!Array.isArray(data) || data.length === 0) {
          setProceduresCheckMsg('ℹ️ Este departamento no tiene trámites disponibles por el momento.')
        } else {
          setProceduresCheckMsg(null)
        }
      } catch (e) {
        console.error('Error verificando trámites:', e)
        setProceduresCheckMsg('No se pudieron verificar los trámites del departamento. Intenta más tarde.')
      } finally {
        setCheckingProcedures(false)
      }
    }
    checkProcedures()
  }, [deptId])

  const isWeekday = (value: string) => {
    const d = new Date(value + 'T00:00:00')
    const day = d.getDay() // 0=Sun, 6=Sat
    return day >= 1 && day <= 5
  }

  const validate = () => {
    // DNI: 7-10 dígitos, sin puntos
    if (!dni || !/^\d{7,10}$/.test(dni)) return 'Ingresa un DNI válido (7-10 dígitos, solo números).'
    if (!deptId) return 'Selecciona un departamento.'
    if (!date) return 'Selecciona una fecha.'
    if (date <= todayStr) return 'La fecha debe ser posterior al día de hoy.'
    if (!isWeekday(date)) return 'Solo se permiten días de lunes a viernes.'
    if (!time) return 'Selecciona un horario.'
    if (!ALLOWED_TIMES.includes(time as any)) return 'El horario debe ser 09:00, 10:00, 11:00, 14:00, 15:00 o 16:00.'
    if (!reason.trim()) return 'Indica brevemente el motivo de la consulta.'
    return null
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const v = validate()
    if (v) {
      setError(v)
      return
    }
    setError(null)
    const selected = departments.find((d: any) => d.id === deptId)
    const deptName = selected?.name || 'Departamento'
    onSubmit({ dni, departmentId: deptId, departmentName: deptName, date, time, reason: reason.trim() })
  }

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} aria-hidden="true" />
      <div className="relative z-[61] w-[520px] rounded-xl bg-white shadow-2xl">
        <div className="px-5 py-4 border-b">
          <h2 className="text-lg font-semibold">Solicitar Turno</h2>
        </div>
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Departamento</label>
            <select
              className="w-full border rounded-md px-3 py-2"
              value={deptId}
              onChange={(e) => setDeptId(e.target.value)}
            >
              {departments.length === 0 && (
                <option value="">Cargando departamentos...</option>
              )}
              {departments.map((d: any) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
            {checkingProcedures && (
              <div className="text-xs text-gray-500 mt-1">Verificando trámites disponibles...</div>
            )}
            {proceduresCheckMsg && (
              <div className="text-xs mt-1 text-gray-700">{proceduresCheckMsg}</div>
            )}
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">DNI</label>
              <input
                type="text"
                inputMode="numeric"
                className="w-full border rounded-md px-3 py-2"
                placeholder="Ej: 12345678"
                value={dni}
                onChange={(e) => setDni(e.target.value.replace(/[^0-9]/g, ''))}
              />
              <div className="text-xs text-gray-500 mt-1">Solo números, 7-10 dígitos.</div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Fecha Preferida</label>
              <input
                type="date"
                min={todayStr}
                className="w-full border rounded-md px-3 py-2"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Horario Preferido</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={time}
                onChange={(e) => setTime(e.target.value)}
              >
                <option value="">Seleccionar horario</option>
                {ALLOWED_TIMES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Motivo de la consulta</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[80px]"
              placeholder="Describe brevemente tu consulta..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm">{error}</div>
          )}

          <div className="flex gap-2 justify-end pt-2">
            <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
            <Button type="submit" className="bg-blue-600 hover:bg-blue-700" disabled={!!proceduresCheckMsg && proceduresCheckMsg.includes('no tiene trámites')}>
              Solicitar Turno
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}