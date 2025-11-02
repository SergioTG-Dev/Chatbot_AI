from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import re
from ..db.supabase_client import supabase

print("[api.endpoints.faqs] módulo cargado y router registrado")

router = APIRouter(prefix="/faqs", tags=["FAQs"])

@router.get("/ping", summary="Ping FAQs")
def ping_faqs():
    return {"status": "ok"}

def _search_faqs(q: Optional[str] = None, categoria: Optional[str] = None) -> List[Dict[str, Any]]:
    query = supabase.table("faqs_gcba").select("id,categoria,subcategoria,pregunta,respuesta,keywords,url_referencia,tags")

    if categoria:
        query = query.ilike("categoria", f"%{categoria}%")

    if q:
        # Buscar en pregunta y en keywords (array de texto)
        query = query.or_(
            f"pregunta.ilike.%{q}%,keywords.cs.{{{q}}}"
        )

    resp = query.limit(50).execute()
    return resp.data or []

def calculate_relevance_score(faq: Dict[str, Any], search_terms: List[str]) -> float:
    score = 0.0

    pregunta = (faq.get('pregunta') or '').lower()
    respuesta = (faq.get('respuesta') or '').lower()
    keywords = [kw.lower() for kw in faq.get('keywords', []) or []]
    tags = [tag.lower() for tag in faq.get('tags', []) or []]

    for term in search_terms:
        term = term.lower()
        if term in pregunta:
            score += 10.0
        for keyword in keywords:
            if term in keyword:
                score += 8.0
        for tag in tags:
            if term in tag:
                score += 6.0
        if term in respuesta:
            score += 2.0

    total_matches = sum(1 for term in search_terms
                        if term.lower() in pregunta or
                           any(term.lower() in kw for kw in keywords))
    if total_matches > 1:
        score *= 1.5

    return score

@router.get("/", summary="Listar FAQs", description="Devuelve FAQs opcionalmente filtradas por categoría y búsqueda")
def list_faqs(q: Optional[str] = Query(None), categoria: Optional[str] = Query(None)):
    return _search_faqs(q=q, categoria=categoria)

@router.get("/categorias", summary="Obtener categorías", description="Devuelve todas las categorías disponibles")
def get_categorias():
    try:
        result = supabase.table("faqs_gcba").select("categoria").execute()
        categorias = list(set(faq.get('categoria') for faq in (result.data or []) if faq.get('categoria')))
        return {"categorias": sorted(categorias)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo categorías: {str(e)}")

@router.get("/search", summary="Buscar mejor coincidencia", description="Devuelve las mejores coincidencias para una consulta con algoritmo de relevancia")
def search_best_match(
    q: str = Query(..., description="Texto de búsqueda"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    limit: int = Query(3, description="Número máximo de resultados")
):
    results = _search_faqs(q=q, categoria=categoria)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron FAQs")

    search_terms = re.findall(r'\b\w+\b', q.lower())
    scored_faqs = []
    for faq in results:
        score = calculate_relevance_score(faq, search_terms)
        if score > 0:
            scored_faqs.append({**faq, "relevance_score": score})

    scored_faqs.sort(key=lambda x: x["relevance_score"], reverse=True)
    best_matches = scored_faqs[:limit]
    for faq in best_matches:
        faq.pop("relevance_score", None)

    return {
        "faqs": best_matches,
        "total_found": len(scored_faqs),
        "query": q,
        "categoria": categoria,
        "search_terms": search_terms
    }