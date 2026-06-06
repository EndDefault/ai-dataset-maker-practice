from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.rag.chunker import build_chunks, collect_text_files
from src.storage.sqlite_store import get_document_by_path, upsert_document
from src.ui.shared.document_status import document_is_ready, document_status_label


def render_chunk_preview() -> None:
    config = get_config()
    st.markdown('<div class="section-label">Chunk 미리보기</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    if not files:
        st.info("chunk로 나눌 문서가 없습니다.")
        return

    selected_name = st.selectbox("문서 선택", [file_path.name for file_path in files])
    selected_file = next(file_path for file_path in files if file_path.name == selected_name)
    upsert_document(selected_file)
    document = get_document_by_path(selected_file)
    if not document_is_ready(document):
        status = document_status_label(document["status"] if document else None)
        st.warning(f"이 문서는 아직 chunk 미리보기를 만들 수 없습니다. 현재 상태: {status}")
        if document and document["error_message"]:
            st.caption(document["error_message"])
        return

    chunks = build_chunks([selected_file])
    st.caption(f"총 {len(chunks)}개 chunk")
    for chunk in chunks[:5]:
        with st.expander(f"chunk {chunk.index}", expanded=chunk.index == 1):
            st.text(chunk.content[:1400])
