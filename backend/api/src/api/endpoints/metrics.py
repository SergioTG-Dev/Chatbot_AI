from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from ..db.supabase_client import supabase

router = APIRouter(prefix="/metrics", tags=["Metrics"])

class ChatMessageLog(BaseModel):
    session_id: Optional[str] = Field(default=None, description="ID de sesión de conversación")
    sender_id: Optional[str] = Field(default=None, description="ID del remitente (usuario/bot)")
    message_type: Literal["user","bot"]
    text: Optional[str] = None
    nlu_intent: Optional[str] = None
    nlu_confidence: Optional[float] = None
    response_time_ms: Optional[int] = None
    timestamp: Optional[str] = None

@router.post("/chat_messages", summary="Registrar mensaje de chat", description="Inserta un registro de mensaje en la tabla chat_messages de Supabase")
def log_chat_message(msg: ChatMessageLog):
    try:
        payload = msg.model_dump()
        resp = supabase.table("chat_messages").insert(payload).execute()
        return {"status": "ok", "inserted": len(resp.data or [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando mensaje: {str(e)}")

class SessionComplete(BaseModel):
    session_id: str
    completion_status: Literal["complete","incomplete"] = "complete"

@router.post("/chat_sessions/complete", summary="Marcar sesión como completada", description="Actualiza el estado de finalización de una sesión de chat")
def mark_session_complete(data: SessionComplete):
    try:
        resp = supabase.table("chat_sessions").update({
            "completion_status": data.completion_status
        }).eq("session_id", data.session_id).execute()
        return {"status": "ok", "updated": len(resp.data or [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando sesión: {str(e)}")