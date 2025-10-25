from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import uuid

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot Integration"]
)

# Base de datos temporal para información de trámites
tramites_db = [
    {
        "id_tramite": "TRAM-001",
        "nombre": "Licencia de conducir",
        "descripcion": "Obtención o renovación de licencia de conducir",
        "requisitos": ["DNI original", "Foto carnét", "Certificado médico", "Pago de tasas"],
        "duracion_estimada": "15 días hábiles",
        "categoria": "Licencias de Conducir",
        "estado": "activo"
    },
    {
        "id_tramite": "TRAM-002", 
        "nombre": "DNI por primera vez",
        "descripcion": "Tramitación de Documento Nacional de Identidad",
        "requisitos": ["Partida de nacimiento", "Foto digital", "Asistencia con padres/tutores"],
        "duracion_estimada": "30 días hábiles",
        "categoria": "Registro Civil y DNI",
        "estado": "activo"
    },
    {
        "id_tramite": "TRAM-003",
        "nombre": "Pasaporte",
        "descripcion": "Obtención de pasaporte para viajes internacionales",
        "requisitos": ["DNI actualizado", "Foto carnet", "Pago de arancel"],
        "duracion_estimada": "10-15 días hábiles", 
        "categoria": "Registro Civil y DNI",
        "estado": "activo"
    },
    {
        "id_tramite": "TRAM-004",
        "nombre": "Certificado de discapacidad",
        "descripcion": "Obtención de certificado único de discapacidad (CUD)",
        "requisitos": ["DNI", "Historia clínica", "Estudios médicos"],
        "duracion_estimada": "30-60 días hábiles",
        "categoria": "Salud",
        "estado": "activo"
    },
    {
        "id_tramite": "TRAM-005",
        "nombre": "Habilitación comercial",
        "descripcion": "Habilitación de local comercial o negocio",
        "requisitos": ["Planos aprobados", "Contrato de alquiler", "CUIT", "Inscripción AGIP"],
        "duracion_estimada": "30-90 días hábiles",
        "categoria": "Habilitaciones Comerciales",
        "estado": "activo"
    }
]

informacion_util_db = [
    {
        "categoria": "emergencia",
        "titulo": "Números de emergencia",
        "contenido": "Contactos de emergencia disponibles las 24 horas",
        "enlaces": ["https://emergencia.gob.ar", "https://defensacivil.gob.ar"],
        "contactos": ["911", "100", "107"]
    },
    {
        "categoria": "salud",
        "titulo": "Hospitales públicos",
        "contenido": "Red de hospitales y centros de salud pública",
        "enlaces": ["https://salud.gob.ar", "https://hospitales.gob.ar"],
        "contactos": ["0800-222-3444", "saludresponsable@gob.ar"]
    },
    {
        "categoria": "transporte",
        "titulo": "Información de transporte",
        "contenido": "Sistema de transporte público y gestión de SUBE",
        "enlaces": ["https://www.argentina.gob.ar/sube", "https://buenosaires.gob.ar/transporte"],
        "contactos": ["0800-777-SUBE", "147"]
    },
    {
        "categoria": "impuestos",
        "titulo": "Información impositiva",
        "contenido": "Consulta y pago de impuestos (ABL, Patentes, Ingresos Brutos)",
        "enlaces": ["https://www.agip.gob.ar", "https://buenosaires.gob.ar/impuestos"],
        "contactos": ["0800-999-2727", "consultas@agip.gob.ar"]
    }
]

@router.get("/tramites/", response_model=List[Dict])
async def buscar_tramites(palabra_clave: Optional[str] = None, categoria: Optional[str] = None):
    """
    Buscar trámites por palabra clave o categoría
    """
    resultados = tramites_db
    
    if palabra_clave:
        resultados = [
            tramite for tramite in resultados 
            if palabra_clave.lower() in tramite["nombre"].lower() 
            or palabra_clave.lower() in tramite["descripcion"].lower()
        ]
    
    if categoria:
        resultados = [
            tramite for tramite in resultados 
            if tramite["categoria"].lower() == categoria.lower()
        ]
    
    return resultados

@router.get("/tramites/{tramite_id}", response_model=Dict)
async def obtener_tramite(tramite_id: str):
    """
    Obtener un trámite específico por ID
    """
    for tramite in tramites_db:
        if tramite["id_tramite"] == tramite_id:
            return tramite
    raise HTTPException(status_code=404, detail="Trámite no encontrado")

@router.get("/informacion/{categoria}", response_model=List[Dict])
async def obtener_informacion_util(categoria: str):
    """
    Obtener información útil por categoría
    """
    resultados = [
        info for info in informacion_util_db 
        if info["categoria"] == categoria
    ]
    
    if not resultados:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró información para la categoría: {categoria}"
        )
    
    return resultados

@router.get("/categorias/tramites")
async def listar_categorias_tramites():
    """
    Listar todas las categorías de trámites disponibles
    """
    categorias = list(set(tramite["categoria"] for tramite in tramites_db))
    return {"categorias": categorias}

@router.get("/categorias/informacion")
async def listar_categorias_informacion():
    """
    Listar todas las categorías de información disponibles  
    """
    categorias = list(set(info["categoria"] for info in informacion_util_db))
    return {"categorias": categorias}

@router.post("/crear-ticket")
async def crear_ticket_desde_chatbot(ticket_data: Dict[str, Any]):
    """
    Crear un ticket desde el chatbot (versión simulada)
    """
    # Versión simulada - sin conexión a base de datos por ahora
    ticket_id = str(uuid.uuid4())[:8]
    return {
        "estado": "éxito",
        "mensaje": "Ticket creado exitosamente (simulado)",
        "id_ticket": ticket_id,
        "numero_seguimiento": f"TKT-{ticket_id.upper()}",
        "nota": "Esta es una versión simulada. En producción se conectaría con la base de datos."
    }

@router.post("/crear-cita")
async def crear_cita_desde_chatbot(cita_data: Dict[str, Any]):
    """
    Crear una cita desde el chatbot (versión simulada)
    """
    # Versión simulada - sin conexión a base de datos por ahora
    cita_id = str(uuid.uuid4())[:8]
    from datetime import datetime, timedelta
    
    fecha_simulada = datetime.now() + timedelta(days=7)
    
    return {
        "estado": "éxito", 
        "mensaje": "Cita creada exitosamente (simulado)",
        "id_cita": cita_id,
        "fecha": fecha_simulada.isoformat(),
        "ubicacion": cita_data.get("ubicacion", "Oficina Central"),
        "tipo_tramite": cita_data.get("tipo_tramite", "Consulta general"),
        "nota": "Esta es una versión simulada. En producción se conectaría con la base de datos."
    }

@router.get("/health")
async def health_check():
    """
    Health check para el chatbot
    """
    return {
        "status": "healthy",
        "service": "chatbot-api",
        "endpoints_activos": [
            "/chatbot/tramites/",
            "/chatbot/informacion/{categoria}",
            "/chatbot/categorias/tramites",
            "/chatbot/categorias/informacion",
            "/chatbot/crear-ticket",
            "/chatbot/crear-cita"
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }