"""
Base Abstract Classes for Input and Output Adapters.
Guarantees decoupling from external schemas, file formats, and competition test harnesses.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Union
from trl_core.models import Document, FinalAssessment


class BaseInputAdapter(ABC):
    """Abstract adapter for converting external test inputs into canonical Document objects."""

    @abstractmethod
    def load_document(self, source: Union[str, Path]) -> Document:
        """Load and convert a single input file into a canonical Document."""
        pass

    @abstractmethod
    def load_batch(self, source_dir: Union[str, Path]) -> List[Document]:
        """Load and convert all eligible input files in a directory."""
        pass


class BaseOutputAdapter(ABC):
    """Abstract adapter for serializing canonical FinalAssessment objects to output formats."""

    @abstractmethod
    def format_assessment(self, assessment: FinalAssessment) -> Any:
        """Serialize a FinalAssessment into the target payload representation (dict, string, etc.)."""
        pass

    @abstractmethod
    def write_assessment(self, assessment: FinalAssessment, destination: Union[str, Path]) -> Path:
        """Write the serialized assessment to a file and return the destination path."""
        pass

