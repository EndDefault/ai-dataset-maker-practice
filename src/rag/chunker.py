from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.config import get_config
from src.errors import AppError, ErrorCode


SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


@dataclass
class TextDocument:
    path: Path
    content: str


@dataclass
class TextChunk:
    path: Path
    index: int
    content: str


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


def read_pdf_file(path: Path) -> str:
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

        if not pages:
            raise AppError(
                ErrorCode.UNSUPPORTED_FILE_TYPE,
                "텍스트를 추출할 수 없는 PDF입니다. 스캔 이미지 PDF는 OCR 단계가 필요합니다.",
                {"path": str(path)},
            )
        return "\n\n".join(pages)
    except AppError:
        raise
    except Exception as exc:
        raise AppError(ErrorCode.ENCODING_ERROR, "PDF 텍스트 추출 중 오류가 발생했습니다.", {"path": str(path)}) from exc


def read_document_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return read_pdf_file(path)
    return read_text_file(path)


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


def build_chunks(paths: list[Path]) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for document in load_documents(paths):
        for index, content in enumerate(chunk_text(document.content), start=1):
            chunks.append(TextChunk(path=document.path, index=index, content=content))
    return chunks
