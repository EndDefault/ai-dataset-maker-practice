from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from src.config import get_config
from src.normalization.io_cleaner import TASK_LABELS
from src.rag.chunker import collect_text_files
from src.storage.sqlite_store import get_document_by_path, upsert_document
from src.ui.shared.document_status import document_is_ready, document_status_label


DEFAULT_TASK_LABEL = "RAG 질의응답"


def render_input_file_picker() -> list[str]:
    config = get_config()
    uploaded_files = collect_text_files([config.uploads_dir])
    selected_paths: list[str] = st.session_state.setdefault("selected_input_paths", [])
    uploaded_path_set = {str(file_path) for file_path in uploaded_files}
    selected_paths = [path for path in selected_paths if path in uploaded_path_set]
    st.session_state["selected_input_paths"] = selected_paths

    for file_path in uploaded_files:
        upsert_document(file_path)

    st.markdown('<div class="section-label">이번 작업 입력 문서</div>', unsafe_allow_html=True)
    if not uploaded_files:
        st.info("Documents 페이지에서 txt, md, pdf 파일을 먼저 업로드해 주세요.")
        return []

    file_options = {file_path.name: str(file_path) for file_path in uploaded_files}
    selected_name = st.selectbox("업로드한 문서", list(file_options.keys()), key="home_input_file")

    add_col, clear_col = st.columns([0.55, 0.45])
    with add_col:
        if st.button("입력 문서 추가", use_container_width=True):
            selected_path = file_options[selected_name]
            if selected_path not in selected_paths:
                selected_paths.append(selected_path)
                st.session_state["selected_input_paths"] = selected_paths
                st.toast("이번 작업 입력에 추가했습니다.")
            else:
                st.toast("이미 추가된 문서입니다.")
    with clear_col:
        if st.button("선택 목록 비우기", use_container_width=True, disabled=not selected_paths):
            st.session_state["selected_input_paths"] = []
            st.rerun()

    if not selected_paths:
        st.warning("아직 선택한 입력 문서가 없습니다.")
        return []

    st.markdown("선택된 문서")
    unready_names: list[str] = []
    for index, path_text in enumerate(list(selected_paths)):
        path = Path(path_text)
        document = get_document_by_path(path)
        status = document_status_label(document["status"] if document else None)
        extracted_chars = int(document["extracted_char_count"] or 0) if document else 0
        chunk_count = int(document["chunk_count"] or 0) if document else 0
        if not document_is_ready(document):
            unready_names.append(path.name)

        row_left, row_right = st.columns([0.76, 0.24])
        with row_left:
            st.markdown(
                f"""
                <div class="file-row">
                  <div class="file-title">{escape(path.name)}</div>
                  <div class="file-meta">{escape(status)} · {extracted_chars:,}자 · {chunk_count:,} chunks</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with row_right:
            if st.button("선택 해제", key=f"remove_input_{index}_{path.name}", use_container_width=True):
                selected_paths.remove(path_text)
                st.session_state["selected_input_paths"] = selected_paths
                st.rerun()

    if unready_names:
        st.warning("상태가 좋지 않은 문서가 있습니다: " + ", ".join(unready_names))
    return list(selected_paths)


def render_command_input() -> dict | None:
    input_paths = render_input_file_picker()

    st.markdown('<div class="section-label">명령 입력</div>', unsafe_allow_html=True)
    task_labels = list(TASK_LABELS.keys())
    default_index = task_labels.index(DEFAULT_TASK_LABEL) if DEFAULT_TASK_LABEL in task_labels else 0

    with st.form("command_form", clear_on_submit=False):
        task_label = st.selectbox("작업 유형", task_labels, index=default_index)
        command = st.text_area(
            "자연어 명령",
            placeholder="예: 선택한 문서를 기준으로 저출생, 보육, 청년 지원 항목과 금액을 표로 정리해줘",
            height=160,
        )
        submitted = st.form_submit_button("실행", use_container_width=True)

    if not submitted:
        return None

    command = command.strip()
    if not input_paths:
        st.warning("실행할 입력 문서를 먼저 추가해 주세요.")
        return None
    if not command:
        st.warning("실행할 명령을 입력해 주세요.")
        return None

    return {
        "command": command,
        "task_label": task_label,
        "input_paths": input_paths,
    }
