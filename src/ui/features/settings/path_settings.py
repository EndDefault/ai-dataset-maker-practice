from __future__ import annotations

import streamlit as st

from src.config import get_config


def render_path_settings() -> None:
    config = get_config()
    st.markdown('<div class="section-label">경로 설정</div>', unsafe_allow_html=True)
    st.write(f"root: `{config.root_dir}`")
    st.write(f"uploads: `{config.uploads_dir}`")
    st.write(f"outputs: `{config.outputs_dir}`")
    st.write(f"data: `{config.data_dir}`")
    st.caption("환경 변수로 모델명과 Ollama URL을 바꿀 수 있습니다.")
    st.code(
        "OLLAMA_BASE_URL=http://127.0.0.1:11434\n"
        "OLLAMA_MAIN_MODEL=qwen3:14b\n"
        "OLLAMA_CLEANER_MODEL=qwen3:4b\n"
        "OLLAMA_EMBEDDING_MODEL=bge-m3",
        language="txt",
    )
