from __future__ import annotations

import streamlit as st

from src.config import get_config


PAGES = ["Home", "Documents", "Runs", "Settings"]


def render_navigation() -> str:
    config = get_config()
    st.sidebar.title("Local AI")
    st.sidebar.caption("작업 콘솔")
    page_name = st.sidebar.radio("페이지", PAGES, key="selected_page", label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.caption("현재 모델")
    st.sidebar.code(
        f"main: {config.main_model}\ncleaner: {config.cleaner_model}\nembed: {config.embedding_model}",
        language="txt",
    )
    st.sidebar.caption(f"DB: {config.db_path}")
    return page_name
