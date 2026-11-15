"""
Official APCTT Stage 1 Entrypoint (`participant_module.adapter:AssessmentModule`).

Connects the APCTT worker execution protocol directly to the packaged Argus
assessment engine (`participant_module/argus_engine/`).
"""

from pathlib import Path
import sys

_ENGINE_ROOT = Path(__file__).resolve().parent / "argus_engine"
if str(_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(_ENGINE_ROOT))

from competition_engine.apctt_adapter import AssessmentModule

__all__ = ["AssessmentModule"]
