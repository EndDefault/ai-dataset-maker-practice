from __future__ import annotations

import streamlit as st

from src.command_router import execute_command
from src.normalization.io_cleaner import TASK_LABELS
from src.ui.features.home.command_input import render_command_input
from src.ui.features.home.result_preview import render_result_preview
from src.ui.features.home.run_status import render_run_status
from src.ui.shared.layout import render_page_header, render_runtime_chips


def render() -> None:
    render_page_header("작업 콘솔", "자연어 명령을 작업 JSON으로 정리하고 결과를 Markdown으로 저장합니다.")
    render_runtime_chips()

    left, right = st.columns([0.43, 0.57], gap="large")
    with left:
        submitted = render_command_input()
        render_run_status()

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
