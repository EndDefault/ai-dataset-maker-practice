from __future__ import annotations


def strip_frontmatter(markdown: str) -> str:
    if not markdown.startswith("---"):
        return markdown

    lines = markdown.splitlines()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1 :]).lstrip()
    return markdown
