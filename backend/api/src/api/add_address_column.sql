-- Agregar columna address a la tabla departments
ALTER TABLE public.departments 
ADD COLUMN IF NOT EXISTS address TEXT;

-- Actualizar departamentos existentes con direcciones
UPDATE public.departments 
SET address = CASE 
    WHEN name = 'Obras Públicas' THEN 'Av. Corrientes 1234, Buenos Aires Ciudad'
    WHEN name = 'Registro Civil' THEN 'Uruguay 753, Buenos Aires Ciudad'
    WHEN name = 'Tránsito y Transporte' THEN 'Av. Roque Sáenz Peña 511, Buenos Aires Ciudad'
    WHEN name = 'Rentas' THEN 'Carlos Pellegrini 211, Buenos Aires Ciudad'
    WHEN name = 'Salud Pública' THEN 'Av. 9 de Julio 1925, Buenos Aires Ciudad'
    ELSE 'Dirección no disponible'
END
WHERE address IS NULL;