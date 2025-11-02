import uuid
from faker import Faker
from .db.supabase_client import supabase

# Inicializar Faker en español para datos más realistas
fake = Faker('es_ES')

def clear_tables():
    """
    Limpia todas las tablas de la base de datos.
    Útil para empezar desde cero durante el desarrollo.
    El orden es importante para evitar problemas con las claves foráneas.
    """
    print("🧹 Limpiando tablas existentes...")
    try:
        supabase.table("chat_messages").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("chat_sessions").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("tickets").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("turnos").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("officials").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("citizens").delete().neq("id", uuid.uuid4()).execute()
        supabase.table("departments").delete().neq("id", uuid.uuid4()).execute()
        print("✅ Tablas limpiadas exitosamente.")
    except Exception as e:
        print(f"❌ Error al limpiar las tablas: {e}")
        print("   Asegúrate de que tu rol de Supabase tenga los permisos necesarios (SERVICE_ROLE_KEY).")


def seed_database():
    """
    Puebla la base de datos con datos de prueba.
    """
    print("🌱 Comenzando a poblar la base de datos...")

    # 1. Crear Departamentos (usando upsert para evitar duplicados)
    print("   Creando departamentos...")
    departments_data = [
        {"name": "Obras Públicas", "address": "Av. Corrientes 1234, Buenos Aires Ciudad"},
        {"name": "Registro Civil", "address": "Uruguay 753, Buenos Aires Ciudad"},
        {"name": "Tránsito y Transporte", "address": "Av. Roque Sáenz Peña 511, Buenos Aires Ciudad"},
        {"name": "Rentas", "address": "Carlos Pellegrini 211, Buenos Aires Ciudad"},
        {"name": "Salud Pública", "address": "Av. 9 de Julio 1925, Buenos Aires Ciudad"},
    ]
    # upsert inserta o actualiza si el 'name' ya existe
    departments_response = supabase.table("departments").upsert(departments_data, on_conflict="name").execute()
    dept_ids = [dept['id'] for dept in departments_response.data]
    print(f"   ✅ {len(departments_response.data)} departamentos creados/actualizados.")

    # 2. Crear Ciudadanos
    print("   Creando ciudadanos...")
    citizens_data = []
    for _ in range(50):
        citizens_data.append({
            "dni": fake.unique.numeric(digits=8),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
        })
    citizens_response = supabase.table("citizens").insert(citizens_data).execute()
    citizen_ids = [citizen['id'] for citizen in citizens_response.data]
    print(f"   ✅ {len(citizens_response.data)} ciudadanos creados.")

    # 3. Crear Funcionarios (simulando la relación con auth.users)
    print("   Creando funcionarios...")
    officials_data = []
    for i in range(10):
        officials_data.append({
            # Generamos un UUID para simular el ID que vendría de auth.users
            "id": str(uuid.uuid4()),
            "full_name": fake.name(),
            "description": fake.sentence(nb_words=10),
            "department_id": fake.random.choice(dept_ids),
            # El primer funcionario será un administrador
            "role": 'admin' if i == 0 else 'funcionario'
        })
    officials_response = supabase.table("officials").insert(officials_data).execute()
    official_ids = [official['id'] for official in officials_response.data]
    print(f"   ✅ {len(officials_response.data)} funcionarios creados (1 admin, 9 funcionarios).")

    # 4. Crear Tickets
    print("   Creando tickets...")
    tickets_data = []
    for _ in range(30):
        tickets_data.append({
            "citizen_id": fake.random.choice(citizen_ids),
            "department_id": fake.random.choice(dept_ids),
            "assigned_official_id": fake.random.choice(official_ids + [None]),
            "title": fake.sentence(nb_words=4),
            "description": fake.paragraph(nb_sentences=3),
            "status": fake.random.choice(elements=('abierto', 'en_progreso', 'resuelto', 'cerrado')),
        })
    tickets_response = supabase.table("tickets").insert(tickets_data).execute()
    ticket_ids = [ticket['id'] for ticket in tickets_response.data]
    print(f"   ✅ {len(tickets_response.data)} tickets creados.")

    # 5. Crear Turnos
    print("   Creando turnos...")
    turnos_data = []
    for _ in range(40):
        turnos_data.append({
            "citizen_id": fake.random.choice(citizen_ids),
            "procedure_type": fake.random.choice(elements=('pasaporte', 'carnet_de_conducir', 'cedula', 'renovación de licencia')),
            "scheduled_at": fake.date_time_this_year(before_now=True, after_now=True).isoformat(),
            "status": fake.random.choice(elements=('programado', 'completado', 'cancelado', 'no_asistio')),
        })
    turnos_response = supabase.table("turnos").insert(turnos_data).execute()
    print(f"   ✅ {len(turnos_response.data)} turnos creados.")

    # 6. Crear Sesiones y Mensajes de Chat
    print("   Creando sesiones y mensajes de chat...")
    chat_sessions_data = []
    for _ in range(15):
        chat_sessions_data.append({
            "citizen_id": fake.random.choice(citizen_ids),
            "official_id": fake.random.choice(official_ids + [None]),
            "ticket_id": fake.random.choice(ticket_ids + [None]),
            "status": fake.random.choice(elements=('activa', 'cerrada')),
        })
    sessions_response = supabase.table("chat_sessions").insert(chat_sessions_data).execute()
    session_ids = [session['id'] for session in sessions_response.data]

    chat_messages_data = []
    for session_id in session_ids:
        # Crear entre 1 y 5 mensajes por sesión
        for _ in range(fake.random_int(min=1, max=5)):
            chat_messages_data.append({
                "session_id": session_id,
                "sender_id": fake.random.choice(citizen_ids + official_ids),
                "sender_type": fake.random.choice(elements=('citizen', 'official')),
                "content": fake.sentence(nb_words=7),
            })
    messages_response = supabase.table("chat_messages").insert(chat_messages_data).execute()
    print(f"   ✅ {len(sessions_response.data)} sesiones de chat y {len(messages_response.data)} mensajes creados.")

    print("\n🎉 Base de datos poblada exitosamente.")


if __name__ == "__main__":
    # Descomenta la siguiente línea si quieres limpiar la base de datos antes de poblarla
    # clear_tables()
    seed_database()