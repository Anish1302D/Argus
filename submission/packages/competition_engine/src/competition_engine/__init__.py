"""
Competition Engine Package.
Standalone, air-gapped inference package runnable independently of web services or databases.
Includes the official APCTT AssessmentModule adapter (`apctt_adapter.AssessmentModule`).
"""

from competition_engine.apctt_adapter import AssessmentModule

__version__ = "0.2.0"

__all__ = ["AssessmentModule"]
