from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.storage.sqlite_store import upsert_document


def render_upload_panel() -> None:
    config = get_config()
    st.markdown('<div class="section-label">문서 업로드</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "txt / md / pdf 파일",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
    )
    st.caption("텍스트 기반 PDF를 지원합니다. 스캔 이미지 PDF는 현재 OCR 단계가 필요합니다.")

    if not uploaded_files:
        st.markdown(
            '<div class="soft-note">파일을 선택하면 uploads 폴더에 저장하고 문서 상태를 분석합니다.</div>',
            unsafe_allow_html=True,
        )
        return

    file_names = ", ".join(uploaded_file.name for uploaded_file in uploaded_files)
    st.caption(f"대기 중: {file_names}")
    if st.button("업로드 저장", use_container_width=True):
        for uploaded_file in uploaded_files:
            target = config.uploads_dir / uploaded_file.name
            target.write_bytes(uploaded_file.getbuffer())
            upsert_document(target)
        st.success(f"{len(uploaded_files)}개 파일을 uploads 폴더에 저장했습니다.")
