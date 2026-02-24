from collections import Counter
from nlp_utils import get_words, get_sentences

# ---------------- Emotion Lexicons (Explainable) ----------------

EMOTION_LEXICON = {
    "joy": {
        "happy", "joy", "delight", "pleased", "excited", "satisfied",
        "hope", "optimistic", "relieved", "cheerful", "positive"
    },
    "sadness": {
        "sad", "loss", "grief", "depressed", "unhappy", "regret",
        "disappointed", "hopeless", "miserable", "downcast"
    },
    "anger": {
        "angry", "furious", "rage", "outrage", "annoyed",
        "frustrated", "irritated", "resentful", "hostile"
    },
    "fear": {
        "fear", "afraid", "panic", "threat", "danger", "risk",
        "anxious", "worried", "terrified", "nervous"
    },
    "surprise": {
        "surprised", "shocked", "unexpected", "sudden",
        "astonished", "startled"
    }
}

POSITIVE_WORDS = {
    "good", "great", "positive", "beneficial", "excellent",
    "success", "effective", "improved", "efficient",
    "reliable", "valuable", "strong", "favorable"
}

NEGATIVE_WORDS = {
    "bad", "negative", "poor", "harmful", "failure",
    "problem", "ineffective", "weak", "costly",
    "dangerous", "damaging", "unreliable"
}


def emotion_analysis(text: str) -> dict:
    """
    Explainable emotion & tone analysis.
    Measures:
    - Dominant emotion
    - Emotional volatility
    - Suppressed emotion signal
    """

    words = [w.lower() for w in get_words(text) if w.isalpha()]
    sentences = get_sentences(text)

    if not words:
        return {
            "dominant": "Neutral",
            "volatility": 0.0,
            "summary": "Text too short for emotion analysis.",
            "counts": {}
        }

    # ---------------- Count emotions ----------------
    emotion_counts = Counter()

    for emotion, lexicon in EMOTION_LEXICON.items():
        emotion_counts[emotion] = sum(1 for w in words if w in lexicon)

    dominant_emotion = (
        emotion_counts.most_common(1)[0][0]
        if emotion_counts.most_common(1)[0][1] > 0
        else "Neutral"
    )

    # ---------------- Polarity ----------------
    positive_count = sum(1 for w in words if w in POSITIVE_WORDS)
    negative_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    # ---------------- Emotional Volatility ----------------
    emotion_changes = 0
    for s in sentences:
        s_words = set(w.lower() for w in get_words(s) if w.isalpha())
        if (s_words & POSITIVE_WORDS) and (s_words & NEGATIVE_WORDS):
            emotion_changes += 1

    volatility = round(
        emotion_changes / max(len(sentences), 1),
        3
    )

    # ---------------- Suppressed Emotion Heuristic ----------------
    if dominant_emotion == "Neutral" and (positive_count + negative_count) > 0:
        suppression_note = (
            "Emotion appears suppressed or indirectly expressed."
        )
    else:
        suppression_note = "Emotional tone appears explicit."

    summary = (
        f"The dominant emotional tone is {dominant_emotion.capitalize()}. "
        f"Emotional volatility is {volatility}. "
        f"{suppression_note}"
    )

    return {
        "dominant": dominant_emotion.capitalize(),
        "volatility": volatility,
        "summary": summary,
        "counts": dict(emotion_counts)
    }
