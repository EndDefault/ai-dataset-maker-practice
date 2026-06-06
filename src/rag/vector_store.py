from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

from src.config import get_config
from src.rag.embedding_client import embed_text
from src.rag.chunker import TextChunk
from src.storage.sqlite_store import list_chunks_missing_embeddings, search_chunk_embeddings, store_chunk_embedding


GENERIC_QUERY_TERMS = {
    "기준",
    "기준으로",
    "내용",
    "관련",
    "관련된",
    "근거",
    "금액",
    "문서",
    "문서명",
    "자료",
    "예산",
    "예산안",
    "정리",
    "정리해줘",
    "지원",
    "질문",
    "찾아",
    "찾아서",
    "출력",
    "파일",
    "파일명",
    "표",
    "표로",
    "표시",
    "표시해줘",
    "항목",
    "항목별",
    "함께",
}


@dataclass
class SearchHit:
    chunk: TextChunk
    score: float


def lexical_search(query: str, chunks: list[TextChunk], *, limit: int = 5) -> list[SearchHit]:
    query_terms = extract_query_terms(query)
    if not query_terms:
        query_terms = [term.strip().lower() for term in query.replace("\n", " ").split() if term.strip()]
    hits: list[SearchHit] = []
    for chunk in chunks:
        score = keyword_score(chunk.content, query_terms)
        if score > 0:
            hits.append(SearchHit(chunk=chunk, score=float(score)))
    return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]


def semantic_search(query: str, paths: list[Path], *, limit: int = 6) -> list[SearchHit]:
    config = get_config()
    ensure_embeddings_for_paths(paths, model=config.embedding_model)
    query_vector = embed_text(query, model=config.embedding_model)
    if not query_vector:
        return []

    rerank_limit = max(limit * 4, limit)
    rows = search_chunk_embeddings(query_vector, paths, model=config.embedding_model, limit=rerank_limit)
    query_terms = extract_query_terms(query)
    hits: list[SearchHit] = []
    for row in rows:
        distance = float(row["distance"] or 0.0)
        vector_score = 1.0 / (1.0 + distance)
        rerank_bonus = keyword_score(str(row["content"]), query_terms)
        hits.append(
            SearchHit(
                chunk=TextChunk(path=Path(row["path"]), index=int(row["chunk_index"]), content=str(row["content"])),
                score=vector_score + rerank_bonus,
            )
        )
    return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]


def extract_query_terms(query: str) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    for raw_term in re.findall(r"[0-9A-Za-z가-힣]+", query.lower()):
        term = strip_korean_suffix(raw_term)
        if term.isdigit() or (term.endswith("년") and term[:-1].isdigit()):
            continue
        if len(term) < 2 or term in GENERIC_QUERY_TERMS:
            continue
        if term not in seen:
            seen.add(term)
            terms.append(term)
    return terms


def strip_korean_suffix(term: str) -> str:
    for suffix in ("으로", "에서", "에게", "에는", "에도", "까지", "부터", "이나", "거나", "과", "와", "을", "를", "이", "가", "은", "는", "도", "만", "의", "로", "에"):
        if term.endswith(suffix) and len(term) > len(suffix) + 1:
            return term[: -len(suffix)]
    return term


def matched_terms(content: str, query_terms: list[str]) -> list[str]:
    lowered = content.lower()
    return [term for term in query_terms if term in lowered]


def keyword_score(content: str, query_terms: list[str]) -> float:
    if not query_terms:
        return 0.0
    lowered = content.lower()
    matches = [term for term in query_terms if term in lowered]
    if not matches:
        return 0.0
    total_count = sum(lowered.count(term) for term in matches)
    return len(matches) * 0.35 + min(total_count, 8) * 0.05


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
