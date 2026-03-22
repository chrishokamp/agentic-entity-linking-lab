"""Transparent extension templates for retrieval and agentic linking."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Callable, Protocol


@dataclass
class EntityCandidate:
    """A candidate entity for retrieval or disambiguation."""

    uri: str
    label: str
    score: float
    metadata: dict[str, Any]


class EmbeddingProvider(Protocol):
    """Students can implement this with OpenAI, sentence-transformers, Ollama, or local code."""

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per text."""


def extract_context_window(text: str, start: int, end: int, window: int = 120) -> dict[str, str]:
    """Extract left and right context around a mention span."""
    left = text[max(0, start - window):start]
    right = text[end:min(len(text), end + window)]
    return {"left_context": left, "right_context": right}


class SimpleVectorStoreTemplate:
    """A tiny in-memory vector retrieval scaffold.

    This is intentionally simple and dependency-free. Students can replace the
    embedding provider and storage backend while keeping the retrieval flow.
    """

    def __init__(self, embedding_provider: EmbeddingProvider):
        self.embedding_provider = embedding_provider
        self._rows: list[dict[str, Any]] = []

    def index_entities(self, entities: list[dict[str, Any]]) -> None:
        texts = [entity["label"] for entity in entities]
        vectors = self.embedding_provider.embed_texts(texts)
        self._rows = [
            {
                "entity": entity,
                "vector": vector,
            }
            for entity, vector in zip(entities, vectors)
        ]

    def retrieve(self, mention: str, top_k: int = 5) -> list[EntityCandidate]:
        mention_vector = self.embedding_provider.embed_texts([mention])[0]
        scored: list[EntityCandidate] = []

        for row in self._rows:
            entity = row["entity"]
            score = _cosine_similarity(mention_vector, row["vector"])
            scored.append(
                EntityCandidate(
                    uri=entity["uri"],
                    label=entity["label"],
                    score=score,
                    metadata={
                        "current_offices": entity.get("current_offices", []),
                        "wikidata_id": entity.get("metadata", {}).get("wikidata_id"),
                    },
                )
            )

        return sorted(scored, key=lambda candidate: candidate.score, reverse=True)[:top_k]


class AgenticLinkerTemplate:
    """A context-driven linker scaffold modeled after the SNOMED project's agentic stage.

    The harness is backend-agnostic: students pass a callable that receives a prompt
    and returns structured output from OpenAI, Anthropic, Ollama, or another client.
    """

    system_prompt = """You are linking mentions in text to Wikidata entities.

Use the mention text, surrounding context, and candidate list to choose the best URI.
Prefer the highest-scoring candidate unless context clearly supports another choice.
Return JSON with:
- chosen_uri
- confidence
- reasoning
"""

    def build_prompt(
        self,
        *,
        full_text: str,
        mention_text: str,
        start: int,
        end: int,
        candidates: list[EntityCandidate],
    ) -> str:
        context = extract_context_window(full_text, start, end)
        lines = [
            "Task: link one mention to the best Wikidata entity.",
            f"Mention: {mention_text}",
            f"Span: {start}-{end}",
            f"Context: ...{context['left_context']}[{mention_text}]{context['right_context']}...",
            "",
            "Candidates:",
        ]

        for index, candidate in enumerate(candidates, start=1):
            lines.append(
                f"{index}. {candidate.label} | {candidate.uri} | score={candidate.score:.4f} | "
                f"offices={', '.join(candidate.metadata.get('current_offices', []))}"
            )

        lines.append("")
        lines.append("Return JSON only.")
        return "\n".join(lines)

    def link_with_llm(
        self,
        *,
        full_text: str,
        mention_text: str,
        start: int,
        end: int,
        candidates: list[EntityCandidate],
        llm_call: Callable[[str, str], dict[str, Any]],
    ) -> dict[str, Any]:
        prompt = self.build_prompt(
            full_text=full_text,
            mention_text=mention_text,
            start=start,
            end=end,
            candidates=candidates,
        )
        return llm_call(self.system_prompt, prompt)


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)
