"""
ML Inference Package (Layer 2).
Provides feature extraction, evidence mining, LightGBM ordinal modeling, and rule adjudication.
"""

from .classifier import TRLOrdinalClassifier
from .features import FeatureExtractor

__all__ = ["TRLOrdinalClassifier", "FeatureExtractor"]
__version__ = "0.1.0"

