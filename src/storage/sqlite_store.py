from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import get_config
from src.schemas import TaskRequest, TaskResult


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
              size integer not null,
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
    with connect() as db:
        db.execute(
            """
            insert into documents (path, name, size, modified_at, created_at)
            values (?, ?, ?, ?, ?)
            on conflict(path) do update set
              name = excluded.name,
              size = excluded.size,
              modified_at = excluded.modified_at
            """,
            (
                str(path),
                path.name,
                stat.st_size,
                datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )


def list_documents() -> list[sqlite3.Row]:
    initialize_database()
    with connect() as db:
        return list(db.execute("select * from documents order by created_at desc"))


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
