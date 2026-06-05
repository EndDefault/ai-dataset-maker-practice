from __future__ import annotations

import importlib.util

import streamlit as st

from src.config import get_config


def render_embedding_status() -> None:
    config = get_config()
    st.markdown('<div class="section-label">RAG 준비 상태</div>', unsafe_allow_html=True)
    sqlite_vec_status = "설치됨" if importlib.util.find_spec("sqlite_vec") else "미설치"
    st.write(f"임베딩 모델: `{config.embedding_model}`")
    st.write(f"벡터 검색 후보: `sqlite-vec` ({sqlite_vec_status})")
    st.caption("첫 버전은 lexical fallback 검색을 포함합니다. sqlite-vec 인덱싱은 다음 단계에서 연결합니다.")
