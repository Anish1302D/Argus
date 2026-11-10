"""
Document Processing Package (Layer 1).
Handles PDF and text extraction with untrusted payload sanitization.
"""

from document_processing.extractor import DocumentExtractor

__all__ = ["DocumentExtractor"]
__version__ = "0.1.0"
