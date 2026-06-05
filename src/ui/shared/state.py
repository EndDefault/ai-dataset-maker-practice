from __future__ import annotations

import streamlit as st


def init_session_state() -> None:
    st.session_state.setdefault("last_result", None)
    st.session_state.setdefault("last_command", "")
    st.session_state.setdefault("selected_page", "Home")
    st.session_state.setdefault("selected_input_paths", [])
