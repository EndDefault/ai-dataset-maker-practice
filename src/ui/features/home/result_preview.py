from __future__ import annotations

import streamlit as st

from src.schemas import TaskStatus
from src.ui.shared.messages import NO_RESULT


def render_result_preview() -> None:
    st.markdown('<div class="section-label">결과 미리보기</div>', unsafe_allow_html=True)
    result = st.session_state.get("last_result")
    if not result:
        st.info(NO_RESULT)
        return

    if result.status == TaskStatus.SUCCESS:
        st.success(f"{result.title} 완료")
    else:
        st.error(f"{result.title}: {result.error_code}")

    if result.output_path:
        st.caption(f"Markdown: {result.output_path}")
    if result.error_path:
        st.caption(f"Error JSON: {result.error_path}")

    st.markdown(result.markdown)
