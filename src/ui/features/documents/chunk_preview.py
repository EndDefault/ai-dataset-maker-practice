from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.rag.chunker import build_chunks, collect_text_files


def render_chunk_preview() -> None:
    config = get_config()
    st.markdown('<div class="section-label">Chunk 미리보기</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    if not files:
        st.info("chunk로 나눌 문서가 없습니다.")
        return

    selected_name = st.selectbox("문서 선택", [file_path.name for file_path in files])
    selected_file = next(file_path for file_path in files if file_path.name == selected_name)
    chunks = build_chunks([selected_file])
    st.caption(f"총 {len(chunks)}개 chunk")
    for chunk in chunks[:5]:
        with st.expander(f"chunk {chunk.index}", expanded=chunk.index == 1):
            st.text(chunk.content[:1400])
