"""
Unit Tests for Standalone Competition CLI (run_inference.py).
Verifies graceful error handling on malformed inputs, nonexistent paths, and strict security mode.
"""

from pathlib import Path
import subprocess
import sys


def test_cli_missing_input_argument():
    result = subprocess.run(
        [sys.executable, "run_inference.py"],
        capture_output=True,
        text=True
    )
    # argparse returns code 2 for missing required argument
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_cli_nonexistent_file():
    result = subprocess.run(
        [sys.executable, "run_inference.py", "--input", "non_existent_file_xyz.txt"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "does not exist" in result.stderr


def test_cli_empty_file(empty_file: Path):
    result = subprocess.run(
        [sys.executable, "run_inference.py", "--input", str(empty_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "empty" in result.stderr.lower()


def test_cli_valid_document_success(sample_valid_paper: Path, tmp_path: Path):
    out_file = tmp_path / "cli_output.json"
    result = subprocess.run(
        [
            sys.executable, "run_inference.py",
            "--input", str(sample_valid_paper),
            "--output", str(out_file)
        ],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "[SUCCESS]" in result.stdout
    assert out_file.exists()


def test_cli_prompt_injection_neutralized_default(sample_injection_paper: Path, tmp_path: Path):
    # Under standard execution, prompt injection is neutralized and execution succeeds
    out_file = tmp_path / "injection_output.json"
    result = subprocess.run(
        [
            sys.executable, "run_inference.py",
            "--input", str(sample_injection_paper),
            "--output", str(out_file)
        ],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert out_file.exists()


def test_cli_prompt_injection_strict_security_rejection(sample_injection_paper: Path, tmp_path: Path):
    # Under strict security, malicious documents are explicitly rejected
    out_file = tmp_path / "rejected_output.json"
    result = subprocess.run(
        [
            sys.executable, "run_inference.py",
            "--input", str(sample_injection_paper),
            "--output", str(out_file),
            "--strict-security"
        ],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "prompt injection" in result.stderr.lower()

