from __future__ import annotations

import streamlit as st

from src.ui.features.documents.chunk_preview import render_chunk_preview
from src.ui.features.documents.document_table import render_document_table
from src.ui.features.documents.upload_panel import render_upload_panel
from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header(
        "문서",
        "업로드한 문서의 상태와 chunk를 확인합니다.",
    )

    render_upload_panel()
    st.divider()
    render_document_table()
    st.divider()
    render_chunk_preview()
