from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.storage.sqlite_store import upsert_document


def render_upload_panel() -> None:
    config = get_config()
    st.markdown('<div class="section-label">문서 업로드</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("txt/md 파일", type=["txt", "md"], accept_multiple_files=True)
    if not uploaded_files:
        return

    if st.button("업로드 저장", use_container_width=True):
        for uploaded_file in uploaded_files:
            target = config.uploads_dir / uploaded_file.name
            target.write_bytes(uploaded_file.getbuffer())
            upsert_document(target)
        st.success(f"{len(uploaded_files)}개 파일을 uploads 폴더에 저장했습니다.")
