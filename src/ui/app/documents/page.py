from __future__ import annotations

import streamlit as st

from src.ui.features.documents.chunk_preview import render_chunk_preview
from src.ui.features.documents.document_table import render_document_table
from src.ui.features.documents.embedding_status import render_embedding_status
from src.ui.features.documents.upload_panel import render_upload_panel
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header("문서", "업로드된 txt/md/pdf 문서와 검색 단위 chunk 상태를 확인합니다.")
    top_left, top_right = st.columns([0.45, 0.55], gap="large")
    with top_left:
        render_upload_panel()
        render_embedding_status()
    with top_right:
        render_document_table()
    st.divider()
    render_chunk_preview()
