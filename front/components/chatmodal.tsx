
import { RealtimeChat } from './rasachat';

interface ChatModalProps {
  onClose: () => void;
}

export default function ChatModal({ onClose }: ChatModalProps) {
    const tempRoomName = "BA-Main-Session"; 
    const tempUsername = "Visitante BA";

    return (
        <div className="fixed bottom-10 right-15 z-50 h-[500px] w-[350px] rounded-xl shadow-2xl bg-white flex flex-col overflow-hidden">
            <div className="bg-blue-700 text-white p-4 flex justify-between items-center">
                <h2 className="text-lg font-bold">Agente IA BA</h2>
                <button onClick={onClose}>&times;</button>
            </div>

            <div className="flex-1 min-h-0">
        <RealtimeChat 
          roomName={tempRoomName}
          username={tempUsername}
        />
            </div>
        </div>
    );
}