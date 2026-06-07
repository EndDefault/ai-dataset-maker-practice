from __future__ import annotations

from html import escape

import streamlit as st

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
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid #e5e7eb;
        }
        .page-title {
            font-size: 1.45rem;
            font-weight: 750;
            margin: 0 0 0.1rem;
        }
        .page-subtitle {
            color: #64748b;
            font-size: 0.92rem;
            margin: 0 0 1rem;
        }
        .section-label {
            color: #334155;
            font-size: 0.86rem;
            font-weight: 700;
            margin: 0.15rem 0 0.5rem;
        }
        .file-row {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            padding: 0.55rem 0.65rem;
            margin-bottom: 0.35rem;
        }
        .file-title {
            color: #0f172a;
            font-weight: 700;
        }
        .file-meta {
            color: #64748b;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }
        .soft-note {
            color: #475569;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 0.65rem 0.75rem;
            font-size: 0.86rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="page-title">{escape(title)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{escape(subtitle)}</div>', unsafe_allow_html=True)
