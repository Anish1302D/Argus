"""
Document Processing Package (Layer 1).
Handles PDF and text extraction with untrusted payload sanitization.
"""

from .extractor import DocumentExtractor, ExtractedPage

__all__ = ["DocumentExtractor", "ExtractedPage"]
__version__ = "0.1.0"

