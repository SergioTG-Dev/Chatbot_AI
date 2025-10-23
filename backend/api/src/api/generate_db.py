from supabase import create_client

# Configura tu proyecto Supabase
url = "https://TU_PROYECTO.supabase.co"
key = "TU_API_KEY"  # Usa la service_role para poder crear tablas
supabase = create_client(url, key)

# Bloque SQL para crear tablas y funciones
sql_script = """
-- ===========================
-- 1. Tabla de perfiles de usuario
-- ===========================
create table if not exists public.user_profiles (
    user_id uuid primary key references auth.users(id) on delete cascade,
    dni text unique,
    preferred_role text check (preferred_role in ('citizen', 'official')) default null
);

-- ===========================
-- 2. Tabla de departamentos
-- ===========================
create table if not exists public.departaments (
    id uuid primary key default gen_random_uuid(),
    name text not null
);

-- ===========================
-- 3. Tabla de funcionarios (officials)
-- ===========================
create table if not exists public.officials (
    id uuid primary key references auth.users(id) on delete cascade,
    full_name text,
    avatar_url text,
    departament_id uuid references public.departaments(id) on delete set null
);

-- ===========================
-- 4. Tabla de ciudadanos
-- ===========================
create table if not exists public.citizens (
    id uuid primary key references auth.users(id) on delete cascade,
    first_name text not null,
    last_name text not null,
    created_at timestamptz default now()
);

-- ===========================
-- 5. Tabla de citas
-- ===========================
create table if not exists public.appointments (
    id uuid primary key default gen_random_uuid(),
    citizen_id uuid references public.citizens(id) on delete cascade,
    procedure_type text not null,
    appointment_datetime timestamptz not null,
    office_location text,
    status text default 'pending',
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- ===========================
-- 6. Tabla de tickets
-- ===========================
create table if not exists public.tickets (
    id uuid primary key default gen_random_uuid(),
    citizen_id uuid references public.citizens(id) on delete cascade,
    subject text not null,
    description text,
    status text default 'open',
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- ===========================
-- 7. Función: obtener rol principal
-- ===========================
create or replace function public.get_user_role()
returns text
language sql
security definer
set search_path = public
as $$
  select case
    when up.preferred_role is not null then up.preferred_role
    when exists (select 1 from officials where id = auth.uid()) then 'official'
    when exists (select 1 from citizens where id = auth.uid()) then 'citizen'
    else 'guest'
  end
  from auth.users u
  left join public.user_profiles up on u.id = up.user_id
  where u.id = auth.uid();
$$;

-- ===========================
-- 8. Función: cambiar rol preferido
-- ===========================
create or replace function public.set_preferred_role(new_role text)
returns void
language plpgsql
security definer
as $$
begin
  if new_role not in ('citizen', 'official') then
    raise exception 'Invalid role';
  end if;

  insert into public.user_profiles(user_id, preferred_role)
  values (auth.uid(), new_role)
  on conflict (user_id) do update set preferred_role = excluded.preferred_role;
end;
$$;

-- ===========================
-- 9. Función: obtener email por DNI
-- ===========================
create or replace function public.get_email_by_dni(p_dni text)
returns text
language sql
security definer
as $$
  select u.email
  from public.user_profiles up
  join auth.users u on up.user_id = u.id
  where up.dni = p_dni
$$;
"""

# ⚡ Ejecutar el SQL desde Supabase (requiere service_role key)
response = supabase.postgrest.rpc("sql", {"query": sql_script})
print(response)
