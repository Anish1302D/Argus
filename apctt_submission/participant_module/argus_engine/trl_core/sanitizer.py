"""
Untrusted Data Sanitizer & Prompt Injection Defense.
Enforces strict boundaries between untrusted document text and model reasoning prompts.
"""

import re
import unicodedata
from typing import List, NamedTuple, Set


class SanitizedResult(NamedTuple):
    cleaned_text: str
    is_safe: bool
    detected_threats: List[str]


# Common prompt injection, role-hijacking, and jailbreak patterns in untrusted technical text
PROMPT_INJECTION_PATTERNS = [
    (r"(?i)\bignore\s+(all\s+)?(previous\s+|prior\s+|above\s+)?(instructions|prompts|directions)\b", "INSTRUCTION_OVERRIDE"),
    (r"(?i)\b(system\s+override|system\s+prompt|developer\s+mode)\b", "SYSTEM_ROLE_HIJACK"),
    (r"(?i)\b(you\s+must|you\s+are\s+now|act\s+as)\s+(an?\s+)?(ai|unrestricted|evaluator|admin)\b", "ROLEPLAY_HIJACK"),
    (r"(?i)\b(award|assign|classify|predict|output)\s+(only\s+)?(trl\s*[1-9]|level\s*[1-9])\b", "OUTPUT_FORCING"),
    (r"(?i)\b(disregard\s+the\s+evidence|evidence\s+is\s+unnecessary)\b", "EVIDENCE_BYPASS"),
    (r"(?i)<\s*/?\s*(system|instruction|prompt|context|assistant|human)\s*>", "RESERVED_TAG_INJECTION"),
    (r"(?i)```\s*(system|override|admin)\b", "CODEBLOCK_ESCALATION"),
]

# Zero-width and hidden unicode characters often used for adversarial bypass
DANGEROUS_UNICODE_CHARS: Set[str] = {
    "\u200B",  # Zero-width space
    "\u200C",  # Zero-width non-joiner
    "\u200D",  # Zero-width joiner
    "\uFEFF",  # Zero-width no-break space / BOM
    "\u202A",  # Left-to-right embedding
    "\u202B",  # Right-to-left embedding
    "\u202D",  # Left-to-right override
    "\u202E",  # Right-to-left override
}


def sanitize_text(text: str) -> SanitizedResult:
    """
    Sanitize raw text extracted from untrusted documents.
    1. Strips dangerous hidden/zero-width unicode characters.
    2. Normalizes unicode representation (NFKC).
    3. Detects known prompt injection, system role override, and output-forcing patterns.
    4. Escapes reserved XML tags that could break agent system prompts.
    """
    if not text:
        return SanitizedResult(cleaned_text="", is_safe=True, detected_threats=[])

    # Strip dangerous zero-width and bidirectional override characters
    cleaned_chars = [c for c in text if c not in DANGEROUS_UNICODE_CHARS]
    cleaned = "".join(cleaned_chars)

    # Normalize unicode
    cleaned = unicodedata.normalize("NFKC", cleaned)

    # Detect threats
    detected_threats: List[str] = []
    for pattern, threat_type in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned):
            detected_threats.append(threat_type)

    # Neutralize XML tags that might clash with delimiter wrappers
    # E.g. replace <untrusted_payload> or <system> with escaped forms
    cleaned = re.sub(r"<\s*(/?)untrusted_payload\s*>", r"[\1untrusted_payload]", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<\s*(/?)system\s*>", r"[\1system]", cleaned, flags=re.IGNORECASE)

    is_safe = len(detected_threats) == 0
    return SanitizedResult(cleaned_text=cleaned, is_safe=is_safe, detected_threats=detected_threats)


def wrap_untrusted_payload(text: str, payload_id: str = "doc_content") -> str:
    """
    Wrap untrusted text in strict, well-defined XML encapsulation tags for agent consumption.
    Agent prompts must be instructed to treat everything within this tag purely as passive data.
    """
    sanitized = sanitize_text(text)
    return (
        f'<untrusted_document_payload id="{payload_id}" threats_detected="{len(sanitized.detected_threats)}">\n'
        f"{sanitized.cleaned_text}\n"
        f"</untrusted_document_payload>"
    )
