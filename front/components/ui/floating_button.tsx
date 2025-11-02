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
      {showChatModal && (
        <>
          {/* Overlay para difuminar fondo y hero cuando el modal está abierto */}
          <div
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
            aria-hidden="true"
            onClick={handleCloseChat}
          />
          <ChatModal onClose={handleCloseChat} />
        </>
      )}


      <div className="fixed bottom-6 right-6 z-50">
        
        <button
          className="relative w-16 h-16 rounded-full bg-blue-700 flex items-center justify-center shadow-xl hover:shadow-2xl transition-all"
          onClick={handleOpenChat}
          aria-label="Abrir CiviBot"
        >

          <Image
            src={robotIconPath}
            alt="CiviBot"
            width={64} 
            height={64}
            className='p-1.5'
          />
        </button>
  
      </div>
    </>
  );
}