import { Button } from '@/components/ui/button'; 
import type { RasaButton } from './chat-message'; 


interface QuickReplyButtonsProps {
  buttons: RasaButton[];
  onButtonClick: (payload: string) => void;
}

export default function QuickReplyButtons({ buttons, onButtonClick }: QuickReplyButtonsProps) {
  return (
    <div className="flex flex-wrap gap-2 mt-2 max-w-[75%]"> 
      {buttons.map((button, index) => (
        <Button
          key={index}
          variant="outline"
          className="rounded-full bg-blue-500 hover:bg-blue-600 text-white border-none py-1 px-3 text-sm h-auto"
          onClick={() => onButtonClick(button.payload)}
        >
          {button.title}
        </Button>
      ))}
    </div>
  );
}