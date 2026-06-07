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

    rows = []
    for file_path in files:
        stat = file_path.stat()
        row = document_rows.get(str(file_path))
        page_count = row["page_count"] if row and row["page_count"] is not None else "-"
        extracted_chars = int(row["extracted_char_count"] or 0) if row else 0
        chunk_count = int(row["chunk_count"] or 0) if row else 0
        rows.append(
            {
                "파일": file_path.name,
                "형식": file_path.suffix.lower().lstrip(".") or "unknown",
                "크기": f"{stat.st_size:,} bytes",
                "상태": document_status_label(row["status"] if row else None),
                "PDF": page_count,
                "글자 수": extracted_chars,
                "Chunks": chunk_count,
                "수정 시간": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "분석 시간": row["analyzed_at"].replace("T", " ") if row and row["analyzed_at"] else "-",
                "오류": row["error_message"] if row and row["error_message"] else "",
            }
        )

    st.dataframe(rows, use_container_width=True, hide_index=True)

    with st.expander("문서 삭제", expanded=False):
        st.warning("삭제하면 uploads 파일과 SQLite 문서/chunk/embedding 기록이 함께 정리됩니다.")
        file_by_name = {file_path.name: file_path for file_path in files}
        selected_name = st.selectbox("삭제할 문서", list(file_by_name.keys()), key="delete_document_name")
        confirm = st.checkbox(f"{selected_name} 삭제 확인", key=f"delete_document_confirm_{selected_name}")
        if st.button("선택 문서 삭제", use_container_width=True, disabled=not confirm):
            remove_document_file(file_by_name[selected_name])
            st.toast("문서를 삭제했습니다.")
            st.rerun()


def remove_document_file(file_path: Path) -> None:
    selected_paths: list[str] = st.session_state.get("selected_input_paths", [])
    st.session_state["selected_input_paths"] = [path for path in selected_paths if Path(path) != file_path]
    delete_document(file_path)
    if file_path.exists():
        file_path.unlink()
