"""
markdown_plus.cli
~~~~~~~~~~~~~~~~~

Command-line entry point.

    markdown-plus FILE.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="markdown-plus",
        description=(
            "Interactive Markdown viewer for the terminal. "
            "Links with {.modal-btn} open native terminal modals."
        ),
    )
    parser.add_argument("file", type=Path, help="Markdown file to view.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path: Path = args.file
    if not path.is_file():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 1

    try:
        from .tui import run as run_tui
    except ImportError as exc:
        print(
            "error: the interactive viewer needs its runtime deps.\n"
            '    pip install "markdown-plus[cli]"\n'
            f"    (underlying error: {exc})",
            file=sys.stderr,
        )
        return 1

    return run_tui(path)


if __name__ == "__main__":
    raise SystemExit(main())
