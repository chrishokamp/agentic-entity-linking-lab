"""Educational helpers for a Wikidata-backed entity linking lab."""

from .agentic_linking import (
    AgenticLinkerTemplate,
    extract_context_window,
)
from .candidate_retrieval import EntityCandidate, SimpleVectorStoreTemplate
from .wikidata import (
    DEFAULT_BOOTSTRAP_QUERY_PATH,
    DEFAULT_WIKIDATA_ENDPOINT,
    QUERIES_DIR,
    annotate_text,
    build_knowledge_base,
    build_surface_form_index,
    execute_sparql_query,
    fetch_default_bootstrap_knowledge_base,
    fetch_knowledge_base_from_query,
    load_sparql_query,
    normalize_surface_form,
)

__all__ = [
    "AgenticLinkerTemplate",
    "DEFAULT_BOOTSTRAP_QUERY_PATH",
    "DEFAULT_WIKIDATA_ENDPOINT",
    "EntityCandidate",
    "QUERIES_DIR",
    "SimpleVectorStoreTemplate",
    "annotate_text",
    "build_knowledge_base",
    "build_surface_form_index",
    "execute_sparql_query",
    "extract_context_window",
    "fetch_default_bootstrap_knowledge_base",
    "fetch_knowledge_base_from_query",
    "load_sparql_query",
    "normalize_surface_form",
]
