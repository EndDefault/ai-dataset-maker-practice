from __future__ import annotations

import streamlit as st

from src.schemas import TaskStatus
from src.ui.shared.markdown import strip_frontmatter
from src.ui.shared.messages import NO_RESULT


def render_result_preview() -> None:
    st.markdown('<div class="section-label">결과 미리보기</div>', unsafe_allow_html=True)
    if st.button("이전 결과/캐시 삭제", use_container_width=True):
        st.session_state["last_result"] = None
        st.session_state["last_command"] = ""
        st.cache_data.clear()
        st.cache_resource.clear()
        st.toast("이전 결과와 Streamlit 캐시를 삭제했습니다.")
        st.rerun()

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

    st.markdown(strip_frontmatter(result.markdown))
