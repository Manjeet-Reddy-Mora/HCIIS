import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Basic text cleaning for NLP analysis.
    - Removes extra whitespace
    - Normalizes punctuation
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\n", " ").strip()
    return text


def get_sentences(text: str):
    """Split text into sentences"""
    return sent_tokenize(text)


def get_words(text: str):
    """Tokenize text into words"""
    return word_tokenize(text.lower())


def sentence_lengths(sentences):
    """Return list of sentence lengths"""
    return [len(word_tokenize(s)) for s in sentences]


def lexical_density(words):
    """
    Lexical density = content words / total words
    High density → higher cognitive effort
    """
    content_words = [w for w in words if w.isalpha() and w not in STOP_WORDS]
    if len(words) == 0:
        return 0
    return round(len(content_words) / len(words), 3)
