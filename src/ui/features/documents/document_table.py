from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.config import get_config
from src.rag.chunker import collect_text_files
from src.storage.sqlite_store import upsert_document


def render_document_table() -> None:
    config = get_config()
    st.markdown('<div class="section-label">문서 목록</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    for file_path in files:
        upsert_document(file_path)

    if not files:
        st.info("아직 업로드된 txt/md/pdf 문서가 없습니다.")
        return

    rows = []
    for file_path in files:
        stat = file_path.stat()
        rows.append(
            {
                "파일": file_path.name,
                "크기(bytes)": stat.st_size,
                "수정 시간": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "경로": str(file_path),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
