from __future__ import annotations

import json
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from scoring_engine import score_project  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: python score.py <input.json>", file=sys.stderr)
        return 1

    input_path = Path(args[0])
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        result = score_project(payload)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result["markdown_report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
