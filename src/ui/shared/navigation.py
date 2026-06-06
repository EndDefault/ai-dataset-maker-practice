from __future__ import annotations

import streamlit as st


PAGES = ["Home", "Documents", "Runs", "Settings"]


def render_navigation() -> str:
    if st.session_state.get("selected_page") not in PAGES:
        st.session_state["selected_page"] = "Home"

    st.sidebar.title("Local AI")
    return st.sidebar.radio("페이지", PAGES, key="selected_page", label_visibility="collapsed")
