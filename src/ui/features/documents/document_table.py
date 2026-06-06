from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from src.config import get_config
from src.rag.chunker import collect_text_files
from src.storage.sqlite_store import delete_document, list_documents, upsert_document
from src.ui.shared.document_status import document_status_label


def render_document_table() -> None:
    config = get_config()
    st.markdown('<div class="section-label">문서 목록</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    for file_path in files:
        upsert_document(file_path)
    document_rows = {row["path"]: row for row in list_documents()}

    if not files:
        st.info("아직 업로드된 txt, md, pdf 문서가 없습니다.")
        return

    header_name, header_status, header_metrics, header_modified, header_delete = st.columns([0.26, 0.15, 0.23, 0.18, 0.18])
    header_name.caption("파일")
    header_status.caption("상태")
    header_metrics.caption("처리 정보")
    header_modified.caption("수정/분석 시간")
    header_delete.caption("관리")

    for file_path in files:
        stat = file_path.stat()
        row = document_rows.get(str(file_path))
        col_name, col_status, col_metrics, col_modified, col_delete = st.columns([0.26, 0.15, 0.23, 0.18, 0.18])
        with col_name:
            st.write(file_path.name)
            st.caption(f"{file_path.suffix.lower().lstrip('.') or 'unknown'} · {stat.st_size:,} bytes")
        with col_status:
            st.write(document_status_label(row["status"] if row else None))
            if row and row["error_message"]:
                st.caption(row["error_message"])
        with col_metrics:
            page_count = row["page_count"] if row and row["page_count"] is not None else "-"
            extracted_chars = int(row["extracted_char_count"] or 0) if row else 0
            chunk_count = int(row["chunk_count"] or 0) if row else 0
            if row and row["file_type"] == "pdf":
                st.write(f"PDF {page_count}p")
            else:
                st.write("텍스트 문서")
            st.caption(f"{extracted_chars:,}자 · {chunk_count:,} chunks")
        with col_modified:
            st.write(datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
            if row and row["analyzed_at"]:
                st.caption(f"분석 {row['analyzed_at'].replace('T', ' ')}")
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
