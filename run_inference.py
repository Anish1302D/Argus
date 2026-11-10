#!/usr/bin/env python3
"""
Root CLI entrypoint for TRL Debate Engine.
Delegates to packages/competition_engine/run_inference.py.
"""

import sys
from pathlib import Path

# Add all package src directories to Python path
ROOT_DIR = Path(__file__).resolve().parent
for pkg in ["core", "document_processing", "ml_inference", "retrieval", "agent_orchestration", "competition_engine"]:
    pkg_src = ROOT_DIR / "packages" / pkg / "src"
    if pkg_src.exists() and str(pkg_src) not in sys.path:
        sys.path.insert(0, str(pkg_src))

from packages.competition_engine.run_inference import main

if __name__ == "__main__":
    sys.exit(main())

