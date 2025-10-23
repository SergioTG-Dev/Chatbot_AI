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
const RASA_API_URL = process.env.NEXT_PUBLIC_RASA_API_URL || "http://localhost:5005/webhooks/rest/webhook";


interface RasaChatProps {
  roomName: string;
  username: string;
}

export function useRasaChat({ roomName, username }: RasaChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isSending, setIsSending] = useState(false) 
  const BOT_NAME = "Agente IA BA"; 
  const SENDER_ID = roomName ? `BA-Session-${roomName}` : `BA-Session-${Math.random().toString(36).substring(2, 9)}`; 


  const sendMessage = useCallback(
    async (content: string) => {
      if (isSending || !content.trim()) return

      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        content,
        user: { name: username },
        createdAt: new Date().toISOString(),
      }

      setMessages((current) => [...current, userMessage])
      setIsSending(true)

      try {
        const response = await fetch(RASA_API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sender: SENDER_ID,
            message: content,
          }),
        })

        if (!response.ok) {
          throw new Error(`Rasa API Error: ${response.statusText}`)
        }

        const rasaResponses = await response.json()


        if (Array.isArray(rasaResponses) && rasaResponses.length > 0) {
          const botMessages: ChatMessage[] = rasaResponses.map((res, index) => ({
            id: `${userMessage.id}-bot-${index}`,
            content: res.text || "Lo siento, no tengo respuesta para eso.",
            user: { name: BOT_NAME }, 
            createdAt: new Date().toISOString(),
            buttons: res.buttons || undefined, 
          }))
          
          setMessages((current) => [...current, ...botMessages])
        }

      } catch (error) {
        console.error('Error al comunicarse con Rasa:', error)
        const errorMessage: ChatMessage = {
          id: crypto.randomUUID(),
          content: "Error: No se pudo conectar con el servicio de IA de Buenos Aires.",
          user: { name: BOT_NAME },
          createdAt: new Date().toISOString(),
        }
        setMessages((current) => [...current, errorMessage])
      } finally {
        setIsSending(false)
      }
    },
    [username, isSending, SENDER_ID]
  )

  return { messages, sendMessage, isConnected: !isSending }
}