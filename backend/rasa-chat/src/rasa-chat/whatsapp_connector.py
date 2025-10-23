#backend\rasa\whatsapp_connector.py
import inspect
import logging
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Callable, Awaitable

from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)

logger = logging.getLogger(__name__)

class WhatsAppConnector(InputChannel):
    """Conector personalizado para WhatsApp."""

    @classmethod
    def name(cls) -> Text:
        """Define el nombre del canal."""
        return "whatsapp"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        """Crea el blueprint de Sanic con los endpoints."""
        
        whatsapp_webhook = Blueprint(
            "whatsapp_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @whatsapp_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @whatsapp_webhook.route("/webhooks/twilio/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            """Endpoint principal donde Twilio/WhatsApp enviará los mensajes."""
            
            # Twilio envía datos como form-urlencoded, no JSON
            form_data = await request.form()
            sender_id = form_data.get("From")  # Número del usuario
            text = form_data.get("Body")       # Texto del mensaje
            input_channel = self.name()

            # Depuración: verifica que estás recibiendo los datos
            print(f"📨 Mensaje recibido de {sender_id}: {text}")

            collector = CollectingOutputChannel()

            try:
                # Enviar el mensaje a Rasa para procesamiento
                await on_new_message(
                    UserMessage(
                        text,
                        collector,
                        sender_id,
                        input_channel=input_channel,
                    )
                )
                
                # Depuración: ver las respuestas generadas
                print(f"🤖 Respuestas generadas: {collector.messages}")
                
            except Exception as e:
                logger.error(f"Error procesando mensaje: {e}")
                return response.json({"error": "Error interno del servidor"}, status=500)

            # Devolver las respuestas generadas por Rasa
            return response.json(collector.messages)

        return whatsapp_webhook