from __future__ import annotations

import importlib.util

import streamlit as st

from src.config import get_config
from src.llm.ollama_client import get_ollama_client


def render_run_status() -> None:
    config = get_config()
    st.markdown('<div class="section-label">런타임 상태</div>', unsafe_allow_html=True)
    models = get_ollama_client().list_models()
    has_sqlite_vec = bool(importlib.util.find_spec("sqlite_vec"))

    st.write(f"SQLite DB: `{config.db_path}`")
    st.write(f"sqlite-vec: `{'installed' if has_sqlite_vec else 'missing'}`")
    if models:
        st.write("Ollama 모델:")
        st.code("\n".join(models), language="txt")
    else:
        st.warning("Ollama 모델 목록을 가져오지 못했습니다. Ollama가 실행 중인지 확인해 주세요.")
