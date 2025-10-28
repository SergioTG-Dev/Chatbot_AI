'use client'; 

import Image from 'next/image';
import { useState } from 'react';
import { Button } from '@/components/ui/button'; 
import { ArrowRightIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'; 
import ChatModal from '@/components/chatmodal';

export default function Floating_button() {
  const [isOpen, setIsOpen] = useState(false);
  
  const [showChatModal, setShowChatModal] = useState(false);


  const robotIconPath = "/ChatBot.svg";

  const handleOpenChat = () => {
    setShowChatModal(true);
    setIsOpen(false);
  };
  
  const handleCloseChat = () => {
    setShowChatModal(false);
  };

  return (
    <>
      {showChatModal && <ChatModal onClose={handleCloseChat} />}


      <div className="fixed bottom-10 right-10 z-50">
        
        <button
          className="relative w-16 h-16 rounded-full bg-blue-700 flex items-center justify-center shadow-xl hover:shadow-2xl transition-all"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Abrir menú del Agente IA y WhatsApp"
        >

          <Image
            src={robotIconPath}
            alt="Agente IA de Buenos Aires"
            width={64} 
            height={64}
            className='p-1.5'
          />
        </button>

        <div 
          className={`absolute bottom-full right-0 mb-4 flex flex-col gap-3 transition-all duration-300 ease-in-out ${
            isOpen ? 'opacity-100 translate-y-0 visible' : 'opacity-0 translate-y-5 invisible'
          }`}
        >

          <Button 
            variant="default" 
            className="bg-white text-blue-700 hover:bg-gray-100" 
            onClick={handleOpenChat}
          >
            Continuar en Chat <ChatBubbleLeftRightIcon className="ml-2 w-4 h-4" />
          </Button>
          
          <Button 
            variant="default" 
            className="bg-green-500 hover:bg-green-600 text-white" 
            onClick={() => window.open('https://wa.me/', '_blank')}
          >
            Contactar por WhatsApp <ArrowRightIcon className="ml-2 w-4 h-4" /> 
          </Button>
        </div>

      </div>
    </>
  );
}