-- Tabla de departamentos (si no existe)
CREATE TABLE IF NOT EXISTS public.departments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Tabla de Tickets/Solicitudes
CREATE TABLE IF NOT EXISTS public.tickets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    citizen_id UUID REFERENCES public.citizens(id) ON DELETE CASCADE NOT NULL,
    department_id UUID REFERENCES public.departments(id) ON DELETE SET NULL,
    assigned_official_id UUID REFERENCES public.officials(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'abierto', -- abierto, en_progreso, cerrado
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de Turnos
CREATE TABLE IF NOT EXISTS public.turnos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    citizen_id UUID REFERENCES public.citizens(id) ON DELETE CASCADE NOT NULL,
    procedure_type TEXT NOT NULL, -- 'pasaporte', 'carnet_de_conducir', etc.
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status TEXT NOT NULL DEFAULT 'programado', -- programado, completado, cancelado
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de Sesiones de Chat
CREATE TABLE IF NOT EXISTS public.chat_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    citizen_id UUID REFERENCES public.citizens(id) ON DELETE CASCADE NOT NULL,
    official_id UUID REFERENCES public.officials(id) ON DELETE SET NULL,
    ticket_id UUID REFERENCES public.tickets(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'activa', -- activa, cerrada
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de Mensajes de Chat
CREATE TABLE IF NOT EXISTS public.chat_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES public.chat_sessions(id) ON DELETE CASCADE NOT NULL,
    sender_id UUID NOT NULL,
    sender_type TEXT NOT NULL, -- 'citizen' o 'official'
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);




-- ============================================
-- Tabla de Departamentos (Requerida por 'officials')
-- Nota: Usé el nombre 'departments' (inglés) que es el estándar,
-- pero si prefieres 'departaments' (español), solo debes renombrar la tabla
-- y la referencia en 'officials'.
-- ============================================
CREATE TABLE IF NOT EXISTS public.departments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- Tabla de Ciudadanos
-- Almacena los datos de los ciudadanos de Argentina.
-- ============================================
CREATE TABLE IF NOT EXISTS public.citizens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    dni TEXT NOT NULL UNIQUE, -- El DNI debe ser único para cada ciudadano.
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, -- El email también debe ser único.
    created_at TIMESTAMPTZ DEFAULT NOW() -- Registra la fecha de creación.
);

-- ============================================
-- Tabla de Funcionarios
-- Almacena los datos de los funcionarios públicos.
-- IMPORTANTE: El 'id' de esta tabla es una referencia directa a un usuario
-- en la tabla de autenticación de Supabase (auth.users).
-- ============================================
CREATE TABLE IF NOT EXISTS public.officials (
    -- El 'id' es una clave foránea a auth.users y también la clave primaria de esta tabla.
    id UUID NOT NULL,
    full_name TEXT NOT NULL,
    description TEXT,
    -- Referencia al departamento al que pertenece el funcionario.
    -- Si se elimina un departamento, el campo se pone en NULL (no se borra el funcionario).
    department_id UUID REFERENCES public.departments(id) ON DELETE SET NULL,
    
    -- Definimos la clave primaria
    PRIMARY KEY (id),
    
    -- Definimos la restricción de clave foránea hacia la tabla de autenticación de Supabase.
    -- Si se elimina el usuario en auth.users, también se elimina este registro.
    FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- Índices para mejorar el rendimiento en búsquedas frecuentes
-- Índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_tickets_citizen_id ON public.tickets(citizen_id);
CREATE INDEX IF NOT EXISTS idx_turnos_citizen_id ON public.turnos(citizen_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON public.chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_citizens_dni ON public.citizens(dni);
CREATE INDEX IF NOT EXISTS idx_officials_department_id ON public.officials(department_id);

-- ============================================
-- Tabla de FAQs GCBA
-- Conocimiento base para preguntas frecuentes del chatbot.
-- ============================================
CREATE TABLE IF NOT EXISTS public.faqs_gcba (
    id SERIAL PRIMARY KEY,
    categoria TEXT NOT NULL,
    subcategoria TEXT,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    keywords TEXT[] DEFAULT '{}',
    url_referencia TEXT,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices recomendados para búsquedas por categoría/subcategoría y por palabras clave
CREATE INDEX IF NOT EXISTS idx_faqs_categoria ON public.faqs_gcba(categoria);
CREATE INDEX IF NOT EXISTS idx_faqs_subcategoria ON public.faqs_gcba(subcategoria);
CREATE INDEX IF NOT EXISTS idx_faqs_keywords ON public.faqs_gcba USING GIN (keywords);
