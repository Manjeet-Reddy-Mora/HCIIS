import re
from nlp_utils import get_sentences, get_words

# --- Explainable linguistic cues ---

DECISION_VERBS = {
    "decide", "choose", "select", "agree", "accept", "reject",
    "approve", "commit", "proceed", "consider", "opt", "authorize",
    "confirm", "decline", "terminate", "continue", "discontinue",
    "enroll", "withdraw", "sign", "cancel"
}

RISK_TERMS = {
    # General risk & harm
    "risk", "loss", "damage", "harm", "threat", "danger", "exposure",
    "impact", "consequence", "liability", "uncertainty",

    # Financial & business risk
    "cost", "penalty", "fine", "charge", "expense", "debt",
    "default", "bankruptcy", "losses", "decline",

    # Legal & contractual risk
    "liability", "breach", "violation", "noncompliance", "lawsuit",
    "claim", "dispute", "termination", "revocation", "sanction",

    # Operational & technical risk
    "failure", "outage", "downtime", "error", "malfunction",
    "breakdown", "defect", "vulnerability", "incident",

    # Security & safety risk
    "attack", "breach", "leak", "theft", "fraud", "compromise",
    "unauthorized", "unsafe", "hazard",

    # Human & reputational risk
    "injury", "fatality", "reputation", "reputational",
    "trust", "misconduct", "negligence"
}

AMBIGUOUS_TERMS = {
    "may", "might", "could", "possible", "potential", "likely",
    "subject to", "as applicable", "at discretion", "from time to time",
    "where feasible", "as appropriate", "depending on", "in some cases",
    "to the extent possible"
}

VAGUE_PHRASES = {
    "as necessary", "if required", "where appropriate",
    "reasonable efforts", "best efforts", "as determined",
    "at our discretion", "when needed", "as decided",
    "subject to change", "without notice"
}


def decision_risk(text: str) -> dict:
    """
    Explainable decision risk & ambiguity analysis.
    """

    sentences = get_sentences(text)
    words = [w.lower() for w in get_words(text) if w.isalpha()]

    if not sentences:
        return {
            "density": 0,
            "ambiguity": 0,
            "notes": "Text too short to analyze decision risk."
        }

    decision_sentences = 0
    risk_mentions = 0
    ambiguity_markers = 0
    vague_commitments = 0

    for s in sentences:
        s_words = set(w.lower() for w in get_words(s) if w.isalpha())
        s_lower = s.lower()

        if s_words & DECISION_VERBS:
            decision_sentences += 1

        risk_mentions += sum(1 for r in RISK_TERMS if r in s_lower)
        ambiguity_markers += sum(1 for a in AMBIGUOUS_TERMS if a in s_lower)
        vague_commitments += sum(1 for v in VAGUE_PHRASES if v in s_lower)

    total_sentences = len(sentences)

    # --- Metrics ---
    decision_density = round(decision_sentences / total_sentences, 3)
    raw_ambiguity = ambiguity_markers + vague_commitments
    ambiguity_score = round(
    min(raw_ambiguity / max(total_sentences, 1), 1.0),
    3
)


    # --- Interpretation ---
    notes = []

    if decision_density > 0.3:
        notes.append(
            "The text contains frequent decision-related statements."
        )
    elif decision_density > 0:
        notes.append(
            "The text contains some decision-related content."
        )
    else:
        notes.append(
            "Few explicit decisions are presented in the text."
        )

    if ambiguity_score > 0.4:
        notes.append(
            "High ambiguity detected: commitments and outcomes are unclear."
        )
    elif ambiguity_score > 0:
        notes.append(
            "Moderate ambiguity detected in commitments or conditions."
        )
    else:
        notes.append(
            "Decisions and commitments appear relatively clear."
        )

    if decision_sentences > 0 and risk_mentions == 0:
        notes.append(
            "Decisions are presented without clearly stated risks."
        )

    return {
        "density": decision_density,
        "ambiguity": ambiguity_score,
        "notes": " ".join(notes),
        "details": {
            "decision_sentences": decision_sentences,
            "risk_mentions": risk_mentions,
            "ambiguity_markers": ambiguity_markers,
            "vague_phrases": vague_commitments
        }
    }
