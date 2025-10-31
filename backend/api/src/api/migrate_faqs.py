"""
Script para migrar FAQs desde rasa-chat/actions/gcba_faqs_db.py hacia Supabase
Ejecutar con: poetry run python src/api/migrate_faqs.py
"""

import sys
import os
from pathlib import Path

# Agregar el path del archivo de FAQs de Rasa
rasa_path = Path(__file__).parent.parent.parent.parent / "rasa-chat" / "src" / "rasa-chat" / "actions"
sys.path.append(str(rasa_path))

try:
    from gcba_faqs_db import faqs_database, CREATE_TABLE_SQL
except ImportError:
    print("Error: No se pudo importar gcba_faqs_db.py desde rasa-chat")
    sys.exit(1)

from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_supabase_client() -> Client:
    """Crear cliente de Supabase"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar definidas en .env")
    
    return create_client(url, key)

def create_table_if_not_exists(supabase: Client):
    """Crear tabla faqs_gcba si no existe"""
    print("Verificando si existe la tabla faqs_gcba...")
    
    # Intentar hacer una consulta simple para verificar si la tabla existe
    try:
        result = supabase.table("faqs_gcba").select("id").limit(1).execute()
        print("✓ Tabla faqs_gcba ya existe")
        return True
    except Exception as e:
        print(f"Tabla faqs_gcba no existe o hay error: {e}")
        print("Nota: Debes crear la tabla manualmente en Supabase con el SQL del archivo gcba_faqs_db.py")
        print("\nSQL para crear la tabla:")
        print(CREATE_TABLE_SQL)
        return False

def migrate_faqs(supabase: Client):
    """Migrar FAQs desde el archivo local hacia Supabase"""
    
    if not create_table_if_not_exists(supabase):
        return False
    
    print(f"Iniciando migración de {len(faqs_database)} FAQs...")
    
    # Limpiar tabla existente (opcional)
    try:
        supabase.table("faqs_gcba").delete().neq("id", 0).execute()
        print("✓ Tabla limpiada")
    except Exception as e:
        print(f"Advertencia al limpiar tabla: {e}")
    
    # Insertar FAQs
    success_count = 0
    error_count = 0
    
    for faq in faqs_database:
        try:
            # Preparar datos para Supabase
            faq_data = {
                "categoria": faq["categoria"],
                "subcategoria": faq.get("subcategoria"),
                "pregunta": faq["pregunta"],
                "respuesta": faq["respuesta"],
                "keywords": faq.get("keywords", []),
                "url_referencia": faq.get("url_referencia"),
                "tags": faq.get("tags", []),
                "activo": True
            }
            
            # Insertar en Supabase
            result = supabase.table("faqs_gcba").insert(faq_data).execute()
            
            if result.data:
                success_count += 1
                print(f"✓ FAQ {faq['id']}: {faq['pregunta'][:50]}...")
            else:
                error_count += 1
                print(f"✗ Error insertando FAQ {faq['id']}")
                
        except Exception as e:
            error_count += 1
            print(f"✗ Error insertando FAQ {faq['id']}: {e}")
    
    print(f"\n=== RESUMEN ===")
    print(f"FAQs migradas exitosamente: {success_count}")
    print(f"Errores: {error_count}")
    print(f"Total procesadas: {len(faqs_database)}")
    
    return success_count > 0

def verify_migration(supabase: Client):
    """Verificar que la migración fue exitosa"""
    try:
        result = supabase.table("faqs_gcba").select("id, categoria, pregunta").execute()
        
        if result.data:
            print(f"\n=== VERIFICACIÓN ===")
            print(f"Total FAQs en Supabase: {len(result.data)}")
            
            # Mostrar algunas categorías
            categorias = {}
            for faq in result.data:
                cat = faq["categoria"]
                categorias[cat] = categorias.get(cat, 0) + 1
            
            print("Categorías disponibles:")
            for cat, count in categorias.items():
                print(f"  - {cat}: {count} FAQs")
                
            return True
        else:
            print("No se encontraron FAQs en la base de datos")
            return False
            
    except Exception as e:
        print(f"Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("=== MIGRACIÓN DE FAQs GCBA ===")
    
    try:
        # Conectar a Supabase
        supabase = get_supabase_client()
        print("✓ Conectado a Supabase")
        
        # Migrar FAQs
        if migrate_faqs(supabase):
            # Verificar migración
            verify_migration(supabase)
            print("\n✓ Migración completada exitosamente!")
        else:
            print("\n✗ Error en la migración")
            
    except Exception as e:
        print(f"Error general: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()