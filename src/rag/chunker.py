from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from src.config import get_config
from src.errors import AppError, ErrorCode


SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


class DocumentStatus:
    UPLOADED = "uploaded"
    INDEXED = "indexed"
    TEXT_EMPTY = "text_empty"
    SCANNED_PDF = "scanned_pdf"
    UNSUPPORTED = "unsupported"
    ERROR = "error"


@dataclass
class TextDocument:
    path: Path
    content: str


@dataclass
class TextChunk:
    path: Path
    index: int
    content: str
    chunk_type: str = "text"
    section_title: str = ""
    item_title: str = ""
    page_number: int | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ChunkRecord:
    content: str
    chunk_type: str = "text"
    section_title: str = ""
    item_title: str = ""
    page_number: int | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class PdfTextResult:
    content: str
    page_count: int
    extracted_page_count: int


@dataclass
class DocumentAnalysis:
    path: Path
    file_type: str
    status: str
    page_count: int | None
    extracted_char_count: int
    chunk_count: int
    text_extractable: bool
    is_scanned_pdf: bool
    error_message: str
    chunks: list[ChunkRecord]


def resolve_input_paths(paths: list[Path]) -> list[Path]:
    config = get_config()
    resolved = []
    for path in paths or [config.uploads_dir]:
        candidate = path if path.is_absolute() else config.root_dir / path
        if candidate.exists():
            resolved.append(candidate)
    return resolved


def collect_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in resolve_input_paths(paths):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(item for item in path.rglob("*") if item.is_file() and item.suffix.lower() in SUPPORTED_SUFFIXES))
    return sorted(set(files))


def read_text_file(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp949"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def inspect_pdf_file(path: Path) -> PdfTextResult:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise AppError(ErrorCode.UNSUPPORTED_FILE_TYPE, "PDF 처리를 위해 pypdf 패키지가 필요합니다.") from exc

    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as exc:
                raise AppError(ErrorCode.UNSUPPORTED_FILE_TYPE, "암호화된 PDF는 아직 처리할 수 없습니다.", {"path": str(path)}) from exc

        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[page {index}]\n{text.strip()}")

        return PdfTextResult(content="\n\n".join(pages), page_count=len(reader.pages), extracted_page_count=len(pages))
    except AppError:
        raise
    except Exception as exc:
        raise AppError(ErrorCode.ENCODING_ERROR, "PDF 텍스트 추출 중 오류가 발생했습니다.", {"path": str(path)}) from exc


def read_pdf_file(path: Path) -> str:
    result = inspect_pdf_file(path)
    if not result.content.strip():
        raise AppError(
            ErrorCode.UNSUPPORTED_FILE_TYPE,
            "텍스트를 추출할 수 없는 PDF입니다. 스캔 이미지 PDF는 OCR 단계가 필요합니다.",
            {"path": str(path), "page_count": result.page_count},
        )
    return result.content


def read_document_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return read_pdf_file(path)
    return read_text_file(path)


def analyze_document_file(path: Path) -> DocumentAnalysis:
    suffix = path.suffix.lower()
    file_type = suffix.lstrip(".") or "unknown"

    if suffix not in SUPPORTED_SUFFIXES:
        return DocumentAnalysis(
            path=path,
            file_type=file_type,
            status=DocumentStatus.UNSUPPORTED,
            page_count=None,
            extracted_char_count=0,
            chunk_count=0,
            text_extractable=False,
            is_scanned_pdf=False,
            error_message="지원하지 않는 파일 형식입니다.",
            chunks=[],
        )

    try:
        page_count: int | None = None
        is_scanned_pdf = False
        if suffix == ".pdf":
            pdf_result = inspect_pdf_file(path)
            content = pdf_result.content
            page_count = pdf_result.page_count
            is_scanned_pdf = page_count > 0 and pdf_result.extracted_page_count == 0
        else:
            content = read_text_file(path)

        extracted_char_count = len(content.strip())
        chunks = chunk_document_text(content)
        if is_scanned_pdf:
            status = DocumentStatus.SCANNED_PDF
            error_message = "텍스트를 추출할 수 없습니다. 스캔 이미지 PDF로 추정됩니다."
        elif not extracted_char_count:
            status = DocumentStatus.TEXT_EMPTY
            error_message = "추출된 텍스트가 없습니다."
        else:
            status = DocumentStatus.INDEXED
            error_message = ""

        return DocumentAnalysis(
            path=path,
            file_type=file_type,
            status=status,
            page_count=page_count,
            extracted_char_count=extracted_char_count,
            chunk_count=len(chunks),
            text_extractable=bool(extracted_char_count),
            is_scanned_pdf=is_scanned_pdf,
            error_message=error_message,
            chunks=chunks,
        )
    except AppError as exc:
        status = DocumentStatus.UNSUPPORTED if exc.code == ErrorCode.UNSUPPORTED_FILE_TYPE else DocumentStatus.ERROR
        return DocumentAnalysis(
            path=path,
            file_type=file_type,
            status=status,
            page_count=None,
            extracted_char_count=0,
            chunk_count=0,
            text_extractable=False,
            is_scanned_pdf=False,
            error_message=exc.message,
            chunks=[],
        )
    except Exception as exc:
        return DocumentAnalysis(
            path=path,
            file_type=file_type,
            status=DocumentStatus.ERROR,
            page_count=None,
            extracted_char_count=0,
            chunk_count=0,
            text_extractable=False,
            is_scanned_pdf=False,
            error_message=str(exc),
            chunks=[],
        )


def load_documents(paths: list[Path]) -> list[TextDocument]:
    return [TextDocument(path=file_path, content=read_document_file(file_path)) for file_path in collect_text_files(paths)]


def chunk_text(content: str, *, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    cleaned = "\n".join(line.rstrip() for line in content.splitlines()).strip()
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + max_chars, len(cleaned))
        chunks.append(cleaned[start:end].strip())
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def chunk_document_text(content: str) -> list[ChunkRecord]:
    structured_chunks = build_structured_chunks(content)
    if structured_chunks:
        return structured_chunks
    return [ChunkRecord(content=chunk) for chunk in chunk_text(content)]


def build_structured_chunks(content: str) -> list[ChunkRecord]:
    lines = [line.strip() for line in content.replace("\r\n", "\n").splitlines()]
    chunks: list[ChunkRecord] = []
    current_section = ""
    current_page: int | None = None
    current_item_lines: list[str] = []
    current_item_page: int | None = None

    def flush_item() -> None:
        nonlocal current_item_lines, current_item_page
        if not current_section or not current_item_lines:
            current_item_lines = []
            current_item_page = None
            return

        item_text = normalize_inline_text(" ".join(current_item_lines))
        for candidate_text in split_item_candidates(item_text):
            title = infer_item_title(candidate_text)
            content = "\n".join(
                [
                    f"section: {current_section}",
                    f"item: {title}",
                    f"page: {current_item_page or ''}",
                    candidate_text,
                ]
            ).strip()
            chunks.append(
                ChunkRecord(
                    content=content,
                    chunk_type="item",
                    section_title=current_section,
                    item_title=title,
                    page_number=current_item_page,
                    metadata={"amounts": extract_amounts(candidate_text)},
                )
            )
        current_item_lines = []
        current_item_page = None

    for line in lines:
        if not line:
            continue

        page_match = re.match(r"\[page\s+(\d+)\]", line, flags=re.IGNORECASE)
        if page_match:
            current_page = int(page_match.group(1))
            continue

        if is_page_or_major_heading(line):
            flush_item()
            current_section = ""
            continue

        section_title = detect_section_title(line)
        if section_title:
            flush_item()
            current_section = section_title
            continue

        if not current_section:
            continue

        if is_item_start(line):
            flush_item()
            current_item_lines = [line]
            current_item_page = current_page
        elif current_item_lines:
            current_item_lines.append(line)

    flush_item()
    return chunks


def detect_section_title(line: str) -> str:
    if "【" not in line or "】" not in line:
        return ""
    title = line.split("【", 1)[0]
    title = re.sub(r"^[0-9ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ.\-\s]+", "", title)
    title = title.replace("·", " ")
    title = normalize_inline_text(title)
    return title


def is_item_start(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("ㅇ") or stripped.startswith("-")


def is_page_or_major_heading(line: str) -> bool:
    stripped = line.strip()
    if re.match(r"^-\s*\d+\s*-\s*$", stripped):
        return True
    return bool(re.match(r"^-\s*\d+\s*-\s*\d+\s+", stripped))


def normalize_inline_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_item_candidates(text: str) -> list[str]:
    if len(extract_amounts(text)) <= 1:
        if "하고, 특별" in text:
            parts = re.split(r"\s*하고,\s*", text, maxsplit=1)
            candidates = [part.strip() for part in parts if part.strip()]
            if len(candidates) == 2:
                return candidates
        return [text]

    parts = re.split(r"(?<=\))\s*(?:하고,|하며,|하고|,)\s*", text)
    candidates = [part.strip() for part in parts if part.strip()]
    return candidates or [text]


def extract_amounts(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"\(\s*\+([0-9.,]+)\s*\)", text)]


def infer_item_title(text: str, *, max_chars: int = 48) -> str:
    cleaned = re.sub(r"^[ㅇ\-\s()]+", "", text)
    cleaned = re.split(r"억원\(\+|\(\+|하여|하고|으로|지원|지급", cleaned, maxsplit=1)[0]
    cleaned = normalize_inline_text(cleaned).strip(" ,·")
    if not cleaned:
        cleaned = normalize_inline_text(text)
    return cleaned[:max_chars]


def build_chunks(paths: list[Path]) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for document in load_documents(paths):
        for index, chunk in enumerate(chunk_document_text(document.content), start=1):
            chunks.append(
                TextChunk(
                    path=document.path,
                    index=index,
                    content=chunk.content,
                    chunk_type=chunk.chunk_type,
                    section_title=chunk.section_title,
                    item_title=chunk.item_title,
                    page_number=chunk.page_number,
                    metadata=chunk.metadata,
                )
            )
    return chunks
