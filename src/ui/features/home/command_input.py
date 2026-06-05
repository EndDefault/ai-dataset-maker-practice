from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.config import get_config
from src.normalization.io_cleaner import TASK_LABELS
from src.rag.chunker import collect_text_files


def render_input_file_picker() -> list[str]:
    config = get_config()
    uploaded_files = collect_text_files([config.uploads_dir])
    selected_paths: list[str] = st.session_state.setdefault("selected_input_paths", [])

    st.markdown('<div class="section-label">입력 파일</div>', unsafe_allow_html=True)
    if not uploaded_files:
        st.info("Documents 페이지에서 txt, md, pdf 파일을 먼저 업로드해 주세요.")
        return []

    file_options = {file_path.name: str(file_path) for file_path in uploaded_files}
    selected_name = st.selectbox("업로드한 파일", list(file_options.keys()))
    add_left, add_right = st.columns([0.45, 0.55])
    with add_left:
        if st.button("추가", use_container_width=True):
            selected_path = file_options[selected_name]
            if selected_path not in selected_paths:
                selected_paths.append(selected_path)
                st.session_state["selected_input_paths"] = selected_paths
                st.toast("입력 파일에 추가했습니다.")
            else:
                st.toast("이미 추가된 파일입니다.")
    with add_right:
        st.caption("필요한 파일을 하나씩 추가해 이번 작업 입력으로 사용합니다.")

    if not selected_paths:
        st.warning("아직 선택한 입력 파일이 없습니다.")
        return []

    st.write("선택한 입력 파일")
    for index, path_text in enumerate(list(selected_paths)):
        path = Path(path_text)
        col_name, col_delete = st.columns([0.75, 0.25])
        with col_name:
            st.caption(path.name)
        with col_delete:
            if st.button("삭제", key=f"remove_input_{index}_{path.name}", use_container_width=True):
                selected_paths.remove(path_text)
                st.session_state["selected_input_paths"] = selected_paths
                st.rerun()
    return list(selected_paths)


def render_command_input() -> dict | None:
    st.markdown('<div class="section-label">명령 입력</div>', unsafe_allow_html=True)
    input_paths = render_input_file_picker()

    with st.form("command_form", clear_on_submit=False):
        command = st.text_area(
            "자연어 명령",
            placeholder="예: uploads 폴더 자료를 기준으로 sqlite-vec 설치 방법 알려줘",
            height=150,
        )
        task_label = st.selectbox("작업 유형", list(TASK_LABELS.keys()))
        submitted = st.form_submit_button("실행", use_container_width=True)

    if not submitted:
        return None

    if not input_paths:
        st.warning("실행할 입력 파일을 먼저 추가해 주세요.")
        return None

    return {
        "command": command,
        "task_label": task_label,
        "input_paths": input_paths,
    }
