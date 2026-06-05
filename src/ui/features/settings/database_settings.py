from __future__ import annotations

import sqlite3

import streamlit as st

from src.config import get_config
from src.storage.sqlite_store import initialize_database


def render_database_settings() -> None:
    config = get_config()
    st.markdown('<div class="section-label">DB 설정</div>', unsafe_allow_html=True)
    initialize_database()
    st.write(f"SQLite version: `{sqlite3.sqlite_version}`")
    st.write(f"DB path: `{config.db_path}`")
    st.write(f"DB exists: `{config.db_path.exists()}`")
