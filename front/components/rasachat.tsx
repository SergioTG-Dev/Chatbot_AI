
'use client'

import { cn } from '@/lib/utils'
import { ChatMessageItem } from '@/components/chat-message'
import { useChatScroll } from '@/hooks/use-chat-scroll'
import {
  type ChatMessage,
  useRasaChat,} from '@/hooks/use-rasa-chat' 
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Send } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

interface RealtimeChatProps {
  roomName: string
  username: string
  onMessage?: (messages: ChatMessage[]) => void
  messages?: ChatMessage[]
  exposeSendMessage?: (fn: (content: string) => void) => void
}

/**
 * @param roomName - Nombre de la "sala" (usado como parámetro de hook, aunque Rasa usa 'sender_id')
 * @param username - El nombre de usuario que se mostrará
 * @returns El componente de chat
 */
export const RealtimeChat = ({
  roomName,
  username,
  onMessage,
  messages: initialMessages = [],
  exposeSendMessage,
}: RealtimeChatProps) => {
  const { containerRef, scrollToBottom } = useChatScroll()

  const {
    messages: rasaMessages,
    sendMessage,
    isConnected,
  } = useRasaChat({
    roomName,
    username,
  })

  const [newMessage, setNewMessage] = useState('')
  const [hasStarted, setHasStarted] = useState(false)

  const allMessages = useMemo(() => {
    const mergedMessages = [...initialMessages, ...rasaMessages] // Usamos 'rasaMessages'
    const uniqueMessages = mergedMessages.filter(
      (message, index, self) => index === self.findIndex((m) => m.id === message.id)
    )
    const toTs = (m: ChatMessage) => {
      const value = (m as any).createdAt
      if (!value) return 0
      const ts = Date.parse(value as any)
      return isNaN(ts) ? 0 : ts
    }
    const sortedMessages = uniqueMessages.sort((a, b) => {
      const diff = toTs(a) - toTs(b)
      if (diff !== 0) return diff
      return (a.id || '').localeCompare(b.id || '')
    })

    return sortedMessages
  }, [initialMessages, rasaMessages])

  useEffect(() => {
    if (onMessage) {
      onMessage(allMessages)
    }
  }, [allMessages, onMessage])

  useEffect(() => {
    scrollToBottom()
  }, [allMessages, scrollToBottom])

  // Enviar saludo inicial al abrir el chat para mostrar el mensaje de bienvenida.
  // Usamos sessionStorage para evitar doble ejecución en dev (React StrictMode) y re-montajes.
  useEffect(() => {
    if (!isConnected || allMessages.length > 0) return

    const key = `civibot:greeted:${roomName}`
    const already = typeof window !== 'undefined' ? sessionStorage.getItem(key) : '1'
    if (!already && !hasStarted) {
      setHasStarted(true)
      sessionStorage.setItem(key, '1')
      try {
        sendMessage('/greet')
      } catch (err) {
        // Si falla, el usuario puede iniciar manualmente.
      }
    }
  }, [hasStarted, isConnected, allMessages.length, sendMessage, roomName])

  const handleSendMessage = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault()
      if (!newMessage.trim() || !isConnected) return

      sendMessage(newMessage)
      setNewMessage('')
    },
    [newMessage, isConnected, sendMessage]
  )
  
  // Expone la función sendMessage al padre para acciones rápidas
  useEffect(() => {
    if (exposeSendMessage) {
      exposeSendMessage(sendMessage)
    }
  }, [exposeSendMessage, sendMessage])
  
  const handleQuickReply = useCallback(
    (payload: string) => {
      if (!isConnected) return
      
      sendMessage(payload)
    },
    [isConnected, sendMessage]
  )


  return (
    <div className="flex flex-col h-full w-full bg-background text-foreground antialiased">
      <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {allMessages.length === 0 ? null : null}
        <div className="space-y-1">
          {allMessages.map((message, index) => {
            const prevMessage = index > 0 ? allMessages[index - 1] : null
            const showHeader = !prevMessage || prevMessage.user.name !== message.user.name

            return (
              <div
                key={message.id}
                className="animate-in fade-in slide-in-from-bottom-4 duration-300"
              >
                <ChatMessageItem
                  message={message}
                  isOwnMessage={message.user.name === username}
                  showHeader={showHeader}
                  onQuickReplyClick={handleQuickReply} 
                />
              </div>
            )
          })}
        </div>
      </div>

      <form onSubmit={handleSendMessage} className="flex w-full gap-2 border-t border-border p-4">
        <Input
          className={cn(
            'rounded-full bg-background text-sm transition-all duration-300',
            isConnected && newMessage.trim() ? 'w-[calc(100%-36px)]' : 'w-full'
          )}
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          disabled={!isConnected}
        />
        {isConnected && newMessage.trim() && (
          <Button
            className="aspect-square rounded-full animate-in fade-in slide-in-from-right-4 duration-300"
            type="submit"
            disabled={!isConnected}
          >
            <Send className="size-4" />
          </Button>
        )}
      </form>
    </div>
  )
}