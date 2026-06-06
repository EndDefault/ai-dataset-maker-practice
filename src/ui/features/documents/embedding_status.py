from __future__ import annotations

import importlib.util

import streamlit as st

from src.config import get_config
from src.storage.sqlite_store import get_embedding_index_summary


def render_embedding_status() -> None:
    config = get_config()
    st.markdown('<div class="section-label">RAG 준비 상태</div>', unsafe_allow_html=True)
    sqlite_vec_status = "설치됨" if importlib.util.find_spec("sqlite_vec") else "미설치"
    index_summary = get_embedding_index_summary()
    st.write(f"임베딩 모델: `{config.embedding_model}`")
    st.write(f"임베딩 차원: `{config.embedding_dimensions}`")
    st.write(f"벡터 검색 후보: `sqlite-vec` ({sqlite_vec_status})")
    st.write(f"저장된 벡터 row: `{index_summary['vector_count']}`")
    st.caption("RAG 질의응답은 sqlite-vec 벡터 검색을 먼저 사용하고, 실패 시 lexical fallback 검색을 사용합니다.")
