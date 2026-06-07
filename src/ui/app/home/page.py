from __future__ import annotations

import streamlit as st

from src.command_router import execute_command
from src.normalization.io_cleaner import TASK_LABELS
from src.ui.features.home.command_input import render_command_input
from src.ui.features.home.result_preview import render_result_preview
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header(
        "작업 콘솔",
        "문서를 선택하고 명령을 실행한 뒤 결과를 확인합니다.",
    )

    left, right = st.columns([0.40, 0.60], gap="large")
    with left:
        submitted = render_command_input()

    with right:
        if submitted:
            selected_task = TASK_LABELS.get(submitted["task_label"])
            with st.spinner("작업을 실행하는 중입니다..."):
                result = execute_command(
                    submitted["command"],
                    selected_task=selected_task,
                    input_paths=submitted["input_paths"],
                )
                st.session_state["last_result"] = result
                st.session_state["last_command"] = submitted["command"]
        render_result_preview()
