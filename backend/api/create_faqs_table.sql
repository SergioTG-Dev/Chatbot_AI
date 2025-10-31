-- Crear tabla FAQs del GCBA en Supabase
-- Ejecutar este SQL en el SQL Editor de Supabase

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

-- Crear índices para mejorar performance
CREATE INDEX idx_categoria ON faqs_gcba(categoria);
CREATE INDEX idx_keywords ON faqs_gcba USING GIN(keywords);
CREATE INDEX idx_tags ON faqs_gcba USING GIN(tags);

-- Habilitar RLS (Row Level Security) si es necesario
ALTER TABLE faqs_gcba ENABLE ROW LEVEL SECURITY;

-- Política para permitir lectura pública (opcional)
CREATE POLICY "Allow public read access" ON faqs_gcba
    FOR SELECT USING (true);

-- Política para permitir escritura con service role (opcional)
CREATE POLICY "Allow service role full access" ON faqs_gcba
    FOR ALL USING (auth.role() = 'service_role');