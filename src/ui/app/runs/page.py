from __future__ import annotations

import streamlit as st

from src.ui.features.runs.artifact_viewer import render_artifact_viewer
from src.ui.features.runs.error_detail import render_error_detail
from src.ui.features.runs.run_history import render_run_history
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header(
        "실행 기록",
        "과거 실행 결과와 오류 기록을 확인합니다.",
    )

    left, right = st.columns([0.44, 0.56], gap="large")
    with left:
        selected_run_id = render_run_history()

    with right:
        if selected_run_id:
            render_artifact_viewer(selected_run_id)
            st.divider()
            render_error_detail(selected_run_id)
        else:
            st.info("실행을 완료하면 상세 산출물이 이 영역에 표시됩니다.")
