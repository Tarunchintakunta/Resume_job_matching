import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def load_training_corpus():
    """Load training corpus"""
    try:
        with open("data/training_corpus.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Training corpus not found. Run prepare_data.py first.")
        return []

def train_tfidf_vectorizer(documents):
    """Train TF-IDF vectorizer on training corpus"""
    print("Training TF-IDF vectorizer...")

    vectorizer = TfidfVectorizer(
        min_df=1,
        max_df=0.9,
        ngram_range=(1, 2)
    )

    vectorizer.fit(documents)

    os.makedirs("models", exist_ok=True)
    with open("models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"Vectorizer trained with {len(vectorizer.get_feature_names_out())} features")
    return vectorizer

def main():
    """Train models using the training corpus"""
    documents = load_training_corpus()
    if not documents:
        return

    print(f"Loaded {len(documents)} training documents")
    train_tfidf_vectorizer(documents)
    print("Model training completed!")

if __name__ == "__main__":
    main()
