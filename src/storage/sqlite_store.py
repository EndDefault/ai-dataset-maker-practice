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
    "analysis_version": "analysis_version text not null default ''",
}

CHUNK_COLUMN_UPGRADES = {
    "chunk_type": "chunk_type text not null default 'text'",
    "section_title": "section_title text not null default ''",
    "item_title": "item_title text not null default ''",
    "page_number": "page_number integer",
    "metadata_json": "metadata_json text",
}

EMBEDDING_COLUMN_UPGRADES = {
    "dimension": "dimension integer not null default 0",
}

DOCUMENT_ANALYSIS_VERSION = "v0.3.3-structured-chunks"
VECTOR_TABLE_NAME = "chunk_embeddings"


def connect(*, load_vec: bool = False) -> sqlite3.Connection:
    config = get_config()
    connection = sqlite3.connect(config.db_path)
    connection.row_factory = sqlite3.Row
    if load_vec:
        _load_sqlite_vec(connection)
    return connection


def _load_sqlite_vec(db: sqlite3.Connection) -> None:
    import sqlite_vec

    db.enable_load_extension(True)
    try:
        sqlite_vec.load(db)
    finally:
        db.enable_load_extension(False)


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
              chunk_type text not null default 'text',
              section_title text not null default '',
              item_title text not null default '',
              page_number integer,
              content text not null,
              metadata_json text,
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
        _upgrade_chunks_table(db)
        _upgrade_embeddings_table(db)
        db.execute("create index if not exists idx_chunks_document_id on chunks(document_id)")
        db.execute("create index if not exists idx_chunks_section_title on chunks(section_title)")
        db.execute("create index if not exists idx_embeddings_chunk_model on embeddings(chunk_id, model)")

    try:
        initialize_vector_table()
    except Exception:
        pass


def _upgrade_documents_table(db: sqlite3.Connection) -> None:
    existing_columns = {row["name"] for row in db.execute("pragma table_info(documents)")}
    for name, definition in DOCUMENT_COLUMN_UPGRADES.items():
        if name not in existing_columns:
            db.execute(f"alter table documents add column {definition}")


def _upgrade_chunks_table(db: sqlite3.Connection) -> None:
    existing_columns = {row["name"] for row in db.execute("pragma table_info(chunks)")}
    for name, definition in CHUNK_COLUMN_UPGRADES.items():
        if name not in existing_columns:
            db.execute(f"alter table chunks add column {definition}")


def _upgrade_embeddings_table(db: sqlite3.Connection) -> None:
    existing_columns = {row["name"] for row in db.execute("pragma table_info(embeddings)")}
    for name, definition in EMBEDDING_COLUMN_UPGRADES.items():
        if name not in existing_columns:
            db.execute(f"alter table embeddings add column {definition}")


def initialize_vector_table() -> None:
    config = get_config()
    dimension = int(config.embedding_dimensions)
    if dimension <= 0:
        raise ValueError("embedding_dimensions must be greater than 0")

    with connect(load_vec=True) as db:
        db.execute(
            f"create virtual table if not exists {VECTOR_TABLE_NAME} "
            f"using vec0(embedding float[{dimension}])"
        )


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
              analysis_version,
              created_at
            )
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
              modified_at = excluded.modified_at,
              analysis_version = excluded.analysis_version
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
                DOCUMENT_ANALYSIS_VERSION,
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
        and document["analysis_version"] == DOCUMENT_ANALYSIS_VERSION
    )


def _replace_document_chunks(db: sqlite3.Connection, document_id: int, chunks: list) -> None:
    chunk_rows = list(db.execute("select id from chunks where document_id = ?", (document_id,)))
    chunk_ids = [row["id"] for row in chunk_rows]
    if chunk_ids:
        placeholders = ",".join("?" for _ in chunk_ids)
        db.execute(f"delete from embeddings where chunk_id in ({placeholders})", chunk_ids)
        _delete_chunk_embedding_rows(chunk_ids, db=db)
    db.execute("delete from chunks where document_id = ?", (document_id,))
    now = datetime.now().isoformat(timespec="seconds")
    db.executemany(
        """
        insert into chunks (
          document_id,
          chunk_index,
          chunk_type,
          section_title,
          item_title,
          page_number,
          content,
          metadata_json,
          created_at
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                document_id,
                index,
                chunk.chunk_type,
                chunk.section_title,
                chunk.item_title,
                chunk.page_number,
                chunk.content,
                json.dumps(chunk.metadata or {}, ensure_ascii=False),
                now,
            )
            for index, chunk in enumerate(chunks, start=1)
        ],
    )


def _delete_chunk_embedding_rows(chunk_ids: list[int], *, db: sqlite3.Connection | None = None) -> None:
    if not chunk_ids:
        return

    try:
        if db is not None:
            _load_sqlite_vec(db)
            db.executemany(f"delete from {VECTOR_TABLE_NAME} where rowid = ?", [(chunk_id,) for chunk_id in chunk_ids])
            return

        initialize_vector_table()
        with connect(load_vec=True) as vector_db:
            vector_db.executemany(f"delete from {VECTOR_TABLE_NAME} where rowid = ?", [(chunk_id,) for chunk_id in chunk_ids])
    except Exception:
        return


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
            _delete_chunk_embedding_rows(chunk_ids, db=db)
        db.execute("delete from chunks where document_id = ?", (document_id,))
        db.execute("delete from documents where id = ?", (document_id,))


def list_chunks_for_paths(paths: list[Path]) -> list[sqlite3.Row]:
    initialize_database()

    from src.rag.chunker import collect_text_files

    file_paths = collect_text_files(paths)
    for file_path in file_paths:
        upsert_document(file_path)

    if not file_paths:
        return []

    placeholders = ",".join("?" for _ in file_paths)
    with connect() as db:
        return list(
            db.execute(
                f"""
                select
                  c.id,
                  c.document_id,
                  c.chunk_index,
                  c.chunk_type,
                  c.section_title,
                  c.item_title,
                  c.page_number,
                  c.content,
                  c.metadata_json,
                  d.path,
                  d.name
                from chunks c
                join documents d on d.id = c.document_id
                where d.path in ({placeholders})
                order by d.path, c.chunk_index
                """,
                [str(path) for path in file_paths],
            )
        )


def list_chunks_by_section(paths: list[Path], section_title: str) -> list[sqlite3.Row]:
    initialize_database()

    from src.rag.chunker import collect_text_files

    file_paths = collect_text_files(paths)
    for file_path in file_paths:
        upsert_document(file_path)

    if not file_paths or not section_title:
        return []

    placeholders = ",".join("?" for _ in file_paths)
    with connect() as db:
        return list(
            db.execute(
                f"""
                select
                  c.id,
                  c.document_id,
                  c.chunk_index,
                  c.chunk_type,
                  c.section_title,
                  c.item_title,
                  c.page_number,
                  c.content,
                  c.metadata_json,
                  d.path,
                  d.name
                from chunks c
                join documents d on d.id = c.document_id
                where d.path in ({placeholders})
                  and c.section_title = ?
                order by d.path, c.chunk_index
                """,
                [*[str(path) for path in file_paths], section_title],
            )
        )


def list_chunks_missing_embeddings(paths: list[Path], *, model: str) -> list[sqlite3.Row]:
    chunks = list_chunks_for_paths(paths)
    chunk_ids = [int(row["id"]) for row in chunks]
    if not chunk_ids:
        return []

    placeholders = ",".join("?" for _ in chunk_ids)
    with connect() as db:
        metadata_ids = {
            int(row["chunk_id"])
            for row in db.execute(
                f"select chunk_id from embeddings where model = ? and chunk_id in ({placeholders})",
                [model, *chunk_ids],
            )
        }

    vector_ids: set[int] = set()
    try:
        initialize_vector_table()
        with connect(load_vec=True) as db:
            vector_ids = {
                int(row["rowid"])
                for row in db.execute(
                    f"select rowid from {VECTOR_TABLE_NAME} where rowid in ({placeholders})",
                    chunk_ids,
                )
            }
    except Exception:
        vector_ids = set()

    return [row for row in chunks if int(row["id"]) not in metadata_ids or int(row["id"]) not in vector_ids]


def store_chunk_embedding(chunk_id: int, *, model: str, vector: list[float]) -> None:
    initialize_database()
    initialize_vector_table()

    config = get_config()
    values = [float(value) for value in vector]
    if len(values) != int(config.embedding_dimensions):
        raise ValueError(
            f"{model} embedding dimension mismatch: expected {config.embedding_dimensions}, got {len(values)}"
        )

    import sqlite_vec

    now = datetime.now().isoformat(timespec="seconds")
    with connect(load_vec=True) as db:
        db.execute(f"delete from {VECTOR_TABLE_NAME} where rowid = ?", (chunk_id,))
        db.execute(
            f"insert into {VECTOR_TABLE_NAME}(rowid, embedding) values (?, ?)",
            (chunk_id, sqlite_vec.serialize_float32(values)),
        )
        db.execute("delete from embeddings where chunk_id = ? and model = ?", (chunk_id, model))
        db.execute(
            """
            insert into embeddings (chunk_id, model, vector_json, dimension, created_at)
            values (?, ?, ?, ?, ?)
            """,
            (chunk_id, model, json.dumps(values, ensure_ascii=False), len(values), now),
        )


def search_chunk_embeddings(
    query_vector: list[float],
    paths: list[Path],
    *,
    model: str,
    limit: int = 6,
) -> list[sqlite3.Row]:
    initialize_database()
    initialize_vector_table()
    if limit <= 0:
        return []

    from src.rag.chunker import collect_text_files
    import sqlite_vec

    file_paths = collect_text_files(paths)
    if not file_paths:
        return []

    values = [float(value) for value in query_vector]
    placeholders = ",".join("?" for _ in file_paths)
    with connect(load_vec=True) as db:
        total_row = db.execute(f"select count(*) as count from {VECTOR_TABLE_NAME}").fetchone()
        candidate_limit = max(limit, int(total_row["count"] or 0))
        return list(
            db.execute(
                f"""
                select
                  c.id,
                  c.document_id,
                  c.chunk_index,
                  c.chunk_type,
                  c.section_title,
                  c.item_title,
                  c.page_number,
                  c.content,
                  c.metadata_json,
                  d.path,
                  d.name,
                  v.distance
                from {VECTOR_TABLE_NAME} v
                join chunks c on c.id = v.rowid
                join documents d on d.id = c.document_id
                join embeddings e on e.chunk_id = c.id and e.model = ?
                where v.embedding match ?
                  and k = ?
                  and d.path in ({placeholders})
                order by v.distance
                limit ?
                """,
                [
                    model,
                    sqlite_vec.serialize_float32(values),
                    candidate_limit,
                    *[str(path) for path in file_paths],
                    limit,
                ],
            )
        )


def get_embedding_index_summary() -> dict[str, int | bool]:
    initialize_database()
    with connect() as db:
        metadata_count = int(db.execute("select count(*) from embeddings").fetchone()[0])

    try:
        initialize_vector_table()
        with connect(load_vec=True) as db:
            vector_count = int(db.execute(f"select count(*) from {VECTOR_TABLE_NAME}").fetchone()[0])
        sqlite_vec_available = True
    except Exception:
        vector_count = 0
        sqlite_vec_available = False

    return {
        "metadata_count": metadata_count,
        "vector_count": vector_count,
        "sqlite_vec_available": sqlite_vec_available,
    }


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
