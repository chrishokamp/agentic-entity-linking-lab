"""Educational helpers for a Wikidata-backed entity linking lab."""

from .extensions import (
    AgenticLinkerTemplate,
    EntityCandidate,
    SimpleVectorStoreTemplate,
    extract_context_window,
)
from .wikidata import (
    DEFAULT_WIKIDATA_ENDPOINT,
    build_current_irish_politicians_query,
    build_knowledge_base,
    build_surface_form_index,
    execute_sparql_query,
    fetch_current_irish_politicians,
    normalize_surface_form,
    annotate_text,
)

__all__ = [
    "AgenticLinkerTemplate",
    "DEFAULT_WIKIDATA_ENDPOINT",
    "EntityCandidate",
    "SimpleVectorStoreTemplate",
    "annotate_text",
    "build_current_irish_politicians_query",
    "build_knowledge_base",
    "build_surface_form_index",
    "execute_sparql_query",
    "extract_context_window",
    "fetch_current_irish_politicians",
    "normalize_surface_form",
]
