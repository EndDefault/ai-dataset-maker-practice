from __future__ import annotations

from collections.abc import Mapping

from src.rag.chunker import DocumentStatus


STATUS_LABELS = {
    DocumentStatus.UPLOADED: "업로드됨",
    DocumentStatus.INDEXED: "인덱싱 완료",
    DocumentStatus.TEXT_EMPTY: "텍스트 없음",
    DocumentStatus.SCANNED_PDF: "스캔 PDF 추정",
    DocumentStatus.UNSUPPORTED: "지원하지 않는 파일",
    DocumentStatus.ERROR: "오류",
}


def document_status_label(status: str | None) -> str:
    return STATUS_LABELS.get(status or "", status or "알 수 없음")


def document_is_ready(row: Mapping | None) -> bool:
    if not row:
        return False
    return (
        row["status"] == DocumentStatus.INDEXED
        and bool(row["text_extractable"])
        and int(row["chunk_count"] or 0) > 0
    )
