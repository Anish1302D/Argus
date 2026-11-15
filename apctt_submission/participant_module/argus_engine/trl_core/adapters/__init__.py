"""
Input and Output Adapters.
Encapsulates external input/output schemas behind strictly defined interfaces.
"""

from .base import BaseInputAdapter, BaseOutputAdapter
from .internal_adapter import InternalInputAdapter, InternalOutputAdapter

__all__ = [
    "BaseInputAdapter",
    "BaseOutputAdapter",
    "InternalInputAdapter",
    "InternalOutputAdapter",
]

