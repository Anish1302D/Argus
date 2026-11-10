"""
Competition Inference Runner.
Execution logic for standalone, air-gapped inference on technical documentation.
"""

import sys
from pathlib import Path
from typing import Optional

from trl_core.adapters.internal_adapter import InternalInputAdapter, InternalOutputAdapter
from trl_core.models import (
    AgentAssessment,
    AgentType,
    DebateMessage,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    FinalAssessment,
    ImpliedPrerequisiteAudit,
)
from trl_core.sanitizer import sanitize_text
from trl_core.trl_definitions import get_trl_definition


def run_pipeline(
    input_path: Path,
    output_path: Optional[Path] = None,
    strict_security: bool = False
) -> FinalAssessment:
    """
    Execute the standalone competition inference pipeline on an input file.
    Validates input, processes content, detects prompt injections, and generates a structured assessment.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    input_adapter = InternalInputAdapter()
    document = input_adapter.load_document(input_path)

    # Perform security analysis on document chunks
    detected_threats = []
    for chunk in document.chunks:
        sanitized = sanitize_text(chunk.text)
        if not sanitized.is_safe:
            detected_threats.extend(sanitized.detected_threats)

    if detected_threats and strict_security:
        raise ValueError(f"Security Alert: Document rejected due to detected prompt injection threats: {set(detected_threats)}")

    # In Phase 1 baseline, construct a deterministically grounded canonical assessment from document content
    # Note: Phase 2 will plug in the LightGBM classifier, Phase 3 the evidence extraction engine, and Phase 4 the agents
    
    # Check if text contains high-level operational evidence vs basic conceptual language
    content_lower = document.raw_content.lower()
    
    # Preliminary keyword-grounded baseline for Phase 1 verification
    if any(k in content_lower for k in ["operational use", "flight test", "commercial deployment", "field trial"]):
        predicted_level = 7
        confidence = 0.75
        rationale = "Document documents advanced operational trial or field demonstration."
    elif any(k in content_lower for k in ["prototype", "laboratory validation", "bench-scale", "experiment"]):
        predicted_level = 4
        confidence = 0.70
        rationale = "Document demonstrates laboratory-scale prototype and experimental validation."
    elif any(k in content_lower for k in ["formulation", "concept", "analytical"]):
        predicted_level = 2
        confidence = 0.65
        rationale = "Document formulates technical concept with analytical studies; experimental proof absent."
    else:
        predicted_level = 1
        confidence = 0.60
        rationale = "Basic scientific principles observed and reported."

    definition = get_trl_definition(predicted_level)
    satisfied = [c.description for c in definition.criteria]
    missing = []
    if predicted_level < 9:
        next_def = get_trl_definition(predicted_level + 1)
        missing = [c.description for c in next_def.criteria]

    # Traceable evidence item
    evidence_sample = EvidenceItem(
        id=f"EVID-{document.id[:4]}-001",
        document_id=document.id,
        evidence_text=document.chunks[0].text[:200] if document.chunks else "Document text excerpt",
        page_number=1,
        section_name="Overview",
        category=EvidenceCategory.LABORATORY_VALIDATION if predicted_level >= 4 else EvidenceCategory.CONCEPT,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=predicted_level,
        confidence=confidence,
        source_reference={"char_start": 0, "char_end": min(200, len(document.raw_content))}
    )

    # Implied prerequisite example if level >= 4
    implied_audits = []
    if predicted_level >= 4:
        implied_audits.append(
            ImpliedPrerequisiteAudit(
                criterion_id="TRL-2.1",
                target_level=2,
                status="SATISFIED_INFERRED",
                inferred_from_trl=predicted_level,
                anchoring_evidence_id=evidence_sample.id,
                inference_rationale="Demonstrated physical laboratory validation implies underlying concept formulation is satisfied.",
                auditable=True
            )
        )

    assessment = FinalAssessment(
        predicted_trl=predicted_level,
        confidence=confidence,
        justification=f"Baseline Phase 1 Evaluation: {rationale}",
        satisfied_criteria=satisfied,
        implied_prerequisites_audit=implied_audits,
        missing_criteria=missing,
        contradictions=[],
        recommendations=[f"Conduct validation required for TRL {min(9, predicted_level + 1)}: {c}" for c in missing[:2]],
        supporting_evidence=[evidence_sample],
        agent_assessments={
            "optimist": AgentAssessment(
                agent_type=AgentType.OPTIMIST,
                initial_trl=min(9, predicted_level + 1),
                final_trl=predicted_level,
                reasoning="Optimist argument grounded in demonstrated achievements.",
                evidence_references=[evidence_sample.id],
                confidence=confidence
            ),
            "skeptic": AgentAssessment(
                agent_type=AgentType.SKEPTIC,
                initial_trl=max(1, predicted_level - 1),
                final_trl=predicted_level,
                reasoning="Skeptic challenge identifying unverified assertions and missing operational metrics.",
                evidence_references=[],
                confidence=confidence
            ),
        },
        debate_transcript=[
            DebateMessage(
                round_number=1,
                agent_type=AgentType.OPTIMIST,
                argument=f"Demonstrated achievements satisfy criteria for TRL {predicted_level}.",
                evidence_references=[evidence_sample.id]
            ),
            DebateMessage(
                round_number=1,
                agent_type=AgentType.SKEPTIC,
                argument=f"Validation remains incomplete for TRL {min(9, predicted_level + 1)}.",
                evidence_references=[]
            )
        ]
    )

    if output_path is not None:
        out_adapter = InternalOutputAdapter()
        out_adapter.write_assessment(assessment, output_path)

    return assessment

