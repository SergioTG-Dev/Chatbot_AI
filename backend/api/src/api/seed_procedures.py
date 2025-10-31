"""
Script de seed para crear trámites (procedures) por departamento.
Usa el cliente de Supabase ya configurado en la API.

Ejecución:
  poetry run python src/api/seed_procedures.py
"""

from typing import Dict, List
from api.db.supabase_client import supabase


def norm(s: str) -> str:
    return (s or '').strip().lower()


def load_departments() -> List[Dict]:
    resp = supabase.table("departments").select("*").execute()
    return resp.data or []


def match_dept(departments: List[Dict], key: str) -> Dict | None:
    key = norm(key)
    synonyms = {
        "registro civil": ["registro civil", "dni", "documento", "identidad", "partidas", "pasaporte"],
        "licencias": ["licencias", "licencia", "conducir", "transito", "tránsito"],
        "impuestos": ["impuestos", "rentas", "agip", "tribut"],
    }
    keys = [key] + synonyms.get(key, [])
    for d in departments:
        dn = norm(d.get("name"))
        if any(k in dn for k in keys):
            return d
    return None


def ensure_procedure(name: str, department_id: str, description: str = "", duration_minutes: int = 30):
    # Existe por nombre + department_id?
    q = supabase.table("procedures").select("*")\
        .eq("department_id", department_id)\
        .ilike("name", name).execute()
    if q.data:
        return q.data[0]
    ins = supabase.table("procedures").insert({
        "name": name,
        "description": description,
        "department_id": department_id,
        "duration_minutes": duration_minutes,
    }).execute()
    return ins.data and ins.data[0]


def main():
    departments = load_departments()
    if not departments:
        print("No hay departamentos; crea algunos primero.")
        return

    # Definir paquetes de trámites por departamento clave
    seeds: Dict[str, List[Dict]] = {
        "registro civil": [
            {"name": "Solicitud de DNI", "description": "Turno para tramitar DNI nuevo o reposición"},
            {"name": "Partidas de Nacimiento", "description": "Solicitud y retiro de partidas"},
            {"name": "Pasaporte", "description": "Gestión de pasaporte"},
        ],
        "licencias": [
            {"name": "Licencia de Conducir", "description": "Trámite para obtener la licencia"},
            {"name": "Renovación de Licencia", "description": "Renovar licencia vigente"},
            {"name": "Duplicado de Licencia", "description": "Reponer licencia extraviada/robada"},
        ],
        "impuestos": [
            {"name": "AGIP – Impuestos", "description": "Atención general de impuestos y renta"},
            {"name": "Habilitación Comercial", "description": "Gestión de habilitación de comercios"},
        ],
    }

    for dept_key, procs in seeds.items():
        dept = match_dept(departments, dept_key)
        if not dept:
            print(f"No encontré departamento para clave '{dept_key}'. Omite.")
            continue
        dept_id = dept.get("id")
        dept_name = dept.get("name")
        print(f"Seeding procedimientos para: {dept_name} ({dept_id})")
        for p in procs:
            created = ensure_procedure(p["name"], dept_id, p.get("description", ""), p.get("duration_minutes", 30))
            print(f"  - OK: {created.get('name')} (id={created.get('id')})")


if __name__ == "__main__":
    main()