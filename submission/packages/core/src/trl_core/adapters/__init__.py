"""
Input and Output Adapters.
Encapsulates external input/output schemas behind strictly defined interfaces.
"""

from trl_core.adapters.base import BaseInputAdapter, BaseOutputAdapter
from trl_core.adapters.internal_adapter import InternalInputAdapter, InternalOutputAdapter

__all__ = [
    "BaseInputAdapter",
    "BaseOutputAdapter",
    "InternalInputAdapter",
    "InternalOutputAdapter",
]

