from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.llm.ollama_client import get_ollama_client


def render_model_settings() -> None:
    config = get_config()
    st.markdown('<div class="section-label">모델 설정</div>', unsafe_allow_html=True)
    st.text_input("메인 응답 모델", value=config.main_model, disabled=True)
    st.text_input("입출력 정제 모델", value=config.cleaner_model, disabled=True)
    st.text_input("임베딩 모델", value=config.embedding_model, disabled=True)

    if st.button("Ollama 모델 확인", use_container_width=True):
        models = get_ollama_client().list_models()
        if models:
            st.code("\n".join(models), language="txt")
        else:
            st.warning("Ollama에 연결하지 못했습니다.")
