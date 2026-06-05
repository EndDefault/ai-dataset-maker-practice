from __future__ import annotations

import math
from dataclasses import dataclass

from src.rag.chunker import TextChunk


@dataclass
class SearchHit:
    chunk: TextChunk
    score: float


def lexical_search(query: str, chunks: list[TextChunk], *, limit: int = 5) -> list[SearchHit]:
    query_terms = {term.strip().lower() for term in query.replace("\n", " ").split() if term.strip()}
    hits: list[SearchHit] = []
    for chunk in chunks:
        content = chunk.content.lower()
        score = sum(content.count(term) for term in query_terms)
        if score > 0:
            hits.append(SearchHit(chunk=chunk, score=float(score)))
    return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
