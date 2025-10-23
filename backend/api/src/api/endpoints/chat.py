import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from uuid import UUID
from db.supabase_client import supabase
from core.redis import redis_client
from schemas.chat import Message, MessageCreate

router = APIRouter(prefix="/chat", tags=["Chat"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: UUID):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print(f"Cliente conectado a la sesión {session_id}")

    def disconnect(self, session_id: UUID):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        print(f"Cliente desconectado de la sesión {session_id}")

    async def send_personal_message(self, message: str, session_id: UUID):
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_text(message)

manager = ConnectionManager()

@router.post("/sessions", status_code=201)
def create_chat_session(citizen_dni: str, ticket_id: UUID = None):
    citizen = supabase.table("citizens").select("id").eq("dni", citizen_dni).execute()
    if not citizen.data:
        raise HTTPException(status_code=404, detail="Citizen not found")
    
    session_data = {
        "citizen_id": citizen.data[0]["id"],
        "ticket_id": str(ticket_id) if ticket_id else None
    }
    response = supabase.table("chat_sessions").insert(session_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating chat session")
    return response.data[0]

@router.post("/sessions/{session_id}/messages", response_model=Message)
def send_message(session_id: UUID, message: MessageCreate):
    # 1. Guardar en Supabase para persistencia
    message_data = message.model_dump()
    message_data['session_id'] = str(session_id)
    response = supabase.table("chat_messages").insert(message_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error sending message")
    
    # 2. Publicar en Redis para notificación en tiempo real
    redis_message = json.dumps({
        "sender_id": str(message.sender_id),
        "sender_type": message.sender_type,
        "content": message.content,
        "timestamp": response.data[0]["timestamp"]
    })
    redis_client.publish(f"chat_channel:{session_id}", redis_message)
    
    return response.data[0]

@router.get("/sessions/{session_id}/messages", response_model=List[Message])
def get_message_history(session_id: UUID):
    response = supabase.table("chat_messages").select("*").eq("session_id", str(session_id)).order("timestamp").execute()
    return response.data

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: UUID):
    await manager.connect(websocket, session_id)
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"chat_channel:{session_id}")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await manager.send_personal_message(message['data'], session_id)
            # Mantener la conexión viva y escuchar otros mensajes si es necesario
            # Por ejemplo, si el cliente envía un mensaje directamente por WebSocket
            # data = await websocket.receive_text()
            # await manager.send_personal_message(f"Echo: {data}", session_id)
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        await pubsub.unsubscribe(f"chat_channel:{session_id}")
        await pubsub.close()