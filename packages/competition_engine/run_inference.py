#!/usr/bin/env python3
"""
Standalone Competition Inference CLI.
Entrypoint for official competition evaluation.
Runs completely offline with zero dependency on the web app or hosted APIs.
"""

import argparse
import sys
from pathlib import Path

# Add all modular package src directories to path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1] if (SCRIPT_DIR.name == "competition_engine") else SCRIPT_DIR
for pkg in ["core", "document_processing", "ml_inference", "retrieval", "agent_orchestration", "competition_engine"]:
    pkg_src = REPO_ROOT / "packages" / pkg / "src"
    if pkg_src.exists() and str(pkg_src) not in sys.path:
        sys.path.insert(0, str(pkg_src))

from competition_engine.runner import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="TRL Debate Engine — Standalone Competition Inference Engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        required=True,
        help="Path to the input document file (.txt, .md, .pdf)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Path to write the output JSON file. If omitted, defaults to outputs/assessment_<doc_id>.json"
    )
    parser.add_argument(
        "--format",
        choices=["internal"],
        default="internal",
        help="Target output schema adapter. 'internal' uses the PRD v1.0 canonical format."
    )
    parser.add_argument(
        "--strict-security",
        action="store_true",
        help="Strict mode: reject documents containing detected prompt injection threats."
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_file: Path = args.input.resolve()

    # Graceful input validation
    if not input_file.exists():
        sys.stderr.write(f"[ERROR] Input file does not exist: {input_file}\n")
        return 1

    if not input_file.is_file():
        sys.stderr.write(f"[ERROR] Target path is not a file: {input_file}\n")
        return 1

    if input_file.stat().st_size == 0:
        sys.stderr.write(f"[ERROR] Input document is empty (0 bytes): {input_file}\n")
        return 1

    # Default output path
    output_file = args.output
    if output_file is None:
        output_file = Path("outputs") / f"assessment_{input_file.stem}.json"

    try:
        sys.stdout.write(f"[INFO] Ingesting document: {input_file.name}\n")
        assessment = run_pipeline(
            input_path=input_file,
            output_path=output_file,
            strict_security=args.strict_security
        )
        sys.stdout.write(f"[SUCCESS] Predicted TRL: {assessment.predicted_trl} (Confidence: {assessment.confidence:.2f})\n")
        sys.stdout.write(f"[SUCCESS] Assessment saved to: {output_file.resolve()}\n")
        return 0
    except Exception as exc:
        sys.stderr.write(f"[FATAL] Pipeline failed gracefully: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

