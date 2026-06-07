from __future__ import annotations

import streamlit as st

from src.ui.shared.layout import render_page_header


def render() -> None:
    render_page_header(
        "설정",
        "현재는 화면에서 바꿀 설정이 없습니다.",
    )

    st.info("아직 설정할 항목이 없습니다.")
