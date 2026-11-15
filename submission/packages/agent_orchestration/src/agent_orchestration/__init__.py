"""
Agent Orchestration Package (Layer 3).
Coordinates the Optimist, Skeptic, and Referee agents in a bounded adversarial debate
protocol with deterministic synthesis and implied prerequisites adjudication.
"""

from agent_orchestration.optimist import OptimistReviewer
from agent_orchestration.skeptic import SkepticReviewer
from agent_orchestration.referee import RefereeAdjudicator
from agent_orchestration.protocol import ReviewProtocol

__version__ = "2.0.0"

__all__ = [
    "OptimistReviewer",
    "SkepticReviewer",
    "RefereeAdjudicator",
    "ReviewProtocol",
]
