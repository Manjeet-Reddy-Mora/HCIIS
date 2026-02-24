import re
from nlp_utils import get_sentences, get_words

# --- Lexicons (explainable & editable) ---
FEAR_WORDS = {
     "crisis", "danger", "threat", "risk", "urgent", "warning",
    "collapse", "disaster", "catastrophe", "panic", "fear", "loss",
    "fatal", "deadly", "severe", "critical", "emergency", "alarming",
    "unstable", "unsafe", "harm", "damage", "destruction", "chaos",
    "uncertain", "instability", "breakdown", "failure", "attack",
    "exposed", "vulnerable", "irreversible"
}

AUTHORITY_PHRASES = {
    "experts say", "studies show", "research proves", "scientists agree",
    "according to experts", "authorities say", "official sources confirm",
    "it is widely believed", "industry leaders agree", "medical experts warn",
    "government sources indicate", "analysts predict", "reports suggest",
    "research indicates", "evidence suggests", "it is well known"
}

CERTAINTY_WORDS = {
     "always", "never", "undeniable", "guaranteed", "certainly",
    "definitely", "absolutely", "no doubt", "everyone knows",
    "proven", "inevitable", "unquestionable", "without exception",
    "beyond doubt", "indisputable", "conclusive", "undoubtedly"
}

EMOTIONAL_WORDS = {
    "shocking", "outrageous", "incredible", "devastating", "amazing",
    "terrible", "unbelievable", "heartbreaking", "disturbing",
    "horrifying", "tragic", "disgusting", "remarkable", "astonishing",
    "terrifying", "emotional", "painful", "exciting", "frightening"
}


def _count_phrases(text, phrases):
    text_l = text.lower()
    return sum(1 for p in phrases if p in text_l)


def _count_words(words, lexicon):
    return sum(1 for w in words if w in lexicon)


def manipulation_score(text: str) -> dict:
    """
    Explainable manipulation & persuasion analysis.
    Returns a score + detailed breakdown.
    """

    sentences = get_sentences(text)
    words = [w.lower() for w in get_words(text) if w.isalpha()]

    if not words:
        return {
            "score": 0,
            "details": "Text too short to analyze manipulation."
        }

    # --- Feature counts ---
    fear_count = _count_words(words, FEAR_WORDS)
    authority_count = _count_phrases(text, AUTHORITY_PHRASES)
    certainty_count = _count_words(words, CERTAINTY_WORDS)
    emotional_count = _count_words(words, EMOTIONAL_WORDS)

    total_words = len(words)

    # --- Normalized ratios ---
    fear_ratio = fear_count / total_words
    certainty_ratio = certainty_count / total_words
    emotional_ratio = emotional_count / total_words

    # --- Scoring (weights are explainable) ---
    sentence_factor = max(len(sentences), 1)
    score = (
        fear_ratio * 30 +
        certainty_ratio * 25 +
        emotional_ratio * 25 +
        (authority_count / sentence_factor) * 20
    )

    score = round(min(score * 100, 100), 2)

    # --- Explanation ---
    explanation_parts = []

    if fear_count > 0:
        explanation_parts.append(
            f"Fear framing detected ({fear_count} fear-related terms)."
        )

    if authority_count > 0:
        explanation_parts.append(
            f"Authority masking present ({authority_count} authoritative phrases without evidence)."
        )

    if certainty_count > 0:
        explanation_parts.append(
            f"High certainty language used ({certainty_count} absolute terms)."
        )

    if emotional_count > 0:
        explanation_parts.append(
            f"Emotionally loaded language detected ({emotional_count} terms)."
        )

    if not explanation_parts:
        explanation = (
            "Minimal manipulative or persuasive language detected. "
            "The text appears largely informational."
        )
    else:
        explanation = " ".join(explanation_parts)

    return {
        "score": score,
        "details": explanation,
        "breakdown": {
            "fear_terms": fear_count,
            "authority_phrases": authority_count,
            "certainty_terms": certainty_count,
            "emotional_terms": emotional_count
        }
    }
