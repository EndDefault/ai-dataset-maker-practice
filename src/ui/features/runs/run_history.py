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
            "완료": row["finished_at"] or "-",
            "모델": row["model"] or "-",
            "오류": row["error_code"] or "",
            "출력": row["output_path"] or "",
            "명령": shorten(row["command"]),
        }
        for row in runs
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    run_ids = [row["id"] for row in runs]
    return st.selectbox(
        "상세 확인할 run",
        run_ids,
        format_func=lambda run_id: format_run_option(run_id, runs),
    )


def shorten(value: str, limit: int = 70) -> str:
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def format_run_option(run_id: str, runs: list) -> str:
    for row in runs:
        if row["id"] == run_id:
            return f"{row['id']} · {row['task_type']} · {row['status']}"
    return run_id
