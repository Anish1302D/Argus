"""
ARGUS Official APCTT Stage 1 Participant Module.
Entrypoint: `participant_module.adapter:AssessmentModule`
"""

from pathlib import Path
import sys

_ENGINE_ROOT = Path(__file__).resolve().parent / "argus_engine"
if str(_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(_ENGINE_ROOT))

from participant_module.adapter import AssessmentModule

__all__ = ["AssessmentModule"]
