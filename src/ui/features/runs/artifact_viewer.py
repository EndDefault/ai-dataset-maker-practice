from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.storage.sqlite_store import list_artifacts


def render_artifact_viewer(run_id: str) -> None:
    st.markdown('<div class="section-label">산출물</div>', unsafe_allow_html=True)
    artifacts = list_artifacts(run_id)
    if not artifacts:
        st.info("저장된 산출물이 없습니다.")
        return

    for artifact in artifacts:
        path = Path(artifact["path"])
        with st.expander(f"{artifact['kind']} / {path.name}", expanded=artifact["kind"] == "markdown"):
            st.caption(str(path))
            if path.exists() and path.suffix == ".md":
                st.markdown(path.read_text(encoding="utf-8"))
            elif path.exists():
                st.code(path.read_text(encoding="utf-8"), language="json")
            else:
                st.warning("파일을 찾지 못했습니다.")
