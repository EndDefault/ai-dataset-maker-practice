from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import get_config
from src.schemas import TaskRequest, TaskResult


DOCUMENT_COLUMN_UPGRADES = {
    "file_type": "file_type text not null default ''",
    "status": "status text not null default 'uploaded'",
    "page_count": "page_count integer",
    "extracted_char_count": "extracted_char_count integer not null default 0",
    "chunk_count": "chunk_count integer not null default 0",
    "text_extractable": "text_extractable integer not null default 0",
    "is_scanned_pdf": "is_scanned_pdf integer not null default 0",
    "error_message": "error_message text",
    "analyzed_at": "analyzed_at text",
}


def connect() -> sqlite3.Connection:
    config = get_config()
    connection = sqlite3.connect(config.db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with connect() as db:
        db.executescript(
            """
            create table if not exists runs (
              id text primary key,
              task_type text not null,
              status text not null,
              command text not null,
              model text,
              created_at text not null,
              finished_at text,
              output_path text,
              error_code text
            );

            create table if not exists documents (
              id integer primary key autoincrement,
              path text not null unique,
              name text not null,
              file_type text not null default '',
              size integer not null,
              status text not null default 'uploaded',
              page_count integer,
              extracted_char_count integer not null default 0,
              chunk_count integer not null default 0,
              text_extractable integer not null default 0,
              is_scanned_pdf integer not null default 0,
              error_message text,
              analyzed_at text,
              modified_at text,
              created_at text not null
            );

            create table if not exists chunks (
              id integer primary key autoincrement,
              document_id integer,
              chunk_index integer not null,
              content text not null,
              created_at text not null,
              foreign key(document_id) references documents(id)
            );

            create table if not exists embeddings (
              id integer primary key autoincrement,
              chunk_id integer,
              model text not null,
              vector_json text not null,
              created_at text not null,
              foreign key(chunk_id) references chunks(id)
            );

            create table if not exists artifacts (
              id integer primary key autoincrement,
              run_id text not null,
              kind text not null,
              path text not null,
              created_at text not null,
              foreign key(run_id) references runs(id)
            );

            create table if not exists errors (
              id integer primary key autoincrement,
              run_id text not null,
              code text not null,
              message text not null,
              details_json text,
              created_at text not null,
              foreign key(run_id) references runs(id)
            );
            """
        )
        _upgrade_documents_table(db)


def _upgrade_documents_table(db: sqlite3.Connection) -> None:
    existing_columns = {row["name"] for row in db.execute("pragma table_info(documents)")}
    for name, definition in DOCUMENT_COLUMN_UPGRADES.items():
        if name not in existing_columns:
            db.execute(f"alter table documents add column {definition}")


def insert_run(request: TaskRequest, *, model: str) -> None:
    initialize_database()
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as db:
        db.execute(
            """
            insert into runs (id, task_type, status, command, model, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            (request.run_id, request.task_type.value, "running", request.command, model, now),
        )


def finish_run(result: TaskResult) -> None:
    initialize_database()
    with connect() as db:
        db.execute(
            """
            update runs
               set status = ?, finished_at = ?, output_path = ?, error_code = ?
             where id = ?
            """,
            (
                result.status.value,
                datetime.now().isoformat(timespec="seconds"),
                str(result.output_path or ""),
                result.error_code,
                result.run_id,
            ),
        )


def add_artifact(run_id: str, kind: str, path: Path) -> None:
    with connect() as db:
        db.execute(
            "insert into artifacts (run_id, kind, path, created_at) values (?, ?, ?, ?)",
            (run_id, kind, str(path), datetime.now().isoformat(timespec="seconds")),
        )


def add_error(run_id: str, code: str, message: str, details: dict | None = None) -> None:
    with connect() as db:
        db.execute(
            "insert into errors (run_id, code, message, details_json, created_at) values (?, ?, ?, ?, ?)",
            (run_id, code, message, json.dumps(details or {}, ensure_ascii=False), datetime.now().isoformat(timespec="seconds")),
        )


def upsert_document(path: Path) -> None:
    initialize_database()
    stat = path.stat()
    now = datetime.now().isoformat(timespec="seconds")
    modified_at = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
    with connect() as db:
        existing = db.execute("select * from documents where path = ?", (str(path),)).fetchone()
        if _document_analysis_is_current(existing, stat.st_size, modified_at):
            return

        from src.rag.chunker import analyze_document_file

        analysis = analyze_document_file(path)
        db.execute(
            """
            insert into documents (
              path,
              name,
              file_type,
              size,
              status,
              page_count,
              extracted_char_count,
              chunk_count,
              text_extractable,
              is_scanned_pdf,
              error_message,
              analyzed_at,
              modified_at,
              created_at
            )
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            on conflict(path) do update set
              name = excluded.name,
              file_type = excluded.file_type,
              size = excluded.size,
              status = excluded.status,
              page_count = excluded.page_count,
              extracted_char_count = excluded.extracted_char_count,
              chunk_count = excluded.chunk_count,
              text_extractable = excluded.text_extractable,
              is_scanned_pdf = excluded.is_scanned_pdf,
              error_message = excluded.error_message,
              analyzed_at = excluded.analyzed_at,
              modified_at = excluded.modified_at
            """,
            (
                str(path),
                path.name,
                analysis.file_type,
                stat.st_size,
                analysis.status,
                analysis.page_count,
                analysis.extracted_char_count,
                analysis.chunk_count,
                int(analysis.text_extractable),
                int(analysis.is_scanned_pdf),
                analysis.error_message,
                now,
                modified_at,
                now,
            ),
        )
        document = db.execute("select id from documents where path = ?", (str(path),)).fetchone()
        if document:
            _replace_document_chunks(db, document["id"], analysis.chunks)


def _document_analysis_is_current(document: sqlite3.Row | None, size: int, modified_at: str) -> bool:
    if not document:
        return False
    return (
        int(document["size"] or 0) == size
        and document["modified_at"] == modified_at
        and bool(document["analyzed_at"])
    )


def _replace_document_chunks(db: sqlite3.Connection, document_id: int, chunks: list[str]) -> None:
    chunk_rows = list(db.execute("select id from chunks where document_id = ?", (document_id,)))
    chunk_ids = [row["id"] for row in chunk_rows]
    if chunk_ids:
        placeholders = ",".join("?" for _ in chunk_ids)
        db.execute(f"delete from embeddings where chunk_id in ({placeholders})", chunk_ids)
    db.execute("delete from chunks where document_id = ?", (document_id,))
    now = datetime.now().isoformat(timespec="seconds")
    db.executemany(
        "insert into chunks (document_id, chunk_index, content, created_at) values (?, ?, ?, ?)",
        [(document_id, index, content, now) for index, content in enumerate(chunks, start=1)],
    )


def delete_document(path: Path) -> None:
    initialize_database()
    with connect() as db:
        document = db.execute("select id from documents where path = ?", (str(path),)).fetchone()
        if not document:
            return
        document_id = document["id"]
        chunk_rows = list(db.execute("select id from chunks where document_id = ?", (document_id,)))
        chunk_ids = [row["id"] for row in chunk_rows]
        if chunk_ids:
            placeholders = ",".join("?" for _ in chunk_ids)
            db.execute(f"delete from embeddings where chunk_id in ({placeholders})", chunk_ids)
        db.execute("delete from chunks where document_id = ?", (document_id,))
        db.execute("delete from documents where id = ?", (document_id,))


def list_documents() -> list[sqlite3.Row]:
    initialize_database()
    with connect() as db:
        return list(db.execute("select * from documents order by created_at desc"))


def get_document_by_path(path: Path) -> sqlite3.Row | None:
    initialize_database()
    with connect() as db:
        return db.execute("select * from documents where path = ?", (str(path),)).fetchone()


def list_runs(limit: int = 50) -> list[sqlite3.Row]:
    initialize_database()
    with connect() as db:
        return list(db.execute("select * from runs order by created_at desc limit ?", (limit,)))


def list_artifacts(run_id: str) -> list[sqlite3.Row]:
    initialize_database()
    with connect() as db:
        return list(db.execute("select * from artifacts where run_id = ? order by created_at desc", (run_id,)))


def list_errors(run_id: str) -> list[sqlite3.Row]:
    initialize_database()
    with connect() as db:
        return list(db.execute("select * from errors where run_id = ? order by created_at desc", (run_id,)))
