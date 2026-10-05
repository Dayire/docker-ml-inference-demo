"""Generate a tiny teaching artifact. This is not a validated sentiment model."""
import os
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


def main():
    texts = [
        "I love this excellent wonderful product", "great happy fantastic service",
        "amazing good delightful experience", "I like this brilliant lovely film",
        "I hate this terrible awful product", "bad sad horrible service",
        "poor disappointing unpleasant experience", "I dislike this dreadful boring film",
    ]
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(texts, ["positive"] * 4 + ["negative"] * 4)
    path = Path(os.getenv("MODEL_PATH", "models/sentiment.joblib"))
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"Saved teaching model to {path}")


if __name__ == "__main__":
    main()
