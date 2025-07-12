from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
import os
from typing import List, Tuple, Dict, Any
from app.services.text_processor import TextProcessor

class ResumeJobVectorizer:
    def __init__(self, model_path: str = None):
        self.text_processor = TextProcessor()
        self.vectorizer = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.vectorizer = TfidfVectorizer(
                min_df=2,
                max_df=0.8,
                ngram_range=(1, 2)
            )
    
    def train(self, documents: List[str]) -> None:
        """Train the vectorizer on a corpus of documents"""
        processed_docs = [self.text_processor.preprocess_text(doc) for doc in documents]
        self.vectorizer.fit(processed_docs)
    
    def vectorize(self, text: str) -> np.ndarray:
        """Convert text to vector representation"""
        if not self.vectorizer:
            raise ValueError("Vectorizer not trained or loaded")
        
        processed_text = self.text_processor.preprocess_text(text)
        vector = self.vectorizer.transform([processed_text])
        return vector.toarray()[0]
    
    def save_model(self, path: str) -> None:
        """Save the trained vectorizer model"""
        with open(path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_model(self, path: str) -> None:
        """Load a trained vectorizer model"""
        with open(path, 'rb') as f:
            self.vectorizer = pickle.load(f)