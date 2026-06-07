from __future__ import annotations

import streamlit as st

from src.schemas import TaskStatus
from src.ui.shared.markdown import strip_frontmatter
from src.ui.shared.messages import NO_RESULT


def render_result_preview() -> None:
    header_left, header_right = st.columns([0.68, 0.32])
    with header_left:
        st.markdown('<div class="section-label">결과 미리보기</div>', unsafe_allow_html=True)
    with header_right:
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
        st.markdown(
            '<div class="soft-note">문서를 선택하고 명령을 실행하면 Markdown 결과가 이 영역에 표시됩니다.</div>',
            unsafe_allow_html=True,
        )
        return

    if result.status == TaskStatus.SUCCESS:
        st.success(f"{result.title} 완료")
    else:
        st.error(f"{result.title}: {result.error_code}")

    path_rows = []
    if result.output_path:
        path_rows.append(("Markdown", str(result.output_path)))
    if result.error_path:
        path_rows.append(("Error JSON", str(result.error_path)))
    if path_rows:
        for label, value in path_rows:
            st.caption(f"{label}: {value}")

    st.divider()
    st.markdown(strip_frontmatter(result.markdown))
