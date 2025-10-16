"""
Base de Conocimientos - FAQs del Gobierno de la Ciudad de Buenos Aires
Estructura para PostgreSQL y Rasa
Fuente: https://buenosaires.gob.ar/gobierno/tramites
"""

# ============================================
# ESTRUCTURA DE BASE DE DATOS POSTGRESQL
# ============================================

CREATE_TABLE_SQL = """
CREATE TABLE faqs_gcba (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    subcategoria VARCHAR(100),
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    keywords TEXT[],
    url_referencia VARCHAR(500),
    tags TEXT[],
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_categoria ON faqs_gcba(categoria);
CREATE INDEX idx_keywords ON faqs_gcba USING GIN(keywords);
CREATE INDEX idx_tags ON faqs_gcba USING GIN(tags);
"""

# ============================================
# BASE DE CONOCIMIENTOS: 60+ FAQs
# ============================================

faqs_database = [
    # ===== CATEGORÍA: REGISTRO CIVIL Y DNI =====
    {
        "id": 1,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "DNI",
        "pregunta": "¿Cómo saco el DNI por primera vez?",
        "respuesta": "Para obtener tu DNI por primera vez debes: 1) Solicitar turno online en buenosaires.gob.ar/tramites/dni-identificacion-de-recien-nacido (para recién nacidos) o dni-nuevo-ejemplar (mayores de edad). 2) Concurrir con partida de nacimiento original. 3) El trámite es gratuito. 4) Tarda entre 15-30 días hábiles.",
        "keywords": ["dni", "primera vez", "sacar dni", "documento", "identificacion"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/dni-nuevo-ejemplar",
        "tags": ["dni", "identidad", "documento"]
    },
    {
        "id": 2,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "DNI",
        "pregunta": "¿Cómo cambio el domicilio en mi DNI?",
        "respuesta": "Para cambiar el domicilio: 1) Pedí turno en https://buenosaires.gob.ar/tramites/dni-cambio-de-domicilio. 2) Llevá DNI anterior y un certificado de domicilio. 3) El trámite es gratuito. 4) Retirás el nuevo DNI en 15-30 días hábiles.",
        "keywords": ["cambio domicilio", "actualizar direccion", "dni domicilio", "mudanza"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/dni-cambio-de-domicilio",
        "tags": ["dni", "domicilio", "actualizacion"]
    },
    {
        "id": 3,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "DNI",
        "pregunta": "¿Qué hago si perdí mi DNI?",
        "respuesta": "Si perdiste tu DNI: 1) Hacé la denuncia policial. 2) Pedí turno para DNI reposición en https://buenosaires.gob.ar/tramites/dni-reposicion. 3) Llevá la denuncia policial. 4) El trámite tiene un costo y demora 15-30 días hábiles.",
        "keywords": ["perdi dni", "dni robado", "dni extraviado", "reposicion dni", "denuncia"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/dni-reposicion",
        "tags": ["dni", "reposicion", "perdida"]
    },
    {
        "id": 4,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "Pasaporte",
        "pregunta": "¿Cómo tramito el pasaporte?",
        "respuesta": "Para tramitar el pasaporte: 1) Solicitá turno en https://buenosaires.gob.ar/tramites/pasaporte. 2) Completá el formulario online. 3) Llevá DNI actualizado. 4) Pagá el arancel correspondiente. 5) El pasaporte se entrega en 10-15 días hábiles.",
        "keywords": ["pasaporte", "tramitar pasaporte", "viaje exterior", "documento viaje"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/pasaporte",
        "tags": ["pasaporte", "viajes", "identidad"]
    },
    {
        "id": 5,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "Partidas",
        "pregunta": "¿Cómo inscribo el nacimiento de mi hijo/a?",
        "respuesta": "Para inscribir el nacimiento: 1) En hospitales públicos se hace automáticamente. 2) En clínicas privadas, acercate al Registro Civil con certificado médico de nacimiento. 3) Llevá DNI de ambos padres. 4) El trámite es gratuito y se hace en el momento.",
        "keywords": ["inscripcion nacimiento", "partida nacimiento", "registrar bebe", "recien nacido"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inscripcion-del-nacimiento",
        "tags": ["registro civil", "nacimiento", "partidas"]
    },

    # ===== CATEGORÍA: LICENCIAS DE CONDUCIR =====
    {
        "id": 6,
        "categoria": "Licencias de Conducir",
        "subcategoria": "Renovación",
        "pregunta": "¿Cómo renuevo mi licencia de conducir?",
        "respuesta": "Para renovar la licencia: 1) Pedí turno en https://buenosaires.gob.ar/tramites/renovacion-de-licencia-de-conducir. 2) Hacé el examen médico online o presencial. 3) Pagá el arancel. 4) Concurrí al turno con DNI y licencia anterior. 5) Retirás la nueva en el momento o por correo.",
        "keywords": ["renovar licencia", "licencia vencida", "renovacion conducir", "registro conducir"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/renovacion-de-licencia-de-conducir",
        "tags": ["licencia", "conducir", "renovacion"]
    },
    {
        "id": 7,
        "categoria": "Licencias de Conducir",
        "subcategoria": "Primera Licencia",
        "pregunta": "¿Cómo obtengo mi primera licencia de conducir?",
        "respuesta": "Para la primera licencia: 1) Pedí turno en https://buenosaires.gob.ar/tramites/otorgamiento-de-licencia-de-conducir. 2) Rendí examen teórico online. 3) Hacé el examen médico. 4) Rendí examen práctico de manejo. 5) Pagá el arancel. 6) Debes tener mínimo 17 años.",
        "keywords": ["primera licencia", "sacar licencia", "aprender a manejar", "licencia nueva", "examen conducir"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/otorgamiento-de-licencia-de-conducir",
        "tags": ["licencia", "primera vez", "conducir"]
    },
    {
        "id": 8,
        "categoria": "Licencias de Conducir",
        "subcategoria": "Duplicado",
        "pregunta": "¿Cómo saco un duplicado de licencia por robo o extravío?",
        "respuesta": "Para duplicado por pérdida: 1) Hacé denuncia policial. 2) Pedí turno en https://buenosaires.gob.ar/tramites/duplicado-de-licencia-de-conducir. 3) Llevá DNI y denuncia. 4) Pagá el arancel. 5) Se entrega en el momento o por correo en 48-72hs.",
        "keywords": ["duplicado licencia", "licencia robada", "perdi licencia", "extraviar licencia"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/duplicado-de-licencia-de-conducir",
        "tags": ["licencia", "duplicado", "perdida"]
    },
    {
        "id": 9,
        "categoria": "Licencias de Conducir",
        "subcategoria": "Consultas",
        "pregunta": "¿Cómo consulto los puntos de mi licencia?",
        "respuesta": "Para consultar puntos: 1) Ingresá a https://buenosaires.gob.ar/tramites/consulta-de-puntaje-en-licencia-de-conducir. 2) Ingresá con tu CUIT/CUIL o número de licencia. 3) Podés ver tu puntaje actual, infracciones y estado de la licencia. Es gratuito y online.",
        "keywords": ["puntos licencia", "consultar puntos", "puntaje conducir", "infracciones"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/consulta-de-puntaje-en-licencia-de-conducir",
        "tags": ["licencia", "puntos", "consulta"]
    },

    # ===== CATEGORÍA: INFRACCIONES DE TRÁNSITO =====
    {
        "id": 10,
        "categoria": "Infracciones de Tránsito",
        "subcategoria": "Consulta",
        "pregunta": "¿Cómo consulto si tengo multas de tránsito?",
        "respuesta": "Para consultar multas: 1) Ingresá a https://buenosaires.gob.ar/tramites/consulta-de-infracciones. 2) Poné patente o DNI. 3) Verás todas las infracciones, montos y vencimientos. 4) Podés pagar online con tarjeta o generar VEP.",
        "keywords": ["multas transito", "consultar multas", "infracciones auto", "fotomultas", "verificar multas"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/consulta-de-infracciones",
        "tags": ["infracciones", "multas", "transito"]
    },
    {
        "id": 11,
        "categoria": "Infracciones de Tránsito",
        "subcategoria": "Descargo",
        "pregunta": "¿Cómo hago un descargo por una multa?",
        "respuesta": "Para presentar descargo: 1) Ingresá a https://buenosaires.gob.ar/tramites/solicitud-de-descargo-por-infracciones-de-transito. 2) Completá el formulario online dentro de los 15 días de notificado. 3) Adjuntá pruebas (fotos, documentos). 4) Te responden en 30-60 días hábiles por email.",
        "keywords": ["descargo multa", "apelar multa", "reclamar infraccion", "defensa multa"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-descargo-por-infracciones-de-transito",
        "tags": ["infracciones", "descargo", "defensa"]
    },
    {
        "id": 56,
        "categoria": "Obras y Construcción",
        "subcategoria": "Demolición",
        "pregunta": "¿Cómo tramito un permiso de demolición?",
        "respuesta": "Para demoler: 1) Ingresá a https://buenosaires.gob.ar/tramites/solicitud-de-permiso-de-demolicion. 2) Presentá planos firmados por profesional. 3) Certificado de no inhabitabilidad. 4) Estudio de impacto sobre edificios linderos. 5) Seguro de responsabilidad civil. 6) Vallado y señalización obligatorios. 7) Inspector aprueba antes de iniciar. 8) Plazo máximo de obra según superficie.",
        "keywords": ["demolicion", "permiso demoler", "derribar edificio", "tirar casa"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-permiso-de-demolicion",
        "tags": ["obras", "demolicion", "permisos"]
    },
    {
        "id": 57,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "Género",
        "pregunta": "¿Cómo cambio el nombre y género en mi DNI?",
        "respuesta": "Para rectificar género y nombre: 1) Ingresá a https://buenosaires.gob.ar/tramites/tramites-solicitud-de-rectificacion-de-genero-y-prenombre-en-partida-de-nacimiento. 2) Completás declaración jurada (no necesita diagnóstico médico). 3) Elegís nuevo nombre. 4) Se modifica partida de nacimiento. 5) Con eso tramitás nuevo DNI. 6) Es gratuito y confidencial. Ley de Identidad de Género garantiza este derecho.",
        "keywords": ["cambio genero", "cambio nombre", "identidad genero", "dni trans", "rectificacion genero"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/tramites-solicitud-de-rectificacion-de-genero-y-prenombre-en-partida-de-nacimiento",
        "tags": ["identidad", "genero", "derechos"]
    },
    {
        "id": 58,
        "categoria": "Trabajo",
        "subcategoria": "Documentación",
        "pregunta": "¿Cómo rúbrico los libros laborales de mi empresa?",
        "respuesta": "Para rúbrica de libros: 1) DIGITAL: https://buenosaires.gob.ar/tramites/alta-de-rubrica-digital-en-el-registro-de-documentacion-laboral. 2) MANUAL: para PYMES. 3) Necesitás estar inscripto en el Registro de Empleadores. 4) Libros: sueldos, jornales, personal, inspecciones. 5) Presentás en Dirección de Trabajo. 6) Es obligatorio y gratuito.",
        "keywords": ["rubrica libros", "libros laborales", "libro sueldos", "empleador"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/alta-de-rubrica-digital-en-el-registro-de-documentacion-laboral",
        "tags": ["trabajo", "empleadores", "documentacion"]
    },
    {
        "id": 59,
        "categoria": "Desarrollo Social",
        "subcategoria": "Violencia",
        "pregunta": "¿Dónde pedir ayuda por violencia de género?",
        "respuesta": "Recursos por violencia de género: 1) Línea 144 (24hs, gratuita, nacional). 2) Centros Integrales de la Mujer (CIM) en cada comuna. 3) Refugios para víctimas. 4) Asesoramiento legal y psicológico gratuito. 5) Botón antipánico. 6) Subsidio habitacional de emergencia. 7) En emergencia: 911. Todo confidencial y sin costo.",
        "keywords": ["violencia genero", "linea 144", "refugio mujeres", "ayuda violencia", "maltrato"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["violencia genero", "emergencia", "ayuda"]
    },
    {
        "id": 60,
        "categoria": "Salud",
        "subcategoria": "Vacunación",
        "pregunta": "¿Dónde me puedo vacunar gratuitamente?",
        "respuesta": "Vacunación gratuita en CABA: 1) Centros de Salud (CeSAC). 2) Hospitales públicos. 3) Vacunatorios específicos. 4) Calendario obligatorio: bebés, niños, adolescentes, adultos mayores. 5) Vacunas especiales: fiebre amarilla, antigripal, COVID-19. 6) Llevá DNI y carnet de vacunación. 7) Consultá vacunatorios en https://buenosaires.gob.ar. No necesitás turno para vacunación.",
        "keywords": ["vacunas", "vacunacion gratuita", "calendario vacunacion", "donde vacunarme", "vacuna gratis"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["salud", "vacunacion", "prevencion"]
    },
    {
        "id": 61,
        "categoria": "Transporte",
        "subcategoria": "Bicicletas",
        "pregunta": "¿Cómo uso el sistema de bicicletas públicas EcoBici?",
        "respuesta": "Para usar EcoBici: 1) Registrate en la app 'BA EcoBici' con DNI. 2) Es gratuito para residentes de CABA. 3) Retirás bici en cualquier estación con tu usuario. 4) Tenés 60 minutos de uso. 5) Devolvés en cualquier estación. 6) Hay más de 400 estaciones en la Ciudad. 7) También hay bicicletas eléctricas en algunas estaciones.",
        "keywords": ["ecobici", "bicicletas publicas", "bicisenda", "bici gratis", "transporte sustentable"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["transporte", "bicicletas", "movilidad"]
    },
    {
        "id": 62,
        "categoria": "Medio Ambiente",
        "subcategoria": "Denuncias",
        "pregunta": "¿Cómo denuncio contaminación o problemas ambientales?",
        "respuesta": "Para denunciar problemas ambientales: 1) Llamá al 147. 2) Denunciá: ruidos molestos, humo, olores, basurales clandestinos, contaminación de agua, maltrato animal. 3) Agencia de Protección Ambiental inspecciona. 4) Para fauna: 0800-999-2727. 5) Podés hacer seguimiento online del reclamo. 6) Multas y sanciones según gravedad.",
        "keywords": ["contaminacion", "denuncia ambiental", "ruidos molestos", "basural", "medio ambiente"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["medio ambiente", "denuncias", "contaminacion"]
    },
    {
        "id": 63,
        "categoria": "Cultura",
        "subcategoria": "Museos",
        "pregunta": "¿Qué museos de la Ciudad son gratuitos?",
        "respuesta": "Museos gratuitos en CABA: 1) Museo de Arte Moderno (MAMBA). 2) Museo Sívori. 3) Museo Larreta. 4) Museo Fernández Blanco. 5) Casa de Ricardo Rojas. 6) Museos históricos de barrio. 7) Algunos tienen horarios de entrada gratuita específicos. 8) Muchos ofrecen visitas guiadas sin costo. Consultá horarios en https://buenosaires.gob.ar",
        "keywords": ["museos gratis", "museos gratuitos", "visitar museos", "cultura gratis"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["cultura", "museos", "turismo"]
    },
    {
        "id": 64,
        "categoria": "Educación",
        "subcategoria": "Universidad",
        "pregunta": "¿Hay becas universitarias del Gobierno de la Ciudad?",
        "respuesta": "Becas universitarias en CABA: 1) Becas para carreras estratégicas (ingeniería, tecnología, salud): https://buenosaires.gob.ar/tramites/beca-para-carreras-estrategicas-de-nivel-superior. 2) Estudiar es Trabajar: beca + trabajo. 3) Cobertura: matrícula, materiales, transporte. 4) Requisitos: vivir en CABA, promedio mínimo, ingresos familiares limitados. 5) Convocatorias anuales. 6) También hay becas para nivel terciario.",
        "keywords": ["becas universitarias", "ayuda universitaria", "beca estudio", "estudiar trabajar"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/beca-para-carreras-estrategicas-de-nivel-superior",
        "tags": ["educacion", "becas", "universidad"]
    },
    {
        "id": 65,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "Clave Ciudad",
        "pregunta": "¿Cómo obtengo la Clave Ciudad?",
        "respuesta": "Para obtener Clave Ciudad: 1) Ingresá a https://buenosaires.gob.ar/tramites/obtencion-clave-ciudad. 2) Completás formulario con CUIL/CUIT. 3) Creás usuario y contraseña. 4) Validás identidad con DNI. 5) Con Clave Ciudad accedés a: trámites online, consulta de impuestos, AGIP, turnos, gestiones electrónicas. 6) Es personal e intransferible.",
        "keywords": ["clave ciudad", "usuario clave ciudad", "registrarse clave ciudad", "login gcba"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/obtencion-clave-ciudad",
        "tags": ["tramites digitales", "clave ciudad", "acceso"]
    },
    {
        "id": 12,
        "categoria": "Infracciones de Tránsito",
        "subcategoria": "Denuncia de Venta",
        "pregunta": "¿Cómo denuncio que vendí mi auto si me llegan multas?",
        "respuesta": "Para denuncia de venta: 1) Ingresá a https://buenosaires.gob.ar/tramites/denuncia-de-venta-de-dominio. 2) Completá formulario con datos del comprador. 3) Adjuntá copia del título o formulario 08. 4) Las multas posteriores a la fecha de venta se transfieren al nuevo titular.",
        "keywords": ["denuncia venta", "vendi auto", "transferir multas", "cambio titular"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/denuncia-de-venta-de-dominio",
        "tags": ["infracciones", "venta", "automotor"]
    },

    # ===== CATEGORÍA: SALUD =====
    {
        "id": 13,
        "categoria": "Salud",
        "subcategoria": "Turnos",
        "pregunta": "¿Cómo saco turno en un Centro de Salud (CeSAC)?",
        "respuesta": "Para turnos en CeSAC: 1) Ingresá a https://buenosaires.gob.ar/tramites/solicitud-de-turnos-en-centros-de-salud-y-accion-comunitaria-cesac. 2) Elegí el CeSAC más cercano. 3) Seleccioná especialidad y horario. 4) Confirmá con tu DNI. 5) También podés llamar al 147 o ir personalmente.",
        "keywords": ["turno cesac", "centro salud", "turno medico", "atencion primaria", "medico gratis"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-turnos-en-centros-de-salud-y-accion-comunitaria-cesac",
        "tags": ["salud", "turnos", "cesac"]
    },
    {
        "id": 14,
        "categoria": "Salud",
        "subcategoria": "Certificado Discapacidad",
        "pregunta": "¿Cómo tramito el Certificado de Discapacidad?",
        "respuesta": "Para el Certificado de Discapacidad: 1) Pedí turno en https://buenosaires.gob.ar/tramites/solicitud-de-certificado-medico-oficial-cmo-para-personas-con-discapacidad. 2) Llevá historia clínica y estudios médicos. 3) Una junta médica evaluará tu caso. 4) El certificado habilita acceso a pensiones, transporte gratuito y otros beneficios.",
        "keywords": ["certificado discapacidad", "cud", "pension discapacidad", "junta medica"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-certificado-medico-oficial-cmo-para-personas-con-discapacidad",
        "tags": ["salud", "discapacidad", "certificado"]
    },

    # ===== CATEGORÍA: IMPUESTOS Y AGIP =====
    {
        "id": 15,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "ABL",
        "pregunta": "¿Cómo consulto y pago el Impuesto Inmobiliario (ABL)?",
        "respuesta": "Para consultar y pagar ABL: 1) Ingresá a https://buenosaires.gob.ar/tramites/inmobiliario-abl-consulta-de-boletas-saldos-y-deuda. 2) Poné partida inmobiliaria o domicilio. 3) Verás todas las cuotas y deudas. 4) Pagá online con tarjeta, débito automático o generá VEP para Rapipago/Pago Fácil.",
        "keywords": ["abl", "impuesto inmobiliario", "pagar abl", "inmueble", "propiedad"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inmobiliario-abl-consulta-de-boletas-saldos-y-deuda",
        "tags": ["impuestos", "abl", "inmobiliario"]
    },
    {
        "id": 16,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "Patentes",
        "pregunta": "¿Cómo pago la patente del auto?",
        "respuesta": "Para pagar patentes: 1) Consultá en https://buenosaires.gob.ar/tramites/patentes-automotores-consulta-de-boletas-saldos-y-deuda. 2) Ingresá patente o dominio. 3) Verás cuotas y deudas. 4) Pagá online, débito automático o en puntos de pago. 5) El pago se acredita en 48-72hs.",
        "keywords": ["patente auto", "pagar patente", "impuesto automotor", "vehiculo"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/patentes-automotores-consulta-de-boletas-saldos-y-deuda",
        "tags": ["impuestos", "patentes", "automotor"]
    },
    {
        "id": 17,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "Ingresos Brutos",
        "pregunta": "¿Cómo me inscribo en Ingresos Brutos?",
        "respuesta": "Para inscripción en Ingresos Brutos: 1) Ingresá con Clave Ciudad en https://www.agip.gob.ar. 2) Completá formulario con actividad económica. 3) Declarás si sos Convenio Multilateral o Local. 4) La inscripción es gratuita. 5) Después debés presentar DDJJ mensual o anual según régimen.",
        "keywords": ["ingresos brutos", "iibb", "inscripcion comercio", "monotributo ciudad", "actividad economica"],
        "url_referencia": "https://www.agip.gob.ar",
        "tags": ["impuestos", "ingresos brutos", "comercio"]
    },
    {
        "id": 18,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "Jubilados",
        "pregunta": "¿Los jubilados tienen exención de ABL?",
        "respuesta": "Sí, jubilados y pensionados pueden solicitar exención: 1) Ingresá a https://buenosaires.gob.ar/tramites/inmobiliario-abl-solicitud-de-exencion-jubilados-y-pensionados. 2) Requisitos: ser propietario, vivir en la propiedad, tener ingresos menores al límite establecido. 3) Llevá DNI, título de propiedad, recibo de jubilación. 4) La exención puede ser del 50% o 100%.",
        "keywords": ["exencion abl", "jubilados abl", "descuento jubilados", "pension abl"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inmobiliario-abl-solicitud-de-exencion-jubilados-y-pensionados",
        "tags": ["impuestos", "exencion", "jubilados"]
    },

    # ===== CATEGORÍA: HABILITACIONES COMERCIALES =====
    {
        "id": 19,
        "categoria": "Habilitaciones Comerciales",
        "subcategoria": "Habilitación",
        "pregunta": "¿Cómo habilito un local comercial?",
        "respuesta": "Para habilitar un local: 1) Consultá si el rubro está permitido en esa ubicación. 2) Ingresá a https://buenosaires.gob.ar/tramites/autorizacion-de-actividades-economicas. 3) Presentá planos, contrato de alquiler, CUIT, inscripción AGIP. 4) AGC inspecciona el local. 5) Pagás tasas y obtenés la habilitación. Demora 30-90 días.",
        "keywords": ["habilitar local", "habilitacion comercial", "abrir negocio", "permiso comercio"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/autorizacion-de-actividades-economicas",
        "tags": ["habilitaciones", "comercio", "agc"]
    },
    {
        "id": 20,
        "categoria": "Habilitaciones Comerciales",
        "subcategoria": "Consultas",
        "pregunta": "¿Cómo saber si puedo poner mi tipo de negocio en determinado lugar?",
        "respuesta": "Para consultar usos: 1) Ingresá a https://buenosaires.gob.ar/tramites/consulta-de-usos. 2) Poné la dirección exacta. 3) El sistema te dirá qué rubros están permitidos. 4) Algunos requieren capacidad de carga, otros tienen restricciones. 5) Es gratuito y online.",
        "keywords": ["consulta usos", "rubros permitidos", "codigo urbanistico", "actividad permitida"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/consulta-de-usos",
        "tags": ["habilitaciones", "consulta", "usos"]
    },
    {
        "id": 21,
        "categoria": "Habilitaciones Comerciales",
        "subcategoria": "Gastronomía",
        "pregunta": "¿Qué necesito para habilitar un restaurante o bar?",
        "respuesta": "Para gastronomía: 1) Consulta de usos favorable. 2) Curso de Manipulación de Alimentos. 3) Planos aprobados con extracción, baños, cocina. 4) Habilitación AGC. 5) Inscripción Bromatológica. 6) Sistema contra incendios. 7) Si hay música en vivo, permiso adicional. 8) Todo el trámite demora 60-120 días.",
        "keywords": ["habilitar restaurante", "bar habilitacion", "gastronomia", "manipulacion alimentos"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inscripcion-al-curso-de-manipulacion-de-alimentos",
        "tags": ["habilitaciones", "gastronomia", "alimentos"]
    },

    # ===== CATEGORÍA: EDUCACIÓN =====
    {
        "id": 22,
        "categoria": "Educación",
        "subcategoria": "Boleto Estudiantil",
        "pregunta": "¿Cómo tramito el Boleto Estudiantil?",
        "respuesta": "Para el Boleto Estudiantil: 1) Tu escuela debe estar inscripta en el programa. 2) Ingresá a https://buenosaires.gob.ar/tramites/boleto-estudiantil. 3) Cargá tus datos y los de tu establecimiento. 4) Esperá la habilitación (48-72hs). 5) Cargás la tarjeta SUBE desde la app o en estaciones. 6) Tenés viajes gratis en transporte público.",
        "keywords": ["boleto estudiantil", "sube estudiante", "transporte gratis", "pase escolar"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/boleto-estudiantil",
        "tags": ["educacion", "transporte", "estudiantes"]
    },
    {
        "id": 23,
        "categoria": "Educación",
        "subcategoria": "Inscripción",
        "pregunta": "¿Cómo inscribo a mi hijo/a en una escuela pública?",
        "respuesta": "Para inscripción escolar: 1) En febrero-marzo se abre la inscripción online en https://buenosaires.gob.ar/tramites/inscripcion-en-linea-para-vacantes-estudiantiles. 2) Elegís hasta 10 escuelas. 3) El sistema asigna vacantes por cercanía y disponibilidad. 4) Te notifican por email. 5) Confirmás presencialmente con DNI y partida de nacimiento.",
        "keywords": ["inscripcion escolar", "escuela publica", "vacante escolar", "primaria", "secundaria"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inscripcion-en-linea-para-vacantes-estudiantiles",
        "tags": ["educacion", "inscripcion", "escuelas"]
    },

    # ===== CATEGORÍA: DESARROLLO SOCIAL =====
    {
        "id": 24,
        "categoria": "Desarrollo Social",
        "subcategoria": "Ciudadanía Porteña",
        "pregunta": "¿Qué es y cómo me inscribo en Ciudadanía Porteña?",
        "respuesta": "Ciudadanía Porteña es una ayuda económica mensual. Para inscribirte: 1) Debés vivir en CABA hace más de 2 años. 2) Tener ingresos bajos. 3) Ingresá a https://buenosaires.gob.ar/tramites/programa-ciudadania-portena. 4) Completá formulario y adjuntá DNI, comprobantes de domicilio e ingresos. 5) Te evalúan y notifican en 30-60 días.",
        "keywords": ["ciudadania portena", "ayuda economica", "subsidio", "asistencia social"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/programa-ciudadania-portena",
        "tags": ["desarrollo social", "subsidios", "ayuda"]
    },
    {
        "id": 25,
        "categoria": "Desarrollo Social",
        "subcategoria": "Ticket Social",
        "pregunta": "¿Qué es el Programa Ticket Social?",
        "respuesta": "Ticket Social entrega tarjetas para comprar alimentos. Requisitos: 1) Vivir en CABA. 2) Tener hijos menores o estar embarazada. 3) Ingresos bajos. 4) Inscribite en https://buenosaires.gob.ar/tramites/programa-ticket-social. 5) Presentás documentación en centros comunitarios. 6) La tarjeta se recarga mensualmente.",
        "keywords": ["ticket social", "tarjeta alimentos", "ayuda alimentaria", "asistencia comida"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/programa-ticket-social",
        "tags": ["desarrollo social", "alimentos", "ayuda"]
    },

    # ===== CATEGORÍA: VIVIENDA =====
    {
        "id": 26,
        "categoria": "Vivienda",
        "subcategoria": "Créditos",
        "pregunta": "¿Cómo accedo a un crédito del IVC para vivienda?",
        "respuesta": "Para créditos del IVC: 1) Ingresá a https://www.buenosaires.gob.ar/ivc. 2) Requisitos: vivir en CABA, ingresos demostrables, no tener otra propiedad. 3) Inscribite en el programa vigente. 4) Presentás documentación (DNI, recibos de sueldo, etc). 5) Te preseleccionan y asignan crédito según disponibilidad.",
        "keywords": ["credito vivienda", "ivc", "comprar casa", "prestamo vivienda"],
        "url_referencia": "https://www.buenosaires.gob.ar/ivc",
        "tags": ["vivienda", "creditos", "ivc"]
    },

    # ===== CATEGORÍA: MATRIMONIO Y UNIÓN CIVIL =====
    {
        "id": 27,
        "categoria": "Matrimonio y Unión Civil",
        "subcategoria": "Matrimonio",
        "pregunta": "¿Cómo me caso en la Ciudad de Buenos Aires?",
        "respuesta": "Para casarte: 1) Pedí turno en https://buenosaires.gob.ar/tramites/solicitud-de-turno-para-matrimonios-en-la-sede-central-del-registro-civil-o-en-sedes. 2) Ambos deben ser mayores de 18 años. 3) Llevá DNI, partida de nacimiento. 4) Elegís fecha y lugar (Registro Civil o sedes comunales). 5) La ceremonia es gratuita. Puede ser civil o con ceremonia.",
        "keywords": ["casarse", "matrimonio civil", "boda", "registro civil", "casamiento"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-turno-para-matrimonios-en-la-sede-central-del-registro-civil-o-en-sedes",
        "tags": ["registro civil", "matrimonio", "ceremonia"]
    },
    {
        "id": 28,
        "categoria": "Matrimonio y Unión Civil",
        "subcategoria": "Unión Civil",
        "pregunta": "¿Qué es la Unión Civil Convivencial y cómo la tramito?",
        "respuesta": "La Unión Civil Convivencial registra la convivencia de parejas. Para tramitarla: 1) Pedí turno en https://buenosaires.gob.ar/tramites/union-civil-convivencial. 2) Deben convivir hace más de 2 años. 3) Llevá DNI de ambos, certificado de convivencia. 4) Es gratuito. 5) Da derechos patrimoniales y sucesorios similares al matrimonio.",
        "keywords": ["union civil", "convivencia", "pareja conviviente", "concubinato"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/union-civil-convivencial",
        "tags": ["registro civil", "union civil", "convivencia"]
    },

    # ===== CATEGORÍA: TRANSPORTE =====
    {
        "id": 29,
        "categoria": "Transporte",
        "subcategoria": "SUBE",
        "pregunta": "¿Cómo gestiono mi tarjeta SUBE?",
        "respuesta": "Para gestionar tu SUBE: 1) Registrala en https://buenosaires.gob.ar/tramites/gestion-sube o en la app Mi Argentina. 2) Podés solicitar reemplazo por robo/pérdida. 3) Verificá saldo en https://www.argentina.gob.ar/sube. 4) Cargala en kioscos, estaciones o con Mercado Pago. 5) Si tenés beneficios, debés registrarte según corresponda.",
        "keywords": ["sube", "tarjeta transporte", "cargar sube", "saldo sube", "perdi sube"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/gestion-sube",
        "tags": ["transporte", "sube", "movilidad"]
    },
    {
        "id": 30,
        "categoria": "Transporte",
        "subcategoria": "Estacionamiento",
        "pregunta": "¿Cómo funciona el estacionamiento medido en CABA?",
        "respuesta": "El estacionamiento medido: 1) Funciona de lunes a viernes de 8 a 20hs y sábados de 8 a 13hs. 2) Pagás con la app 'BA Móvil' o en parquímetros. 3) Tarifa por hora según zona. 4) Las personas con discapacidad están exentas con credencial CUD. 5) Si no pagás, te pueden multar.",
        "keywords": ["estacionamiento medido", "parquimetros", "estacionar", "zona azul"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["transporte", "estacionamiento", "movilidad"]
    },

    # ===== CATEGORÍA: TAXIS Y REMISES =====
    {
        "id": 31,
        "categoria": "Taxis y Remises",
        "subcategoria": "Licencia Taxi",
        "pregunta": "¿Cómo obtengo la licencia para conducir taxi?",
        "respuesta": "Para conducir taxi: 1) Tenés que tener licencia profesional. 2) Inscribite en https://buenosaires.gob.ar/tramites/alta-de-conductor-de-taxi. 3) Curso obligatorio de capacitación. 4) Examen psicofísico especial. 5) Certificado de antecedentes. 6) La licencia de conductor se renueva anualmente.",
        "keywords": ["licencia taxi", "conductor taxi", "chofer taxi", "registro taxi"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/alta-de-conductor-de-taxi",
        "tags": ["taxis", "licencia", "transporte"]
    },
    {
        "id": 32,
        "categoria": "Taxis y Remises",
        "subcategoria": "Denuncias",
        "pregunta": "¿Cómo denuncio un problema con un taxi o remis?",
        "respuesta": "Para denunciar: 1) Ingresá a https://buenosaires.gob.ar/tramites/denuncias-por-servicio-de-taxi-y-remises. 2) Anotá número de móvil, patente, fecha y hora. 3) Describí el problema (tarifa incorrecta, mal trato, etc). 4) Podés adjuntar fotos. 5) La Dirección de Taxis investiga y sanciona si corresponde.",
        "keywords": ["denunciar taxi", "problema remis", "queja taxi", "mal servicio"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/denuncias-por-servicio-de-taxi-y-remises",
        "tags": ["taxis", "denuncias", "reclamos"]
    },

    # ===== CATEGORÍA: CULTURA =====
    {
        "id": 33,
        "categoria": "Cultura",
        "subcategoria": "Bibliotecas",
        "pregunta": "¿Cómo me hago socio de las bibliotecas públicas?",
        "respuesta": "Para asociarte a bibliotecas: 1) Acercate a cualquier biblioteca de la red con DNI. 2) Completás formulario de inscripción. 3) Es gratuito. 4) Te dan un carnet. 5) Podés pedir libros prestados, usar salas de lectura y participar de actividades culturales. Más info: https://buenosaires.gob.ar/tramites/bibliotecas",
        "keywords": ["biblioteca", "socio biblioteca", "prestamo libros", "carnet biblioteca"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/bibliotecas",
        "tags": ["cultura", "bibliotecas", "lectura"]
    },
    {
        "id": 34,
        "categoria": "Cultura",
        "subcategoria": "Proteatro",
        "pregunta": "¿Qué es Proteatro y cómo accedo?",
        "respuesta": "Proteatro ofrece entradas de teatro a precio reducido. Cómo acceder: 1) Ingresá a https://buenosaires.gob.ar/tramites/proteatro. 2) Inscribite con tu DNI. 3) Comprás por internet o en puntos de venta. 4) Entradas desde $1000-$5000 para obras en teatros comerciales e independientes. 5) Es un programa del GCBA.",
        "keywords": ["proteatro", "teatro barato", "entradas teatro", "descuento teatro"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/proteatro",
        "tags": ["cultura", "teatro", "entretenimiento"]
    },

    # ===== CATEGORÍA: TURISMO =====
    {
        "id": 35,
        "categoria": "Turismo",
        "subcategoria": "Alquileres Temporarios",
        "pregunta": "¿Cómo registro mi propiedad para alquileres temporarios turísticos?",
        "respuesta": "Para alquileres temporarios: 1) Registrate en https://buenosaires.gob.ar/tramites/inscripcion-en-el-registro-de-alquileres-temporarios. 2) Presentá título de propiedad, ABL al día. 3) Inspección del Ente de Turismo. 4) Cumplir requisitos de seguridad e higiene. 5) Obtenés número de registro obligatorio para publicar. Válido para Airbnb, Booking, etc.",
        "keywords": ["alquiler temporario", "airbnb", "alquiler turistico", "registro turistico"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inscripcion-en-el-registro-de-alquileres-temporarios",
        "tags": ["turismo", "alquileres", "hospedaje"]
    },

    # ===== CATEGORÍA: DEFENSA AL CONSUMIDOR =====
    {
        "id": 36,
        "categoria": "Defensa al Consumidor",
        "subcategoria": "Denuncias",
        "pregunta": "¿Cómo hago una denuncia por defensa del consumidor?",
        "respuesta": "Para denunciar: 1) Online en https://buenosaires.gob.ar/tramites/denuncia-online-defensa-al-consumidor. 2) Describí el problema (producto defectuoso, servicio no prestado, etc). 3) Adjuntá comprobantes, fotos, facturas. 4) Citarán a una audiencia de conciliación. 5) También podés ir presencialmente a Dirección de Defensa del Consumidor.",
        "keywords": ["denuncia consumidor", "reclamo comercio", "producto defectuoso", "garantia"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/denuncia-online-defensa-al-consumidor",
        "tags": ["consumidor", "denuncias", "reclamos"]
    },

    # ===== CATEGORÍA: ESPACIOS PÚBLICOS =====
    {
        "id": 37,
        "categoria": "Espacios Públicos",
        "subcategoria": "Reclamos",
        "pregunta": "¿Cómo reporto un problema en la vía pública?",
        "respuesta": "Para reportar problemas: 1) Llamá al 147 (atención 24hs). 2) O usá la app 'BA 147'. 3) Reportá: baches, semáforos rotos, alumbrado, limpieza, árboles caídos, etc. 4) Te dan número de reclamo. 5) Seguís el estado online. 6) Las áreas correspondientes resuelven según prioridad.",
        "keywords": ["147", "baches", "alumbrado", "semaforo roto", "basura", "arbol caido"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["espacios publicos", "reclamos", "ciudad"]
    },
    {
        "id": 38,
        "categoria": "Espacios Públicos",
        "subcategoria": "Veredas",
        "pregunta": "¿Quién es responsable de reparar las veredas?",
        "respuesta": "La responsabilidad de las veredas es del propietario del inmueble. Si hay daños por raíces: 1) Podés solicitar reparación al GCBA en https://buenosaires.gob.ar/tramites/solicitud-de-reparacion-de-veredas-rotas-por-raices. 2) El Gobierno evalúa si el daño fue causado por árboles públicos. 3) Si corresponde, GCBA se hace cargo. 4) Sino, debés repararla vos.",
        "keywords": ["veredas rotas", "reparar vereda", "baldosas rotas", "raices arboles"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-reparacion-de-veredas-rotas-por-raices",
        "tags": ["espacios publicos", "veredas", "obras"]
    },

    # ===== CATEGORÍA: MEDIO AMBIENTE =====
    {
        "id": 39,
        "categoria": "Medio Ambiente",
        "subcategoria": "Residuos",
        "pregunta": "¿Cómo funciona la separación de residuos en CABA?",
        "respuesta": "Separación de residuos: 1) VERDES: orgánicos y no reciclables. 2) NEGROS: reciclables (plásticos, papel, cartón, vidrio, metal). 3) Horarios: recolección diferenciada según barrio. 4) Consultá días en https://buenosaires.gob.ar. 5) Puntos verdes para electrónicos, aceite usado, pilas. 6) Multas por no separar o sacar basura fuera de horario.",
        "keywords": ["separacion residuos", "basura reciclable", "bolsas verdes", "puntos verdes", "reciclaje"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["medio ambiente", "residuos", "reciclaje"]
    },

    # ===== CATEGORÍA: OBRAS Y CONSTRUCCIÓN =====
    {
        "id": 40,
        "categoria": "Obras y Construcción",
        "subcategoria": "Permisos",
        "pregunta": "¿Cómo tramito un permiso de obra?",
        "respuesta": "Para permiso de obra: 1) Consultá si necesitás permiso (obras menores pueden ser por responsabilidad profesional). 2) Ingresá a https://buenosaires.gob.ar/tramites/permiso-para-ejecucion-de-obra-civil. 3) Presentá planos firmados por profesional matriculado. 4) Pagás derechos de obra. 5) Inspección municipal. 6) Obtenés permiso. 7) Al finalizar, conforme de obra.",
        "keywords": ["permiso obra", "construir", "reforma", "planos obra", "construccion"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/permiso-para-ejecucion-de-obra-civil",
        "tags": ["obras", "construccion", "permisos"]
    },
    {
        "id": 41,
        "categoria": "Obras y Construcción",
        "subcategoria": "Consultas",
        "pregunta": "¿Necesito permiso para hacer reformas en mi casa?",
        "respuesta": "Depende de la reforma: 1) Obras menores (pintura, revestimientos): NO necesitan permiso. 2) Obras mayores (demolición, ampliación, modificación estructura): SÍ necesitan permiso. 3) Para dudas, consultá en https://buenosaires.gob.ar/tramites/consulta-obligatoria-general. 4) Profesional matriculado debe asesorarte. 5) Obras sin permiso tienen multas.",
        "keywords": ["reforma casa", "permiso reforma", "obras menores", "ampliacion"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/consulta-obligatoria-general",
        "tags": ["obras", "reformas", "consultas"]
    },

    # ===== CATEGORÍA: CEMENTERIOS =====
    {
        "id": 42,
        "categoria": "Cementerios",
        "subcategoria": "Servicios",
        "pregunta": "¿Qué trámites puedo hacer relacionados con cementerios?",
        "respuesta": "Trámites de cementerios: 1) Renovación de nichos/bóvedas. 2) Traslado de restos. 3) Cremación. 4) Certificado de titularidad. 5) Consultas: https://buenosaires.gob.ar/tramites/renovacion-de-arrendamiento-de-nicho. 6) Para servicios fúnebres del GCBA (gratuitos para familias sin recursos): https://buenosaires.gob.ar/tramites/servicio-funerario-del-gobierno-de-la-ciudad-de-buenos-aires",
        "keywords": ["cementerio", "nicho", "boveda", "cremacion", "restos", "funeral"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/servicio-funerario-del-gobierno-de-la-ciudad-de-buenos-aires",
        "tags": ["cementerios", "servicios funebres", "tramites"]
    },

    # ===== CATEGORÍA: EMPLEO =====
    {
        "id": 43,
        "categoria": "Empleo",
        "subcategoria": "Búsqueda",
        "pregunta": "¿Cómo busco trabajo con ayuda del Gobierno de la Ciudad?",
        "respuesta": "Para buscar empleo: 1) Inscribite en https://buenosaires.gob.ar/tramites/solicitud-de-empleo. 2) Subí tu CV. 3) Accedés a: ofertas laborales, cursos de capacitación, orientación vocacional. 4) También hay programas de pasantías y prácticas. 5) Centro de Integración Laboral ofrece asesoramiento gratuito.",
        "keywords": ["buscar trabajo", "empleo", "trabajo caba", "cv", "ofertas laborales"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-empleo",
        "tags": ["empleo", "trabajo", "capacitacion"]
    },

    # ===== CATEGORÍA: FERIAS Y MERCADOS =====
    {
        "id": 44,
        "categoria": "Ferias y Mercados",
        "subcategoria": "Inscripción",
        "pregunta": "¿Cómo me inscribo para vender en ferias de la Ciudad?",
        "respuesta": "Para vender en ferias: 1) FERIAS DE ABASTECIMIENTO: https://buenosaires.gob.ar/tramites/inscripcion-en-el-registro-de-postulantes-de-ferias-itinerantes-de-abastecimiento. 2) FERIAS ARTESANALES: requieren ser artesano certificado. 3) MERCADO DE PULGAS: inscripción específica. 4) Presentás DNI, CUIT, certificado de residencia. 5) Hay lista de espera según disponibilidad de puestos.",
        "keywords": ["feria", "puestos feria", "vender feria", "artesanias", "mercado"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/inscripcion-en-el-registro-de-postulantes-de-ferias-itinerantes-de-abastecimiento",
        "tags": ["ferias", "comercio", "emprendedores"]
    },

    # ===== CATEGORÍA: MASCOTAS =====
    {
        "id": 45,
        "categoria": "Mascotas",
        "subcategoria": "Registro",
        "pregunta": "¿Debo registrar a mi perro potencialmente peligroso?",
        "respuesta": "Sí, es obligatorio. Para registrar: 1) Ingresá a https://buenosaires.gob.ar/tramites/registro-de-propietarios-de-perros-potencialmente-peligrosos. 2) Razas incluidas: Pitbull, Dogo Argentino, Rottweiler, etc. 3) Presentás: DNI, certificado veterinario, fotos del perro. 4) Seguro de responsabilidad civil. 5) Renovación anual. 6) Multas por no registrar.",
        "keywords": ["perro peligroso", "pitbull registro", "registro mascotas", "perro potencialmente peligroso"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/registro-de-propietarios-de-perros-potencialmente-peligrosos",
        "tags": ["mascotas", "registro", "perros"]
    },

    # ===== CATEGORÍA: INFORMACIÓN PÚBLICA =====
    {
        "id": 46,
        "categoria": "Información Pública",
        "subcategoria": "Acceso",
        "pregunta": "¿Cómo solicito información pública al Gobierno de la Ciudad?",
        "respuesta": "Por Ley 104, podés solicitar información: 1) Ingresá a https://buenosaires.gob.ar/tramites/ley-104-solicitud-de-informacion-publica. 2) Describí qué información necesitás. 3) No hace falta justificar el motivo. 4) El Estado tiene 10 días hábiles para responder. 5) Si niegan, podés apelar. 6) Es gratuito.",
        "keywords": ["informacion publica", "ley 104", "solicitar informacion", "transparencia", "acceso informacion"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/ley-104-solicitud-de-informacion-publica",
        "tags": ["informacion publica", "transparencia", "derechos"]
    },

    # ===== CATEGORÍA: EVENTOS =====
    {
        "id": 47,
        "categoria": "Eventos",
        "subcategoria": "Permisos",
        "pregunta": "¿Cómo solicito permiso para realizar un evento en la Ciudad?",
        "respuesta": "Para eventos: 1) EVENTOS PEQUEÑOS: https://buenosaires.gob.ar/tramites/eventos-estandar. 2) EVENTOS MASIVOS (más de 1000 personas): https://buenosaires.gob.ar/tramites/solicitud-de-permiso-de-evento-masivo. 3) Presentás: proyecto del evento, seguros, medidas de seguridad, plan de evacuación. 4) Inspecciones previas. 5) Solicitá con 30-60 días de anticipación.",
        "keywords": ["evento", "permiso evento", "fiesta", "evento masivo", "organizacion eventos"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-permiso-de-evento-masivo",
        "tags": ["eventos", "permisos", "espectaculos"]
    },

    # ===== CATEGORÍA: ADULTOS MAYORES =====
    {
        "id": 48,
        "categoria": "Adultos Mayores",
        "subcategoria": "Centros de Jubilados",
        "pregunta": "¿Qué beneficios hay para adultos mayores en CABA?",
        "respuesta": "Beneficios para adultos mayores: 1) Centros de Día con actividades recreativas y culturales. 2) Programa de Fortalecimiento de Centros de Jubilados. 3) Exenciones impositivas (ABL). 4) Tarifa social de transporte. 5) Cursos y talleres gratuitos. 6) Asistencia en establecimientos residenciales. Info: https://buenosaires.gob.ar",
        "keywords": ["adultos mayores", "jubilados", "tercera edad", "centro jubilados", "beneficios jubilados"],
        "url_referencia": "https://buenosaires.gob.ar",
        "tags": ["adultos mayores", "jubilados", "beneficios"]
    },

    # ===== CATEGORÍA: ESTACIONAMIENTO RESERVADO =====
    {
        "id": 49,
        "categoria": "Estacionamiento",
        "subcategoria": "Reserva",
        "pregunta": "¿Cómo solicito un espacio de estacionamiento reservado?",
        "respuesta": "Para estacionamiento reservado: 1) Personas con discapacidad: con CUD vigente, solicitás en la comuna de tu domicilio. 2) Hoteles y entidades: https://buenosaires.gob.ar/tramites/reserva-de-espacio-de-estacionamiento-para-entidades. 3) Carga y descarga para comercios: https://buenosaires.gob.ar/tramites/solicitud-de-espacio-de-carga-y-descarga-en-la-publica. 4) Evaluación según normativa vigente.",
        "keywords": ["estacionamiento reservado", "cochera discapacitados", "lugar estacionamiento", "carga descarga"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/reserva-de-espacio-de-estacionamiento-para-entidades",
        "tags": ["estacionamiento", "discapacidad", "comercio"]
    },

    # ===== CATEGORÍA: AUTORIZACIONES ESPECIALES =====
    {
        "id": 50,
        "categoria": "Autorizaciones Especiales",
        "subcategoria": "Menores",
        "pregunta": "¿Cómo tramito una autorización de viaje para menores?",
        "respuesta": "Para autorización de viaje de menores: 1) VIAJES AL EXTERIOR: https://buenosaires.gob.ar/tramites/autorizacion-de-viaje-al-exterior-para-menores-de-18-anos. Ambos padres deben autorizar ante escribano o Registro Civil. 2) VIAJES NACIONALES: si viaja con un adulto que no es el padre/madre, necesita autorización simple. 3) Llevá DNI del menor y de los padres.",
        "keywords": ["autorizacion viaje menor", "permiso viaje", "menor exterior", "viajar con menores"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/autorizacion-de-viaje-al-exterior-para-menores-de-18-anos",
        "tags": ["menores", "viajes", "autorizaciones"]
    },

    # ===== MÁS PREGUNTAS COMPLEMENTARIAS =====
    {
        "id": 51,
        "categoria": "Licencias de Conducir",
        "subcategoria": "Ampliación",
        "pregunta": "¿Cómo agrego una categoría a mi licencia de conducir?",
        "respuesta": "Para ampliar licencia: 1) Pedí turno en https://buenosaires.gob.ar/tramites/ampliacion-de-licencia-de-conducir. 2) Rendís examen teórico y práctico de la nueva categoría. 3) Examen médico actualizado. 4) Llevá licencia actual y DNI. 5) Pagás el arancel. 6) Te entregan licencia ampliada en el momento.",
        "keywords": ["ampliar licencia", "agregar categoria", "moto licencia", "camion licencia"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/ampliacion-de-licencia-de-conducir",
        "tags": ["licencia", "ampliacion", "categorias"]
    },
    {
        "id": 52,
        "categoria": "Registro Civil y DNI",
        "subcategoria": "Certificados",
        "pregunta": "¿Cómo obtengo un certificado de domicilio?",
        "respuesta": "Para certificado de domicilio: 1) Acercate a la comuna de tu barrio. 2) Llevá DNI actualizado. 3) Si alquilás, llevá contrato. 4) Un inspector verifica tu domicilio (puede ser en el momento o programar visita). 5) Te entregan el certificado. 6) Sirve para trámites escolares, judiciales, subsidios. Es gratuito.",
        "keywords": ["certificado domicilio", "constancia domicilio", "verificacion domicilio"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/certificado-de-domicilio-real",
        "tags": ["certificados", "domicilio", "tramites"]
    },
    {
        "id": 53,
        "categoria": "Impuestos y AGIP",
        "subcategoria": "Planes de pago",
        "pregunta": "¿Puedo pagar impuestos atrasados en cuotas?",
        "respuesta": "Sí, podés hacer planes de pago: 1) Ingresá a la web de AGIP con Clave Ciudad. 2) Elegí el impuesto (ABL, Patentes, Ingresos Brutos). 3) Consultá planes vigentes (cantidad de cuotas varía). 4) Adherís online. 5) Primera cuota tiene recargo. 6) Si no pagás 2 cuotas consecutivas, se cae el plan.",
        "keywords": ["plan pago", "cuotas impuestos", "deuda impuestos", "refinanciacion"],
        "url_referencia": "https://www.agip.gob.ar",
        "tags": ["impuestos", "planes pago", "deuda"]
    },
    {
        "id": 54,
        "categoria": "Habilitaciones Comerciales",
        "subcategoria": "Baja",
        "pregunta": "¿Cómo doy de baja mi habilitación comercial?",
        "respuesta": "Para dar de baja: 1) Ingresá a https://buenosaires.gob.ar/tramites/solicitud-de-baja-de-habilitacion-comercial. 2) Completás formulario con datos del local. 3) Presentás constancia de baja en AGIP. 4) Declarás que no hay empleados. 5) Inspector verifica que el local esté cerrado. 6) Te liberan de pagar tasas futuras. Importante: baja en AGIP y AGC son separadas.",
        "keywords": ["baja comercio", "cerrar local", "clausura local", "baja habilitacion"],
        "url_referencia": "https://buenosaires.gob.ar/tramites/solicitud-de-baja-de-habilitacion-comercial",
        "tags": ["habilitaciones", "baja", "comercio"]
    } ]#,
    #{
        # "id": 55,
        #"categoria": "Espacios Públicos",
        #"subcategoria": "Publicidad",
        #"pregunta": "¿Cómo solicito permiso para carteles publicitarios?",
        #"respuesta": "Para publicidad en vía pública: 1) Consultá si está permitido en esa ubicación. 2) Ingresá a https://buenosaires.gob.ar/tramites/permiso-solicitud-renovacion-de-anuncio-publicitario. 3) Presentás planos del cartel, contrato del inmueble. 4) Pagás derechos de publicidad. 5) Inspector aprueba la instalación. 6) Permiso anual renovable. 7) Carteles sin permiso son remov