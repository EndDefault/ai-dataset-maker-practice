from __future__ import annotations

import streamlit as st

from src.config import get_config
from src.rag.chunker import TextChunk, build_chunks, collect_text_files
from src.storage.sqlite_store import get_document_by_path, upsert_document
from src.ui.shared.document_status import document_is_ready, document_status_label


def render_chunk_preview() -> None:
    config = get_config()
    st.markdown('<div class="section-label">Chunk 미리보기</div>', unsafe_allow_html=True)
    files = collect_text_files([config.uploads_dir])
    if not files:
        st.info("chunk로 나눌 문서가 없습니다.")
        return

    selected_name = st.selectbox("문서 선택", [file_path.name for file_path in files])
    selected_file = next(file_path for file_path in files if file_path.name == selected_name)
    upsert_document(selected_file)
    document = get_document_by_path(selected_file)
    if not document_is_ready(document):
        status = document_status_label(document["status"] if document else None)
        st.warning(f"이 문서는 아직 chunk 미리보기를 만들 수 없습니다. 현재 상태: {status}")
        if document and document["error_message"]:
            st.caption(document["error_message"])
        return

    chunks = build_chunks([selected_file])
    section_groups = group_chunks_by_section(chunks)
    st.caption(f"총 {len(chunks)}개 item/text chunk · section package {len(section_groups)}개")
    for group_index, (section_title, section_chunks) in enumerate(section_groups[:8], start=1):
        label = f"{section_title} · 후보 {len(section_chunks)}개"
        with st.expander(label, expanded=group_index == 1):
            if section_title == "일반 텍스트":
                for chunk in section_chunks[:3]:
                    st.text(chunk.content[:1000])
            else:
                st.dataframe(build_candidate_rows(section_chunks), use_container_width=True, hide_index=True)


def group_chunks_by_section(chunks: list[TextChunk]) -> list[tuple[str, list[TextChunk]]]:
    groups: list[tuple[str, list[TextChunk]]] = []
    index_by_title: dict[str, int] = {}
    for chunk in chunks:
        title = chunk.section_title or "일반 텍스트"
        if title not in index_by_title:
            index_by_title[title] = len(groups)
            groups.append((title, []))
        groups[index_by_title[title]][1].append(chunk)
    return groups


def build_candidate_rows(chunks: list[TextChunk]) -> list[dict]:
    rows = []
    for index, chunk in enumerate(chunks, start=1):
        amounts = chunk.metadata.get("amounts") if chunk.metadata else []
        amount_text = ", ".join(f"+{amount}억원" for amount in amounts) if amounts else "문서에서 확인 안 됨"
        rows.append(
            {
                "candidate_id": f"C{index}",
                "chunk": chunk.index,
                "예산 항목": chunk.item_title or "문서에서 확인 안 됨",
                "증액 금액": amount_text,
                "근거 내용": chunk.content[:260],
            }
        )
    return rows
