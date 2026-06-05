from __future__ import annotations

import streamlit as st

from src.normalization.io_cleaner import TASK_LABELS


def render_command_input() -> dict | None:
    st.markdown('<div class="section-label">명령 입력</div>', unsafe_allow_html=True)
    with st.form("command_form", clear_on_submit=False):
        command = st.text_area(
            "자연어 명령",
            placeholder="예: uploads 폴더 자료를 기준으로 sqlite-vec 설치 방법 알려줘",
            height=150,
        )
        task_label = st.selectbox("작업 유형", list(TASK_LABELS.keys()))
        input_path_text = st.text_input("입력 경로", value="uploads")
        submitted = st.form_submit_button("실행", use_container_width=True)

    if not submitted:
        return None

    input_paths = [item.strip() for item in input_path_text.split(",") if item.strip()]
    return {
        "command": command,
        "task_label": task_label,
        "input_paths": input_paths,
    }
