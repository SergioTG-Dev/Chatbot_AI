import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from .db.supabase_client import supabase


def load_faqs_from_module() -> Dict[str, Any]:
    """
    Carga CREATE_TABLE_SQL y faqs_database desde el archivo gcba_faqs_db.py
    ubicado en backend/rasa-chat/src/rasa-chat/actions.
    """
    # Corrige el cálculo del directorio base para apuntar a .../Chatbot_AI
    # Estructura esperada: .../Chatbot_AI/backend/api/src/api/seed_faqs.py
    # parents[4] -> .../Chatbot_AI
    base_dir = Path(__file__).resolve().parents[4]
    faqs_path = base_dir / "backend" / "rasa-chat" / "src" / "rasa-chat" / "actions" / "gcba_faqs_db.py"
    if not faqs_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de FAQs en: {faqs_path}")

    import importlib.util
    spec = importlib.util.spec_from_file_location("gcba_faqs_db", str(faqs_path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore
    return {
        "create_sql": getattr(module, "CREATE_TABLE_SQL", None),
        "faqs": getattr(module, "faqs_database", []),
    }


def upsert_faqs(faqs: List[Dict[str, Any]]) -> int:
    """
    Inserta FAQs en la tabla 'faqs_gcba'. Si la tabla no existe, fallará
    y el usuario deberá ejecutar el SQL en Supabase.
    """
    # Limpia la tabla para evitar duplicados (opcional)
    try:
        supabase.table("faqs_gcba").delete().neq("id", 0).execute()
    except Exception as e:
        print("⚠️ No se pudo limpiar la tabla 'faqs_gcba' (¿no existe aún?).", e)

    total = 0
    batch_size = 100
    for i in range(0, len(faqs), batch_size):
        batch = faqs[i : i + batch_size]
        payload = [
            {
                "categoria": f.get("categoria"),
                "subcategoria": f.get("subcategoria"),
                "pregunta": f.get("pregunta"),
                "respuesta": f.get("respuesta"),
                "keywords": f.get("keywords", []),
                "url_referencia": f.get("url_referencia"),
                "tags": f.get("tags", []),
            }
            for f in batch
        ]
        resp = supabase.table("faqs_gcba").insert(payload).execute()
        total += len(resp.data or [])
        print(f"✅ Insertadas {len(resp.data or [])} FAQs (acumulado: {total})")
    return total


def main():
    print("📚 Cargando FAQs desde gcba_faqs_db.py...")
    data = load_faqs_from_module()
    faqs = data["faqs"]
    print(f"🔎 Total de FAQs encontradas: {len(faqs)}")

    print("⚙️ Insertando FAQs en Supabase (tabla 'faqs_gcba')...")
    inserted = upsert_faqs(faqs)
    print(f"🎉 Seed completado: {inserted} FAQs insertadas.")
    print("ℹ️ Si la tabla no existe, ejecuta el SQL de creación en 'backend/api/codigo.sql' o usa el CREATE_TABLE_SQL del módulo.")


if __name__ == "__main__":
    main()