import argparse
import json
import re
from pathlib import Path


HONORIFIC_RE = re.compile(r"(합니다|습니다|해요|이에요|예요|까요|주세요|됩니다|있습니다|없습니다)")
HAN_RE = re.compile(r"[\u4e00-\u9fff]")


def validate_item(item, line_number):
    errors = []
    messages = item.get("messages")

    if not isinstance(messages, list) or len(messages) != 3:
        return [f"line {line_number}: messages must be a 3-item list"]

    roles = [message.get("role") for message in messages]
    if roles != ["system", "user", "assistant"]:
        errors.append(f"line {line_number}: roles must be system,user,assistant; got {roles}")

    for index, message in enumerate(messages):
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            errors.append(f"line {line_number}: message {index} content is empty")

    assistant = messages[2].get("content", "")
    if not assistant.strip().endswith("냥."):
        errors.append(f"line {line_number}: assistant answer should end with 냥.")

    if assistant.count("냥") > 3:
        errors.append(f"line {line_number}: assistant answer appears longer than 3 nyang endings")

    if HONORIFIC_RE.search(assistant):
        errors.append(f"line {line_number}: assistant answer contains honorific expression")

    if HAN_RE.search(assistant):
        errors.append(f"line {line_number}: assistant answer contains CJK ideograph")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate AI Maker Studio JSONL data.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"File not found: {args.path}")

    errors = []
    items = 0

    with args.path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"line {line_number}: invalid JSON: {error}")
                continue

            items += 1
            errors.extend(validate_item(item, line_number))

    if errors:
        print(f"Checked {items} items: failed")
        for error in errors[:50]:
            print(f"- {error}")
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more")
        raise SystemExit(1)

    print(f"Checked {items} items: ok")


if __name__ == "__main__":
    main()
