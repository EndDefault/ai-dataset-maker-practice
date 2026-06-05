from __future__ import annotations

import streamlit as st

from src.storage.sqlite_store import list_runs


def render_run_history() -> str | None:
    st.markdown('<div class="section-label">실행 목록</div>', unsafe_allow_html=True)
    runs = list_runs()
    if not runs:
        st.info("아직 실행 기록이 없습니다.")
        return None

    rows = [
        {
            "run_id": row["id"],
            "작업": row["task_type"],
            "상태": row["status"],
            "생성": row["created_at"],
            "출력": row["output_path"],
        }
        for row in runs
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
    return st.selectbox("상세 확인할 run", [row["id"] for row in runs])
