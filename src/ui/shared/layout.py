from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.storage.sqlite_store import initialize_database


def bootstrap_app() -> None:
    st.set_page_config(
        page_title="Local AI Task Assistant",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    initialize_database()
    inject_css()


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid #e5e7eb;
        }
        .app-title {
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }
        .app-subtitle {
            color: #64748b;
            font-size: 0.93rem;
            margin-bottom: 1.2rem;
        }
        .section-label {
            color: #475569;
            font-size: 0.86rem;
            font-weight: 650;
            margin: 0.5rem 0 0.3rem;
        }
        .status-row {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.7rem;
        }
        .status-chip {
            border: 1px solid #d7dde8;
            border-radius: 999px;
            padding: 0.18rem 0.58rem;
            font-size: 0.78rem;
            color: #334155;
            background: #f8fafc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="app-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_runtime_chips() -> None:
    config = get_config()
    st.markdown(
        f"""
        <div class="status-row">
          <span class="status-chip">main: {config.main_model}</span>
          <span class="status-chip">cleaner: {config.cleaner_model}</span>
          <span class="status-chip">embed: {config.embedding_model}</span>
          <span class="status-chip">db: SQLite</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
