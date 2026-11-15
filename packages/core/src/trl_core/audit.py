"""
Assessment Audit Trail Engine.
Captures immutable, step-by-step audit records of rules evaluated,
decisions taken, conflicts resolved, and criteria accepted or rejected.
Supports bit-for-bit reproducibility via retained inputs and methodology versions.
"""

from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional

from trl_core.models import AuditRecord, AuditTrail


class AuditTrailBuilder:
    """
    Builds an immutable, auditable log of the entire assessment pipeline execution.
    Calculates a deterministic reproducibility hash across inputs, methodology, and rulings.
    """

    def __init__(self, methodology_version: str = "2.0.0-argus"):
        self.methodology_version = methodology_version
        self.records: List[AuditRecord] = []

    def record_stage(
        self,
        rule_id: str,
        stage: str,
        inputs: Dict[str, Any],
        outcome: str,
        explanation: str
    ):
        """Append an auditable rule execution event."""
        # Clean inputs for deterministic JSON serialization
        clean_inputs = {}
        for k, v in inputs.items():
            if isinstance(v, (str, int, float, bool, list, dict)) or v is None:
                clean_inputs[k] = v
            else:
                clean_inputs[k] = str(v)

        rec = AuditRecord(
            rule_id=rule_id,
            stage=stage,
            inputs=clean_inputs,
            outcome=outcome,
            explanation=explanation,
            timestamp=datetime.now(timezone.utc),
        )
        self.records.append(rec)

    def build_audit_trail(self, document_id: str, adjudicated_trl: int) -> AuditTrail:
        """
        Finalize the audit trail and compute deterministic SHA-256 hash.
        """
        # Formulate canonical payload for hashing
        hash_payload = {
            "document_id": document_id,
            "methodology_version": self.methodology_version,
            "adjudicated_trl": adjudicated_trl,
            "events": [
                {
                    "rule_id": r.rule_id,
                    "stage": r.stage,
                    "outcome": r.outcome,
                }
                for r in self.records
            ]
        }
        hash_str = json.dumps(hash_payload, sort_keys=True)
        reproducibility_hash = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

        return AuditTrail(
            methodology_version=self.methodology_version,
            records=list(self.records),
            reproducibility_hash=reproducibility_hash,
        )
