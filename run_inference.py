#!/usr/bin/env python3
"""
Root CLI entrypoint for TRL Debate Engine.
Delegates to packages/competition_engine/run_inference.py.
"""

import sys
from pathlib import Path

# Add core and competition_engine src directories to Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "packages" / "core" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "competition_engine" / "src"))

from packages.competition_engine.run_inference import main

if __name__ == "__main__":
    sys.exit(main())

