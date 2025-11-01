# actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset, ConversationPaused, ActiveLoop
from typing import Text, List, Any, Dict
from .gcba_faqs_db import faqs_database # Base de conocimiento FAQs GCBA
import random
import re
import json
import time
from datetime import datetime
from . import ACTION_INVOCATIONS, ACTION_DURATION

faqs_database = []

try:
    from .gcba_faqs_db import faqs_database as loaded_faqs
    faqs_database = loaded_faqs
    print(f"DEBUG: FAQs cargadas exitosamente. Total: {len(faqs_database)}")
except ImportError:
    print("ADVERTENCIA CRÍTICA: No se pudo importar el módulo gcba_faqs_db. Busque el archivo en la carpeta de actions.")


class ActionSubmitAppointmentForm(Action):
    def name(self) -> Text:
        return "action_submit_appointment_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        t0 = time.time()
        cita_fecha = tracker.get_slot('date')
        
        # Aquí iría el código para llamar a una API/DB para crear la cita.
        # Simulamos una falla/éxito
        success = random.choice([True, True, True, False]) 
        
        if success:
            print(f"DEBUG: Cita creada con éxito para {cita_fecha}.")
            ACTION_INVOCATIONS.labels(action_name=self.name()).inc()
            ACTION_DURATION.labels(action_name=self.name()).observe(time.time() - t0)
            return [SlotSet("action_result", "success")] 
        else:
            print("DEBUG: Falla al crear la cita. Razón: [Simulación].")
            ACTION_INVOCATIONS.labels(action_name=self.name()).inc()
            ACTION_DURATION.labels(action_name=self.name()).observe(time.time() - t0)
            return [SlotSet("action_result", "failure")]


class ActionRescheduleAppointment(Action):
    def name(self) -> Text:
        return "action_reschedule_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cita_id = tracker.get_slot('appointment_id')
        nueva_fecha = tracker.get_slot('date') 
        
        # Aquí iría el código para llamar a una API/DB para reagendar.
        success = (cita_id is not None) and (random.random() > 0.3)
        
        if success:
            print(f"DEBUG: Cita {cita_id} reagendada para {nueva_fecha}.")
            return [SlotSet("action_result", "success")]
        else:
            print("DEBUG: Falla en el reagendamiento.")
            return [SlotSet("action_result", "failure")]

class ActionCancelAppointment(Action):
    def name(self) -> Text:
        return "action_cancel_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lógica para obtener el ID de la cita y llamar a la API de cancelación
        print("DEBUG: Procesando cancelación de cita...")
        
        # Simulación de éxito
        dispatcher.utter_message(text="Tu cita ha sido cancelada exitosamente.")
        return [AllSlotsReset()] # Limpia el historial para una nueva conversación

class ActionAskNewRescheduleDate(Action):
    def name(self) -> Text:
        return "action_ask_new_reschedule_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Por favor, indicame la **nueva fecha y hora** para la que deseas reagendar tu cita.")
        return []

class ActionCheckAppointment(Action):
    def name(self) -> Text:
        return "action_check_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Por favor, dame el ID de la cita que deseas consultar.")
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        t0 = time.time()
        # El bot indica que no entendió y ofrece opciones
        # dispatcher.utter_message(response="utter_ask_rephrase")
        # Evita repetir mensajes genéricos: sólo una instrucción y escucha
        ACTION_INVOCATIONS.labels(action_name=self.name()).inc()
        ACTION_DURATION.labels(action_name=self.name()).observe(time.time() - t0)
        return [SlotSet("action_result", None), FollowupAction("action_listen")]

class ActionDetectAppointmentRequest(Action):
    def name(self) -> Text:
        return "action_detect_appointment_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Detecta keywords de turno/cita en el texto y activa el formulario.
        Si encuentra 'turno' o 'cita', setea el slot 'appointment_request' y hace FollowupAction.
        """
        text = (tracker.latest_message.get("text") or "").lower()
        if not text:
            return []
        has_turno = "turno" in text
        has_cita = "cita" in text
        if has_turno or has_cita:
            value = "turno" if has_turno else "cita"
            # Emitimos el primer prompt del formulario para iniciar la conversación
            dispatcher.utter_message(response="utter_ask_dni")
            # Seteamos el slot y activamos el formulario
            return [
                SlotSet("appointment_request", value),
                ActiveLoop("appointment_full_form"),
                FollowupAction("appointment_full_form"),
            ]
        return []

class ActionSearchFAQ(Action):

    def name(self) -> Text:
        return "action_search_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Consulta FAQs mediante FastAPI en lugar de acceder directo a Supabase.
        Endpoint esperado: GET {FASTAPI_URL}/api/v1/faqs/search?q=&categoria=
        """
        import os
        import requests

        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        t_start = time.time()

        user_text = tracker.latest_message.get('text', '')
        text_lower = (user_text or '').lower().strip()
        # Permitir que consultas cortas capturadas como 'service_type' también filtren FAQs
        categoria_filtrada = (
            tracker.get_slot('process_category')
            or tracker.get_slot('service_type')
            or None
        )
        categoria_lower = (categoria_filtrada or '').lower().strip()

        # Si el usuario invoca la acción sin texto (p.ej., payload "/ask_faq" desde Acciones Rápidas),
        # mostramos un menú fijo de trámites frecuentes SIN consultas externas.
        try:
            if user_text.strip() == "/ask_faq":
                # Menú solicitado
                dispatcher.utter_message(
                    text=(
                        "¿Qué trámite o servicio buscás? Te puedo ayudar con los siguientes trámites frecuentes:"
                    ),
                    buttons=[
                        {
                            "title": "¿Cómo cambio el domicilio en mi DNI?",
                            "payload": "¿Cómo cambio el domicilio en mi DNI?",
                        },
                        {
                            "title": "Licencia de Conducir",
                            "payload": "Licencia de Conducir",
                        },
                        {
                            "title": "Solicitud de Partidas de Nacimiento",
                            "payload": "Solicitud de Partidas de Nacimiento",
                        },
                        {
                            "title": "Infracciones de Tránsito",
                            "payload": "Infracciones de Tránsito",
                        },
                        {
                            "title": "¿Cómo saco turno en un Centro de Salud (CeSAC)?",
                            "payload": "¿Cómo saco turno en un Centro de Salud (CeSAC)?",
                        },
                    ],
                )
                # Enviamos también una respuesta de dominio para garantizar visibilidad en canales REST
                try:
                    dispatcher.utter_message(response="utter_show_frequent_procedures")
                except Exception:
                    pass
                # Métricas de ejecución de la acción
                ACTION_INVOCATIONS.labels(action_name=self.name()).inc()
                ACTION_DURATION.labels(action_name=self.name()).observe(time.time() - t_start)
                return [SlotSet("process_category", None)]
        except Exception:
            pass

        # 1) Intento local: buscar en la base interna gcba_faqs_db.py antes de llamar a la API
        try:
            if faqs_database and (text_lower or categoria_lower):
                for faq in faqs_database:
                    try:
                        kw = ' '.join((faq.get('keywords') or [])).lower()
                        pregunta = (faq.get('pregunta') or '').lower()
                        cat = (faq.get('categoria') or '').lower()
                        local_match = False
                        if text_lower and (text_lower in pregunta or text_lower in kw):
                            local_match = True
                        if categoria_lower and categoria_lower in cat:
                            local_match = True
                        if local_match:
                            respuesta_final = (
                                f"**{faq.get('pregunta','')}**\n\n"
                                f"{faq.get('respuesta','')}\n\n"
                                f"👉 Más información aquí: {faq.get('url_referencia','s/d')}"
                            )
                            dispatcher.utter_message(text=respuesta_final)
                            # Métrica opcional del mensaje del bot
                            try:
                                intent = (tracker.latest_message.get('intent') or {}).get('name')
                                conf = (tracker.latest_message.get('intent') or {}).get('confidence')
                                t_end = time.time()
                                response_ms = int((t_end - t_start) * 1000)
                                requests.post(
                                    f"{fastapi_url}/api/v1/metrics/chat_messages",
                                    json={
                                        "session_id": tracker.sender_id,
                                        "sender_id": tracker.sender_id,
                                        "message_type": "bot",
                                        "text": respuesta_final,
                                        "nlu_intent": intent,
                                        "nlu_confidence": conf,
                                        "response_time_ms": response_ms,
                                    },
                                    timeout=5,
                                )
                            except Exception as me:
                                print(f"WARN metric ActionSearchFAQ (local): {me}")
                            return [SlotSet("process_category", None)]
                    except Exception:
                        continue
        except Exception as e:
            print(f"WARN búsqueda local en ActionSearchFAQ: {e}")

        try:
            params = {"q": user_text}
            if categoria_filtrada:
                params["categoria"] = categoria_filtrada

            resp = requests.get(f"{fastapi_url}/api/v1/faqs/search", params=params, timeout=5)
            if resp.status_code == 200:
                payload = resp.json()
                faqs = []
                # El endpoint devuelve {"faqs": [...]} según la API actual
                if isinstance(payload, dict) and "faqs" in payload:
                    faqs = payload.get("faqs", [])
                elif isinstance(payload, list):
                    faqs = payload

                if faqs:
                    best = faqs[0]
                    respuesta_final = (
                        f"**{best.get('pregunta','')}**\n\n"
                        f"{best.get('respuesta','')}\n\n"
                        f"👉 Más información aquí: {best.get('url_referencia','s/d')}"
                    )
                    dispatcher.utter_message(text=respuesta_final)
                    # Enviar métrica del mensaje de BOT
                    try:
                        intent = (tracker.latest_message.get('intent') or {}).get('name')
                        conf = (tracker.latest_message.get('intent') or {}).get('confidence')
                        t_end = time.time()
                        response_ms = int((t_end - t_start) * 1000)
                        requests.post(
                            f"{fastapi_url}/api/v1/metrics/chat_messages",
                            json={
                                "session_id": tracker.sender_id,
                                "sender_id": tracker.sender_id,
                                "message_type": "bot",
                                "text": respuesta_final,
                                "nlu_intent": intent,
                                "nlu_confidence": conf,
                                "response_time_ms": response_ms,
                            },
                            timeout=5,
                        )
                    except Exception as me:
                        print(f"WARN metric ActionSearchFAQ: {me}")
        except Exception as e:
            # Manejo de errores en la consulta a FastAPI
            try:
                print(f"ERROR FAQs FastAPI: {e}")
            except Exception:
                pass

        return [SlotSet("process_category", None)]

class ActionSetSessionComplete(Action):
    def name(self) -> Text:
        return "action_set_session_complete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import os
        import requests
        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        try:
            requests.post(
                f"{fastapi_url}/api/v1/metrics/chat_sessions/complete",
                json={
                    "session_id": tracker.sender_id,
                    "completion_status": "complete",
                },
                timeout=5,
            )
        except Exception as e:
            print(f"WARN action_set_session_complete: {e}")
        return []

class ActionRespondFAQ(Action):
    def name(self) -> Text:
        return "action_respond_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Responde FAQs usando base local (gcba_faqs_db) y fallback a FastAPI."""
        import os
        import requests

        text = (tracker.latest_message.get('text') or '').lower().strip()
        categoria = (tracker.get_slot('process_category') or '').lower().strip()

        # 1) Búsqueda simple en base local
        best = None
        if faqs_database:
            for faq in faqs_database:
                try:
                    kw = ' '.join((faq.get('keywords') or [])).lower()
                    pregunta = (faq.get('pregunta') or '').lower()
                    cat = (faq.get('categoria') or '').lower()
                    if (text and (text in pregunta or text in kw)) or (categoria and categoria in cat):
                        best = faq
                        break
                except Exception:
                    continue

        # 2) Fallback a FastAPI search si no hay match local
        if not best:
            try:
                fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
                params = {"q": text}
                if categoria:
                    params["categoria"] = categoria
                resp = requests.get(f"{fastapi_url}/api/v1/faqs/search", params=params, timeout=5)
                if resp.status_code == 200:
                    payload = resp.json()
                    faqs = []
                    if isinstance(payload, dict) and "faqs" in payload:
                        faqs = payload.get("faqs", [])
                    elif isinstance(payload, list):
                        faqs = payload
                    if faqs:
                        best = faqs[0]
            except Exception:
                pass

        if best:
            respuesta_final = (
                f"**{best.get('pregunta','')}**\n\n"
                f"{best.get('respuesta','')}\n\n"
                f"👉 Más info: {best.get('url_referencia','s/d')}"
            )
            dispatcher.utter_message(text=respuesta_final)
        # else:
        #     dispatcher.utter_message(response="utter_faq_not_found")

        return [SlotSet("process_category", None)]

class ActionListProcedures(Action):
    def name(self) -> Text:
        return "action_list_procedures"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Lista trámites disponibles consumiendo FastAPI: GET {FASTAPI_URL}/api/v1/procedures"""
        import os
        import requests

        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        try:
            resp = requests.get(f"{fastapi_url}/api/v1/procedures", timeout=10)
        except Exception:
            dispatcher.utter_message(text="No pude obtener los trámites en este momento. Intenta más tarde.")
            return []

        if resp.status_code != 200:
            dispatcher.utter_message(text="No pude obtener los trámites en este momento. Intenta más tarde.")
            return []

        try:
            procedures = resp.json() or []
        except Exception:
            procedures = []

        if not procedures:
            dispatcher.utter_message(text="No hay trámites disponibles por ahora.")
            # Señala contingencia para historias y reglas
            return [SlotSet("action_result", "no_procedures"), FollowupAction("utter_offer_alternate")]

        lines = ["Estos son algunos trámites disponibles:"]
        for p in procedures[:8]:
            name = p.get("name", "(sin nombre)")
            dept = None
            dep_obj = p.get("departments") or {}
            if isinstance(dep_obj, dict):
                dept = dep_obj.get("name")
            if dept:
                lines.append(f"• {name} — {dept}")
            else:
                lines.append(f"• {name}")

        dispatcher.utter_message(text="\n".join(lines))
        return []

class ActionDespedida(Action):
    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_goodbye")
        return [ConversationPaused()]

class ActionStartRegistration(Action):
    def name(self) -> Text:
        return "action_start_registration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_ask_first_name")
        return [SlotSet("registration_needed", "yes")]

class ActionReportEmergency(Action):
    def name(self) -> Text:
        return "action_report_emergency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Mensaje inicial con contactos críticos y pregunta de derivación
        dispatcher.utter_message(text=(
            "🔴 He detectado una situación de emergencia. "
            "Contactos inmediatos: Policía 911, SAME 107, Bomberos 100.\n"
            "Si deseas, puedo registrar un ticket de emergencia para que un operador te contacte. "
            "Por favor, describe brevemente la emergencia y ubicación."
        ))
        return [SlotSet("action_result", "success")]

class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"

    async def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"date": slot_value}

    async def validate_dni(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Valida el DNI contra la API y confirma datos del ciudadano."""
        import os
        import requests

        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")

        dni_text = str(slot_value or "").strip()
        # Normaliza: eliminar puntos y espacios
        dni_norm = ''.join(ch for ch in dni_text if ch.isdigit())
        if not dni_norm or not (7 <= len(dni_norm) <= 8):
            dispatcher.utter_message(text="El DNI ingresado no parece válido. Indicá un número de 7 u 8 dígitos.")
            return {"dni": None}

        try:
            resp = requests.get(f"{fastapi_url}/api/v1/citizens/{dni_norm}", timeout=5)
            if resp.status_code == 200:
                citizen = resp.json() or {}
                nombre = citizen.get("first_name", "")
                apellido = citizen.get("last_name", "")
                correo = citizen.get("email", "")
                # Rellena slots y pide confirmación
                dispatcher.utter_message(response="utter_confirm_found_data")
                return {"dni": dni_norm, "first_name": nombre, "last_name": apellido, "email": correo, "registration_needed": "no"}
            else:
                dispatcher.utter_message(text="No encontré tu DNI en el sistema. Vamos a registrar tus datos.")
                dispatcher.utter_message(response="utter_ask_first_name")
                return {"dni": dni_norm, "registration_needed": "yes", "first_name": None}
        except Exception as e:
            print(f"ERROR validando DNI: {e}")
            dispatcher.utter_message(text="Hubo un error al validar tu DNI. Intentá nuevamente más tarde.")
            return {"dni": None}

    async def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = (slot_value or "").strip()
        if len(val) < 2:
            dispatcher.utter_message(text="El nombre parece inválido. Indicá tu nombre nuevamente.")
            return {"first_name": None}
        dispatcher.utter_message(response="utter_ask_last_name")
        return {"first_name": val}

    async def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = (slot_value or "").strip()
        if len(val) < 2:
            dispatcher.utter_message(text="El apellido parece inválido. Indicá tu apellido nuevamente.")
            return {"last_name": None}
        dispatcher.utter_message(response="utter_ask_email")
        return {"last_name": val}

    async def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        import os
        import requests
        email = (slot_value or "").strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            dispatcher.utter_message(text="El correo ingresado no es válido. Ingresá un correo válido.")
            return {"email": None}

        # Si estamos en flujo de registro, crea ciudadano en FastAPI
        if (tracker.get_slot("registration_needed") or "") == "yes":
            fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
            dni = tracker.get_slot("dni")
            first_name = tracker.get_slot("first_name")
            last_name = tracker.get_slot("last_name")
            try:
                resp = requests.post(
                    f"{fastapi_url}/api/v1/citizens",
                    json={
                        "dni": dni,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    },
                    timeout=5,
                )
                if resp.status_code not in (200, 201):
                    dispatcher.utter_message(text="No pude registrar tu usuario. Intentá más tarde.")
                    return {"email": None}
                dispatcher.utter_message(text="Registro completado. Continuemos con tu turno.")
            except Exception as e:
                print(f"ERROR registrando ciudadano: {e}")
                dispatcher.utter_message(text="Hubo un error registrándote. Intentá más tarde.")
                return {"email": None}

        return {"email": email, "registration_needed": "no"}
    def required_slots(self, domain_slots: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
        """Inserta slots de registro si se necesita registrar ciudadano antes de agendar."""
        slots = ["service_type", "dni", "date", "time"]
        if (tracker.get_slot("registration_needed") or "") == "yes":
            # Recolectar datos antes de continuar
            slots = ["service_type", "dni", "first_name", "last_name", "email", "date", "time"]
        return slots


# ============================
# Nuevo flujo: Formulario completo de turnos
# ============================

class ValidateAppointmentFullForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_full_form"

    @staticmethod
    def _fastapi_url() -> str:
        import os
        return os.getenv("FASTAPI_URL", "http://localhost:8000")

    async def validate_dni(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        import requests
        dni_text = str(slot_value or "").strip()
        dni_norm = ''.join(ch for ch in dni_text if ch.isdigit())
        if not dni_norm or not (7 <= len(dni_norm) <= 8):
            dispatcher.utter_message(text="El DNI ingresado no es válido. Indicá un número de 7 u 8 dígitos.")
            return {"dni": None}

        try:
            resp = requests.get(f"{self._fastapi_url()}/api/v1/citizens/{dni_norm}", timeout=5)
            if resp.status_code == 200:
                citizen = resp.json() or {}
                nombre = (citizen.get("first_name", "") + " " + citizen.get("last_name", "")).strip()
                correo = citizen.get("email", "")
                dispatcher.utter_message(response="utter_confirm_found_data")
                return {"dni": dni_norm, "nombre_completo": nombre, "email": correo, "user_verified": True}
            else:
                dispatcher.utter_message(response="utter_ask_nombre_completo")
                return {"dni": dni_norm, "user_verified": False, "nombre_completo": None}
        except Exception as e:
            print(f"ERROR validate_dni: {e}")
            dispatcher.utter_message(text="Hubo un error al validar tu DNI. Intentá más tarde.")
            return {"dni": None}

    async def validate_nombre_completo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        nombre = (slot_value or "").strip()
        if len(nombre.split()) < 2:
            dispatcher.utter_message(text="Indicá nombre y apellido.")
            return {"nombre_completo": None}
        dispatcher.utter_message(response="utter_ask_email")
        return {"nombre_completo": nombre}

    async def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        import requests
        email = (slot_value or "").strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            dispatcher.utter_message(text="El correo ingresado no es válido.")
            return {"email": None}

        # Crear ciudadano si no estaba verificado
        if not tracker.get_slot("user_verified"):
            nombre = tracker.get_slot("nombre_completo") or ""
            partes = nombre.split()
            first_name = partes[0]
            last_name = " ".join(partes[1:]) or ""
            dni = tracker.get_slot("dni")
            try:
                resp = requests.post(
                    f"{self._fastapi_url()}/api/v1/citizens",
                    json={
                        "dni": dni,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    },
                    timeout=5,
                )
                if resp.status_code not in (200, 201):
                    dispatcher.utter_message(text="No pude registrar tu usuario. Intentá más tarde.")
                    return {"email": None}
                dispatcher.utter_message(text="Registro completado. Continuemos.")
            except Exception as e:
                print(f"ERROR create citizen: {e}")
                dispatcher.utter_message(text="Error registrándote. Intentá más tarde.")
                return {"email": None}

        return {"email": email, "user_verified": True}

    async def validate_department_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        import requests
        val = (slot_value or "").strip()
        if not val:
            # Mostrar departamentos disponibles
            try:
                resp = requests.get(f"{self._fastapi_url()}/api/v1/departments/", timeout=5)
                if resp.status_code == 200:
                    deps = resp.json() or []
                    if deps:
                        buttons = []
                        for d in deps[:8]:
                            buttons.append({
                                "title": d.get("name", "(sin nombre)"),
                                "payload": f"/inform{{\"department_id\":\"{d.get('id')}\"}}"
                            })
                        dispatcher.utter_message(text="Elegí el departamento:", buttons=buttons)
            except Exception as e:
                print(f"ERROR list departments: {e}")
                dispatcher.utter_message(text="No pude listar departamentos ahora.")
            return {"department_id": None}
        return {"department_id": val}

    async def validate_procedure_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        import requests
        val = (slot_value or "").strip()
        dep_id = tracker.get_slot("department_id")
        if not dep_id:
            dispatcher.utter_message(text="Primero seleccioná el departamento.")
            return {"procedure_id": None}
        if not val:
            try:
                resp = requests.get(f"{self._fastapi_url()}/api/v1/departments/{dep_id}/procedures", timeout=5)
                if resp.status_code == 200:
                    procs = resp.json() or []
                    if procs:
                        buttons = []
                        for p in procs[:8]:
                            buttons.append({
                                "title": p.get("name", "(sin nombre)"),
                                "payload": f"/inform{{\"procedure_id\":\"{p.get('id')}\"}}"
                            })
                        dispatcher.utter_message(text="Elegí el trámite:", buttons=buttons)
            except Exception as e:
                print(f"ERROR list procedures: {e}")
                dispatcher.utter_message(text="No pude listar trámites ahora.")
            return {"procedure_id": None}
        return {"procedure_id": val}

    async def validate_scheduled_at(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        val = (slot_value or "").strip()
        # Acepta "YYYY-MM-DD HH:MM"
        try:
            dt = datetime.strptime(val, "%Y-%m-%d %H:%M")
            iso = dt.isoformat() + ":00.000Z"
            return {"scheduled_at": iso}
        except Exception:
            dispatcher.utter_message(text="Formato de fecha/hora inválido. Usá 'YYYY-MM-DD HH:MM'.")
            return {"scheduled_at": None}


class ActionVerifyCitizen(Action):
    def name(self) -> Text:
        return "action_verify_citizen"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import requests, os
        dni = tracker.get_slot("dni")
        if not dni:
            dispatcher.utter_message(response="utter_ask_dni")
            return []
        try:
            fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
            resp = requests.get(f"{fastapi_url}/api/v1/citizens/{dni}", timeout=5)
            if resp.status_code == 200:
                citizen = resp.json() or {}
                nombre = (citizen.get("first_name", "") + " " + citizen.get("last_name", "")).strip()
                return [SlotSet("nombre_completo", nombre), SlotSet("email", citizen.get("email")), SlotSet("user_verified", True)]
            else:
                dispatcher.utter_message(response="utter_ask_nombre_completo")
                return [SlotSet("user_verified", False)]
        except Exception as e:
            print(f"ERROR action_verify_citizen: {e}")
            dispatcher.utter_message(text="No pude verificar tu DNI ahora.")
            return []

class ActionCreateCitizen(Action):
    def name(self) -> Text:
        return "action_create_citizen"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import requests, os
        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        dni = tracker.get_slot("dni")
        nombre = tracker.get_slot("nombre_completo") or ""
        email = tracker.get_slot("email")
        partes = nombre.split()
        first_name = partes[0] if partes else ""
        last_name = " ".join(partes[1:])
        try:
            resp = requests.post(
                f"{fastapi_url}/api/v1/citizens",
                json={"dni": dni, "first_name": first_name, "last_name": last_name, "email": email},
                timeout=5,
            )
            if resp.status_code in (200, 201):
                dispatcher.utter_message(text="Registro completado.")
                return [SlotSet("user_verified", True)]
            else:
                dispatcher.utter_message(text="No pude registrar tu usuario.")
                return []
        except Exception as e:
            print(f"ERROR action_create_citizen: {e}")
            dispatcher.utter_message(text="Error registrando ciudadano.")
            return []

class ActionFetchDepartments(Action):
    def name(self) -> Text:
        return "action_fetch_departments"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import requests, os
        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        try:
            resp = requests.get(f"{fastapi_url}/api/v1/departments/", timeout=5)
            if resp.status_code == 200:
                deps = resp.json() or []
                if not deps:
                    dispatcher.utter_message(text="No hay departamentos disponibles.")
                    return []
                buttons = []
                for d in deps[:10]:
                    buttons.append({
                        "title": d.get("name", "(sin nombre)"),
                        "payload": "/inform" + json.dumps({"department_id": d.get('id')})
                    })
                dispatcher.utter_message(text="Elegí el departamento:", buttons=buttons)
            else:
                dispatcher.utter_message(text="Error al obtener departamentos.")
        except Exception as e:
            print(f"ERROR action_fetch_departments: {e}")
            dispatcher.utter_message(text="No pude obtener departamentos.")
        return []

class ActionFetchProcedures(Action):
    def name(self) -> Text:
        return "action_fetch_procedures"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import requests, os
        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        dep_id = tracker.get_slot("department_id")
        if not dep_id:
            dispatcher.utter_message(text="Primero seleccioná el departamento.")
            return []
        try:
            resp = requests.get(f"{fastapi_url}/api/v1/departments/{dep_id}/procedures", timeout=5)
            if resp.status_code == 200:
                procs = resp.json() or []
                if not procs:
                    dispatcher.utter_message(text="Ese departamento no tiene trámites disponibles.")
                    return []
                buttons = []
                for p in procs[:10]:
                    buttons.append({
                        "title": p.get("name", "(sin nombre)"),
                        "payload": "/inform" + json.dumps({"procedure_id": p.get('id')})
                    })
                dispatcher.utter_message(text="Elegí el trámite:", buttons=buttons)
            else:
                dispatcher.utter_message(text="Error al obtener trámites del departamento.")
        except Exception as e:
            print(f"ERROR action_fetch_procedures: {e}")
            dispatcher.utter_message(text="No pude obtener trámites del departamento.")
        return []

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import requests, os
        fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
        if not tracker.get_slot("user_verified"):
            dispatcher.utter_message(text="Antes de crear el turno, necesitamos validar tus datos.")
            return []
        procedure_id = tracker.get_slot("procedure_id")
        dni = tracker.get_slot("dni")
        scheduled_at = tracker.get_slot("scheduled_at")
        if not (procedure_id and dni and scheduled_at):
            dispatcher.utter_message(text="Faltan datos para crear el turno.")
            return []
        try:
            resp = requests.post(
                f"{fastapi_url}/api/v1/turnos/",
                json={"procedure_id": procedure_id, "citizen_dni": dni, "scheduled_at": scheduled_at},
                timeout=8,
            )
            if resp.status_code in (200, 201):
                payload = resp.json() or {}
                dispatcher.utter_message(text="Turno creado exitosamente.")
                return [SlotSet("turno_id", payload.get("id"))]
            else:
                try:
                    err = resp.json()
                    msg = (err.get("detail") if isinstance(err, dict) else None) or "Error al crear el turno"
                except Exception:
                    msg = "Error al crear el turno"
                dispatcher.utter_message(text=msg)
                return []
        except Exception as e:
            print(f"ERROR action_book_appointment: {e}")
            dispatcher.utter_message(text="No pude crear el turno ahora.")
            return []
