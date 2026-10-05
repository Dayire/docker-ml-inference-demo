import os
from functools import lru_cache

import joblib


@lru_cache(maxsize=1)
def load_model():
    # Only load our own trusted build artifact: pickle/joblib can execute code.
    return joblib.load(os.getenv("MODEL_PATH", "models/sentiment.joblib"))


def predict(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    max_chars = int(os.getenv("MAX_CHARS", "200"))
    if max_chars < 1:
        raise ValueError("MAX_CHARS must be positive")
    used = text[:max_chars]
    model = load_model()
    probabilities = model.predict_proba([used])[0]
    index = int(probabilities.argmax())
    return {
        "text": text,
        "text_used": used,
        "label": str(model.classes_[index]),
        "confidence": round(float(probabilities[index]), 4),
        "max_chars": max_chars,
        "truncated": len(text) > max_chars,
    }
