"""
ML Inference Package (Layer 2).
Provides feature extraction, evidence mining, LightGBM ordinal modeling, and rule adjudication.
"""

from ml_inference.classifier import TRLOrdinalClassifier
from ml_inference.features import FeatureExtractor

__all__ = ["TRLOrdinalClassifier", "FeatureExtractor"]
__version__ = "0.1.0"
