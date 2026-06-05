from __future__ import annotations

import json

import streamlit as st

from src.storage.sqlite_store import list_errors


def render_error_detail(run_id: str) -> None:
    st.markdown('<div class="section-label">오류 상세</div>', unsafe_allow_html=True)
    errors = list_errors(run_id)
    if not errors:
        st.success("기록된 오류가 없습니다.")
        return

    for error in errors:
        st.error(f"{error['code']}: {error['message']}")
        details = json.loads(error["details_json"] or "{}")
        if details:
            st.json(details)
