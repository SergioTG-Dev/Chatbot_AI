"""
Script para agregar la columna address a la tabla departments
"""
from .db.supabase_client import supabase

def migrate_address_column():
    """
    Agrega la columna address a la tabla departments y actualiza los datos existentes
    """
    print("🔧 Ejecutando migración para agregar columna address...")
    
    try:
        print("   Verificando estructura actual de departments...")
        
        # Primero verificamos si la columna ya existe
        response = supabase.table("departments").select("*").limit(1).execute()
        
        if response.data and len(response.data) > 0:
            first_dept = response.data[0]
            if 'address' not in first_dept:
                print("   ⚠️  La columna 'address' no existe. Necesitas ejecutar la migración SQL manualmente.")
                print("   📝 Ejecuta este SQL en tu panel de Supabase:")
                print("   ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS address TEXT;")
                print("\n   Después ejecuta este script nuevamente.")
                return False
            else:
                print("   ✅ La columna 'address' ya existe.")
        
        # Actualizar departamentos existentes con direcciones
        print("   Actualizando direcciones de departamentos...")
        
        departments_updates = [
            {"name": "Obras Públicas", "address": "Av. Corrientes 1234, Buenos Aires Ciudad"},
            {"name": "Registro Civil", "address": "Uruguay 753, Buenos Aires Ciudad"},
            {"name": "Tránsito y Transporte", "address": "Av. Roque Sáenz Peña 511, Buenos Aires Ciudad"},
            {"name": "Rentas", "address": "Carlos Pellegrini 211, Buenos Aires Ciudad"},
            {"name": "Salud Pública", "address": "Av. 9 de Julio 1925, Buenos Aires Ciudad"},
        ]
        
        for dept_update in departments_updates:
            try:
                response = supabase.table("departments").update(
                    {"address": dept_update["address"]}
                ).eq("name", dept_update["name"]).execute()
                
                if response.data:
                    print(f"   ✅ Actualizado: {dept_update['name']}")
                else:
                    print(f"   ⚠️  No se encontró: {dept_update['name']}")
                    
            except Exception as e:
                print(f"   ❌ Error actualizando {dept_update['name']}: {e}")
        
        print("🎉 Migración completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

if __name__ == "__main__":
    migrate_address_column()