import statistics
from nlp_utils import get_sentences, get_words

EVIDENCE_MARKERS = {
    "data", "dataset", "study", "studies", "evidence", "research",
    "analysis", "report", "survey", "experiment", "results",
    "statistics", "figures", "findings", "metrics", "sample",
    "observations", "measured", "evaluated", "validated"
}

RHETORICAL_WORDS = {
    "very", "extremely", "clearly", "obviously", "undoubtedly",
    "remarkably", "highly", "significantly", "truly", "deeply",
    "entirely", "completely", "totally", "absolutely", "purely"
}


def information_quality(text: str) -> dict:
    """
    Explainable Information Quality Index (IQI).
    """

    sentences = get_sentences(text)
    words = [w.lower() for w in get_words(text) if w.isalpha()]

    if not sentences or not words:
        return {
            "quality": 0,
            "analysis": "Text too short to assess information quality."
        }

    total_words = len(words)
    total_sentences = len(sentences)

    # --- Evidence density ---
    evidence_count = sum(1 for w in words if w in EVIDENCE_MARKERS)
    evidence_density = evidence_count / total_words

    # --- Rhetoric density ---
    rhetoric_count = sum(1 for w in words if w in RHETORICAL_WORDS)
    rhetoric_density = rhetoric_count / total_words

    # --- Redundancy estimation ---
    unique_words = set(words)
    redundancy_ratio = 1 - (len(unique_words) / total_words)

    # --- Sentence information variance ---
    sentence_lengths = [len(get_words(s)) for s in sentences]
    length_variance = statistics.pvariance(sentence_lengths)

    # --- Quality scoring ---
    raw_quality = (
    (min(evidence_density / 0.05, 1) * 35) +
    ((1 - min(rhetoric_density / 0.05, 1)) * 25) +
    ((1 - redundancy_ratio) * 25) +
    (min(length_variance / 40, 1) * 15)
    )
    
    quality_score = round(raw_quality * 100, 2)


    # --- Interpretation ---
    insights = []

    if evidence_density > 0.02:
        insights.append("Evidence-backed language detected.")
    else:
        insights.append("Limited explicit evidence detected.")

    if rhetoric_density > 0.02:
        insights.append("Rhetorical emphasis is relatively high.")
    else:
        insights.append("Rhetorical emphasis is minimal.")

    if redundancy_ratio > 0.5:
        insights.append("High redundancy suggests filler content.")
    else:
        insights.append("Low redundancy suggests informational density.")

    analysis = " ".join(insights)

    return {
        "quality": quality_score,
        "analysis": analysis,
        "details": {
            "evidence_density": round(evidence_density, 4),
            "rhetoric_density": round(rhetoric_density, 4),
            "redundancy_ratio": round(redundancy_ratio, 4),
            "sentence_variance": round(length_variance, 2)
        }
    }
