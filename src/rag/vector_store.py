from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from src.config import get_config
from src.rag.embedding_client import embed_text
from src.rag.chunker import TextChunk
from src.storage.sqlite_store import list_chunks_missing_embeddings, search_chunk_embeddings, store_chunk_embedding


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


def semantic_search(query: str, paths: list[Path], *, limit: int = 6) -> list[SearchHit]:
    config = get_config()
    ensure_embeddings_for_paths(paths, model=config.embedding_model)
    query_vector = embed_text(query, model=config.embedding_model)
    if not query_vector:
        return []

    rows = search_chunk_embeddings(query_vector, paths, model=config.embedding_model, limit=limit)
    hits: list[SearchHit] = []
    for row in rows:
        distance = float(row["distance"] or 0.0)
        hits.append(
            SearchHit(
                chunk=TextChunk(path=Path(row["path"]), index=int(row["chunk_index"]), content=str(row["content"])),
                score=1.0 / (1.0 + distance),
            )
        )
    return hits


def ensure_embeddings_for_paths(paths: list[Path], *, model: str) -> int:
    missing_chunks = list_chunks_missing_embeddings(paths, model=model)
    embedded_count = 0
    for chunk in missing_chunks:
        vector = embed_text(str(chunk["content"]), model=model)
        if not vector:
            continue
        store_chunk_embedding(int(chunk["id"]), model=model, vector=vector)
        embedded_count += 1
    return embedded_count


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
