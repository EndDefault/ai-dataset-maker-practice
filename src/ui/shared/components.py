from __future__ import annotations

from pathlib import Path

import streamlit as st


def render_file_link(path: str | Path, label: str | None = None) -> None:
    file_path = Path(path)
    st.caption(f"{label or file_path.name}: {file_path}")


def render_empty_state(title: str, body: str) -> None:
    st.info(f"{title}\n\n{body}")
