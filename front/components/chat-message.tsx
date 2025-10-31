
import { cn } from '@/lib/utils'
import type { ChatMessage } from '@/hooks/use-rasa-chat'
import QuickReplyButtons from './quickreplybutton' 

export interface RasaButton {
  title: string
  payload: string
}

interface ChatMessageItemProps {
  message: ChatMessage & { buttons?: RasaButton[] }
  isOwnMessage: boolean
  showHeader: boolean
  

  onQuickReplyClick: (payload: string) => void

}

export const ChatMessageItem = ({ 
  message, 
  isOwnMessage, 
  showHeader,
  onQuickReplyClick,
}: ChatMessageItemProps) => {
  
  const isBotMessage = !isOwnMessage 
  
  // Convierte URLs en enlaces clickeables manteniendo el resto como texto
  const renderWithLinks = (text: string) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g
    const parts = text.split(urlRegex)
    return parts.map((part, idx) => {
      if (urlRegex.test(part)) {
        return (
          <a
            key={`link-${idx}`}
            href={part}
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:opacity-90"
          >
            {part}
          </a>
        )
      }
      return <span key={`text-${idx}`}>{part}</span>
    })
  }
  
  return (
    <div className={`flex mt-2 ${isOwnMessage ? 'justify-end' : 'justify-start'}`}>
      <div
        className={cn('max-w-[75%] w-fit flex flex-col gap-1', {
          'items-end': isOwnMessage,
        })}
      >
        {showHeader && (
          <div
            className={cn('flex items-center gap-2 text-xs px-3', {
              'justify-end flex-row-reverse': isOwnMessage,
            })}
          >
            <span className={'font-medium'}>{message.user.name}</span>
            <span className="text-foreground/50 text-xs">
              {new Date(message.createdAt).toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true,
              })}
            </span>
          </div>
        )}
        
        <div
          className={cn(
            'py-2 px-3 rounded-xl text-sm w-fit whitespace-pre-wrap break-words',
            isOwnMessage ? 'bg-primary text-primary-foreground' : 'bg-muted text-foreground'
          )}
        >
          {renderWithLinks(message.content)}
        </div>
        
        {message.buttons && message.buttons.length > 0 && isBotMessage && (
            <QuickReplyButtons 
                buttons={message.buttons} 
                onButtonClick={onQuickReplyClick} 
            />
        )}
      </div>
    </div>
  )
}