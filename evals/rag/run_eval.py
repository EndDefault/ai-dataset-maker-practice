from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


EVAL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EVAL_DIR.parents[1]
REPORT_DIR = EVAL_DIR / "reports"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.command_router import execute_command  # noqa: E402
from src.rag.chunker import collect_text_files  # noqa: E402
from src.schemas import TaskStatus  # noqa: E402
from src.ui.shared.markdown import strip_frontmatter  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run RAG evaluation cases.")
    parser.add_argument("--cases", default=str(EVAL_DIR / "cases.json"), help="Path to eval cases JSON.")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N enabled cases.")
    parser.add_argument("--dry-run", action="store_true", help="Validate cases without calling the model.")
    args = parser.parse_args()

    cases_path = Path(args.cases)
    cases = load_cases(cases_path)
    enabled_cases = [case for case in cases if case.get("enabled", True)]
    if args.limit:
        enabled_cases = enabled_cases[: args.limit]

    if args.dry_run:
        return dry_run(enabled_cases)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now()
    results = [run_case(case) for case in enabled_cases]
    report_base = REPORT_DIR / f"rag_eval_{started_at.strftime('%Y%m%d_%H%M%S')}"
    write_json_report(report_base.with_suffix(".json"), started_at, results)
    write_markdown_report(report_base.with_suffix(".md"), started_at, results)

    passed = sum(1 for result in results if result["passed"])
    print(f"RAG eval complete: {passed}/{len(results)} passed")
    print(f"Markdown report: {report_base.with_suffix('.md')}")
    print(f"JSON report: {report_base.with_suffix('.json')}")
    return 0 if passed == len(results) else 1


def load_cases(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def dry_run(cases: list[dict[str, Any]]) -> int:
    print(f"cases: {len(cases)}")
    for case in cases:
        input_paths = case.get("input_paths") or ["uploads"]
        files = collect_text_files([Path(path) for path in input_paths])
        print(f"- {case['id']}: {len(files)} input files")
        print(f"  question: {case['question']}")
    return 0


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    input_paths = case.get("input_paths") or ["uploads"]
    result = execute_command(
        case["question"],
        selected_task="rag_search",
        input_paths=[str(path) for path in input_paths],
    )
    checks = evaluate_checks(case, result)
    passed = all(check["passed"] for check in checks)
    source_names = sorted({Path(source.get("path", "")).name for source in result.sources})

    return {
        "id": case["id"],
        "question": case["question"],
        "passed": passed,
        "status": result.status.value if isinstance(result.status, TaskStatus) else str(result.status),
        "run_id": result.run_id,
        "output_path": str(result.output_path) if result.output_path else "",
        "error_code": result.error_code or "",
        "error_message": result.error_message or "",
        "source_count": len(result.sources),
        "source_names": source_names,
        "checks": checks,
        "answer_markdown": strip_frontmatter(result.markdown),
        "notes": case.get("notes", ""),
    }


def evaluate_checks(case: dict[str, Any], result) -> list[dict[str, Any]]:
    checks_config = case.get("checks") or {}
    markdown = result.markdown or ""
    source_count = len(result.sources)
    checks: list[dict[str, Any]] = []

    checks.append(
        {
            "name": "status_success",
            "passed": result.status == TaskStatus.SUCCESS,
            "expected": "success",
            "actual": result.status.value if isinstance(result.status, TaskStatus) else str(result.status),
        }
    )

    min_sources = int(checks_config.get("min_sources", 0))
    if min_sources:
        checks.append(
            {
                "name": "min_sources",
                "passed": source_count >= min_sources,
                "expected": min_sources,
                "actual": source_count,
            }
        )

    for term in checks_config.get("expected_terms", []):
        checks.append(
            {
                "name": f"expected_term:{term}",
                "passed": term in markdown,
                "expected": term,
                "actual": "present" if term in markdown else "missing",
            }
        )

    for term in checks_config.get("forbidden_terms", []):
        checks.append(
            {
                "name": f"forbidden_term:{term}",
                "passed": term not in markdown,
                "expected": f"not {term}",
                "actual": "absent" if term not in markdown else "present",
            }
        )

    return checks


def write_json_report(path: Path, started_at: datetime, results: list[dict[str, Any]]) -> None:
    payload = {
        "started_at": started_at.isoformat(timespec="seconds"),
        "case_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "results": results,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown_report(path: Path, started_at: datetime, results: list[dict[str, Any]]) -> None:
    lines = [
        "# RAG eval report",
        "",
        f"- started_at: {started_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- passed: {sum(1 for result in results if result['passed'])}/{len(results)}",
        "",
        "| case | result | run_id | sources | output |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for result in results:
        result_label = "PASS" if result["passed"] else "FAIL"
        lines.append(
            f"| {result['id']} | {result_label} | {result['run_id']} | {result['source_count']} | {result['output_path']} |"
        )

    for result in results:
        lines.extend(
            [
                "",
                f"## {result['id']}",
                "",
                f"**Question:** {result['question']}",
                "",
                f"**Result:** {'PASS' if result['passed'] else 'FAIL'}",
                "",
                f"**Sources:** {', '.join(result['source_names']) or '-'}",
                "",
                "### Checks",
                "",
                "| check | result | expected | actual |",
                "| --- | --- | --- | --- |",
            ]
        )
        for check in result["checks"]:
            lines.append(
                f"| {check['name']} | {'PASS' if check['passed'] else 'FAIL'} | {check['expected']} | {check['actual']} |"
            )
        lines.extend(["", "### Answer", "", result["answer_markdown"].strip()])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
