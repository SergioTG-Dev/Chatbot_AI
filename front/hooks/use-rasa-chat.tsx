'use client'

import { useCallback, useState } from 'react'

interface RasaButton {
  title: string
  payload: string
}


export interface ChatMessage {
  id: string
  content: string
  user: {
    name: string
  }
  createdAt: string
  buttons?: RasaButton[]
}

// **URL de Rasa**
// Nota: en algunos entornos Windows, "localhost" puede resolverse de forma
// que falle la conexión desde el navegador. Usar 127.0.0.1 como valor por
// defecto mejora la compatibilidad.
const RASA_API_URL = process.env.NEXT_PUBLIC_RASA_API_URL || "http://127.0.0.1:5005/webhooks/rest/webhook";


interface RasaChatProps {
  roomName: string;
  username: string;
}

export function useRasaChat({ roomName, username }: RasaChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isSending, setIsSending] = useState(false) 
  const BOT_NAME = "CiviBot"; 
  const SENDER_ID = roomName ? `CiviBot-Session-${roomName}` : `CiviBot-Session-${Math.random().toString(36).substring(2, 9)}`; 


  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return

      // Acción local: listar trámites sin pasar por Rasa
      if (content === '/list_procedures_ui') {
        try {
          const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'
          const resp = await fetch(`${apiBase}/api/v1/procedures`)
          let text = 'No hay trámites disponibles por ahora.'
          if (resp.ok) {
            const procedures = await resp.json()
            if (Array.isArray(procedures) && procedures.length > 0) {
              const lines = ['Podés solicitar turno para:']
              for (const p of procedures.slice(0, 8)) {
                const name = p?.name ?? '(sin nombre)'
                const dept = (p?.departments && typeof p.departments === 'object') ? p.departments.name : undefined
                lines.push(dept ? `• ${name} — ${dept}` : `• ${name}`)
              }
              text = lines.join('\n')
            }
          }
          const botMessage: ChatMessage = {
            id: crypto.randomUUID(),
            content: text,
            user: { name: BOT_NAME },
            createdAt: new Date().toISOString(),
          }
          setMessages((current) => [...current, botMessage])
          return
        } catch (e) {
          const botMessage: ChatMessage = {
            id: crypto.randomUUID(),
            content: 'No pude obtener los trámites en este momento. Intenta más tarde.',
            user: { name: BOT_NAME },
            createdAt: new Date().toISOString(),
          }
          setMessages((current) => [...current, botMessage])
          return
        }
      }

      // Interceptación local para "Contactar Funcionario"
      if (content === '/request_contact_info') {
        const contactMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content: '📞 Información de Contacto:\n\n• Teléfono: 4323-9400\n• Email: info@buenosaires.gob.ar\n• Dirección: Av. de Mayo 525, CABA\n• Horario: Lunes a Viernes 8:00-18:00',
          user: { name: BOT_NAME },
          createdAt: new Date().toISOString(),
        }
        setMessages(prev => [...prev, contactMessage])
        return
      }

      // Interceptación local para "Consultar Trámites" (ask_faq)
      if (content === '/ask_faq') {
        const menuText = [
          '📄 Trámites frecuentes:',
          '',
          '• Cómo cambio el domicilio en mi DNI?',
          '• Licencia de Conducir',
          '• Cómo saco turno en un Centro de Salud (CeSAC)?',
          '',
          'Seleccioná una opción:',
        ].join('\n')

        // Enviar intents explícitos con entidad para asegurar respuesta
        const buttons: RasaButton[] = [
          { title: 'Solicitud de DNI', payload: '/faq_gcba{"process_category":"Registro Civil y DNI"}' },
          { title: 'Licencia de Conducir', payload: '/faq_gcba{"process_category":"Licencias de Conducir"}' },
          { title: 'CeSAC', payload: '/faq_gcba{"process_category":"Salud"}' },
        ]

        const botMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content: menuText,
          user: { name: BOT_NAME },
          createdAt: new Date().toISOString(),
          buttons,
        }
        setMessages(prev => [...prev, botMessage])
        return
      }

      // Interceptación local para "Reportar Emergencia"
      if (content === '/report_emergency') {
        const emergencyMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content: '🚨 Contactos de Emergencia:\n\n• Policía: 911\n• SAME (Emergencias Médicas): 107\n• Bomberos: 100\n• Defensa Civil: 103\n• Violencia de Género: 144',
          user: { name: BOT_NAME },
          createdAt: new Date().toISOString(),
        }
        setMessages(prev => [...prev, emergencyMessage])
        return
      }
      // Solo mostrar el mensaje del usuario si no es un payload (no empieza con /)
      let userMessage: ChatMessage | null = null
      if (!content.startsWith('/')) {
        const newUserMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content,
          user: { name: username },
          createdAt: new Date().toISOString(),
        }
        userMessage = newUserMessage
        setMessages((current) => [...current, newUserMessage])
      }

      // Mensaje de carga para mejorar percepción de velocidad en búsquedas de FAQ
      if (content.startsWith('/faq_gcba')) {
        const tempMsg = {
          id: crypto.randomUUID(),
          content: '⏳ Buscando información...',
          user: { name: BOT_NAME },
          createdAt: new Date().toISOString(),
        }
        setMessages((current) => [...current, tempMsg])
      }

      setIsSending(true)

      try {
        // Si el contenido empieza con '/', lo enviamos como payload
        const requestBody = content.startsWith('/') 
          ? { sender: SENDER_ID, message: content }
          : { sender: SENDER_ID, message: content }

        // Aplicar timeout más generoso y reintentar una vez si se aborta (arranque en frío de Rasa)
        const baseTimeoutMs = (content.startsWith('/greet') || content.startsWith('/faq_gcba')) ? 25000 : 15000

        const doFetch = async (ms: number) => {
          const controller = new AbortController()
          const timeoutId = setTimeout(() => controller.abort(), ms)
          try {
            return await fetch(RASA_API_URL, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(requestBody),
              signal: controller.signal,
            })
          } finally {
            clearTimeout(timeoutId)
          }
        }

        let response: Response
        try {
          response = await doFetch(baseTimeoutMs)
        } catch (err: any) {
          if (err?.name === 'AbortError') {
            // Reintento único con más tiempo
            response = await doFetch(baseTimeoutMs + 10000)
          } else {
            throw err
          }
        }

        if (!response.ok) {
          throw new Error(`Rasa API Error: ${response.statusText}`)
        }

        const rasaResponses = await response.json()

        const isFaq = content.startsWith('/faq_gcba')

        if (Array.isArray(rasaResponses) && rasaResponses.length > 0) {
          const baseId = userMessage?.id || crypto.randomUUID()
          const botMessages: ChatMessage[] = rasaResponses.map((res, index) => ({
            id: `${baseId}-bot-${index}`,
            content: res.text || "Lo siento, no tengo respuesta para eso.",
            user: { name: BOT_NAME },
            createdAt: new Date().toISOString(),
            buttons: res.buttons || undefined,
          }))
          
          // Reemplazar mensaje de carga por la respuesta final
          if (isFaq) {
            setMessages((current) => [
              ...current.filter(m => m.content !== '⏳ Buscando información...'),
              ...botMessages
            ])
          } else {
            setMessages((current) => [...current, ...botMessages])
          }
        } else {
          // Sin resultados: remover loader (si existe) y mostrar fallback amable
          const fallback: ChatMessage = {
            id: crypto.randomUUID(),
            content: 'No encontré información para esa consulta. Probá con otras palabras o elegí otra categoría.',
            user: { name: BOT_NAME },
            createdAt: new Date().toISOString(),
          }

          if (isFaq) {
            setMessages((current) => [
              ...current.filter(m => m.content !== '⏳ Buscando información...'),
              fallback,
            ])
          } else {
            setMessages((current) => [...current, fallback])
          }
        }

      } catch (error) {
        console.error('Error al comunicarse con Rasa:', error)
        const nowIso = new Date().toISOString()
        const errorContent = "Error: No se pudo conectar con CiviBot."
        const errorMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content: errorContent,
          user: { name: BOT_NAME },
          createdAt: nowIso,
        }
        // Evitar repetir el mismo mensaje de error consecutivamente
        setMessages((current) => {
          // Limpiar posible loader de FAQs si quedó visible
          const cleaned = current.filter(m => m.content !== '⏳ Buscando información...')
          const last = cleaned[cleaned.length - 1]
          if (last && last.content === errorContent) {
            return cleaned
          }
          return [...cleaned, errorMessage]
        })
      } finally {
        setIsSending(false)
      }
    },
    [username, isSending, SENDER_ID]
  )

  // Consideramos la conexión como disponible mientras la API esté accesible.
  // No bloqueamos envíos concurrentes para permitir Acciones Rápidas inmediatas.
  return { messages, sendMessage, isConnected: true }
}