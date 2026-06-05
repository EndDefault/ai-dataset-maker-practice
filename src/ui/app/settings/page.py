from __future__ import annotations

import streamlit as st

from src.ui.features.settings.database_settings import render_database_settings
from src.ui.features.settings.model_settings import render_model_settings
from src.ui.features.settings.path_settings import render_path_settings
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header("설정", "로컬 모델, SQLite, 작업 경로 상태를 확인합니다.")
    left, right = st.columns(2, gap="large")
    with left:
        render_model_settings()
        render_database_settings()
    with right:
        render_path_settings()
