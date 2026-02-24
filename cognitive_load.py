from nlp_utils import (
    get_sentences,
    get_words,
    sentence_lengths,
    lexical_density
)
import statistics


def cognitive_load(text: str) -> dict:
    """
    Explainable cognitive load estimation based on:
    - Sentence length
    - Sentence length variance
    - Lexical density
    """

    sentences = get_sentences(text)
    words = get_words(text)

    if len(sentences) == 0:
        return {
            "load": 0,
            "attention_drop": "Low",
            "explanation": "Text too short to analyze cognitive load."
        }

    sent_lengths = sentence_lengths(sentences)

    avg_sentence_length = statistics.mean(sent_lengths)
    sentence_variance = statistics.pvariance(sent_lengths)
    lex_density = lexical_density(words)

    # --- Cognitive Load Scoring (Explainable) ---
    load_score = (
    (min(avg_sentence_length / 25, 1) * 40) +
    (min(sentence_variance / 50, 1) * 30) +
    (min(lex_density / 0.7, 1) * 30)
    )
    
    load_score = round(load_score, 2)


    # --- Attention Drop Risk ---
    if load_score > 70:
        attention = "High"
    elif load_score > 40:
        attention = "Medium"
    else:
        attention = "Low"

    explanation = (
        f"The cognitive load is influenced by an average sentence length of "
        f"{round(avg_sentence_length,1)} words, sentence structure variation, "
        f"and a lexical density of {lex_density}. "
        f"Higher values indicate greater mental effort required to process the text."
    )

    return {
        "load": load_score,
        "attention_drop": attention,
        "explanation": explanation
    }

