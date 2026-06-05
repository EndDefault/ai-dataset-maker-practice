from __future__ import annotations

import streamlit as st

from src.ui.features.runs.artifact_viewer import render_artifact_viewer
from src.ui.features.runs.error_detail import render_error_detail
from src.ui.features.runs.run_history import render_run_history
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header("실행 기록", "과거 작업의 Markdown 결과와 오류 파일을 확인합니다.")
    selected_run_id = render_run_history()
    if selected_run_id:
        left, right = st.columns([0.64, 0.36], gap="large")
        with left:
            render_artifact_viewer(selected_run_id)
        with right:
            render_error_detail(selected_run_id)
