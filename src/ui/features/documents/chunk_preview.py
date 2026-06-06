from __future__ import annotations

import json

import streamlit as st

from src.config import get_config
from src.rag.chunker import collect_text_files
from src.storage.sqlite_store import get_document_by_path, list_chunks_for_paths, upsert_document
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

    chunks = list_chunks_for_paths([selected_file])
    item_count = sum(len(read_chunk_items(chunk)) for chunk in chunks)
    st.caption(f"총 {len(chunks)}개 section/text chunk · 후보 항목 {item_count}개")
    for chunk in chunks[:8]:
        items = read_chunk_items(chunk)
        section_title = str(chunk["section_title"] or "일반 텍스트")
        chunk_type = str(chunk["chunk_type"] or "text")
        label = f"chunk {chunk['chunk_index']} · {chunk_type} · {section_title}"
        if items:
            label = f"{label} · 후보 {len(items)}개"
        with st.expander(label, expanded=int(chunk["chunk_index"]) == 1):
            if items:
                st.dataframe(build_candidate_rows(items), use_container_width=True, hide_index=True)
            else:
                st.text(str(chunk["content"])[:1400])


def read_chunk_items(chunk) -> list[dict]:
    raw_metadata = chunk["metadata_json"]
    if not raw_metadata:
        return []
    try:
        metadata = json.loads(raw_metadata)
    except json.JSONDecodeError:
        return []
    items = metadata.get("items")
    return items if isinstance(items, list) else []


def build_candidate_rows(items: list[dict]) -> list[dict]:
    rows = []
    for index, item in enumerate(items, start=1):
        amounts = item.get("amounts") if isinstance(item.get("amounts"), list) else []
        amount_text = ", ".join(f"+{amount}억원" for amount in amounts) if amounts else "문서에서 확인 안 됨"
        rows.append(
            {
                "candidate_id": f"C{index}",
                "예산 항목": str(item.get("title") or ""),
                "증액 금액": amount_text,
                "근거 내용": str(item.get("content") or "")[:260],
            }
        )
    return rows
