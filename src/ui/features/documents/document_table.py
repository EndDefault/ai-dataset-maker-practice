from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from src.config import get_config
from src.rag.chunker import collect_text_files
from src.storage.sqlite_store import delete_document, upsert_document


def render_document_table() -> None:
    config = get_config()
    st.markdown('<div class="section-label">문서 목록</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    for file_path in files:
        upsert_document(file_path)

    if not files:
        st.info("아직 업로드된 txt, md, pdf 문서가 없습니다.")
        return

    for file_path in files:
        stat = file_path.stat()
        col_name, col_size, col_modified, col_delete = st.columns([0.34, 0.16, 0.34, 0.16])
        with col_name:
            st.write(file_path.name)
            st.caption(str(file_path))
        with col_size:
            st.write(f"{stat.st_size:,} bytes")
        with col_modified:
            st.write(datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
        with col_delete:
            if st.button("삭제", key=f"delete_doc_{file_path.name}", use_container_width=True):
                remove_document_file(file_path)
                st.rerun()


def remove_document_file(file_path: Path) -> None:
    selected_paths: list[str] = st.session_state.get("selected_input_paths", [])
    st.session_state["selected_input_paths"] = [path for path in selected_paths if Path(path) != file_path]
    delete_document(file_path)
    if file_path.exists():
        file_path.unlink()
