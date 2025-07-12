import os
import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

def load_data():
    """Load processed datasets"""
    with open("data/processed_resumes.json", "r") as f:
        resumes = json.load(f)
    
    with open("data/processed_jobs.json", "r") as f:
        jobs = json.load(f)
    
    return resumes, jobs

def preprocess_text(text):
    """Simple text preprocessing"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text

def extract_documents(resumes, jobs):
    """Extract text documents from resumes and jobs"""
    documents = []
    
    # Extract resume documents
    for resume in resumes:
        doc = ""
        if "summary" in resume:
            doc += resume["summary"] + " "
        
        if "skills" in resume:
            doc += " ".join(resume["skills"]) + " "
        
        if "experience" in resume:
            for exp in resume["experience"]:
                if "description" in exp:
                    doc += exp["description"] + " "
        
        documents.append(preprocess_text(doc))
    
    # Extract job documents
    for job in jobs:
        doc = ""
        doc += job["title"] + " "
        doc += job["description"] + " "
        doc += " ".join(job["requirements"]) + " "
        
        documents.append(preprocess_text(doc))
    
    return documents

def train_tfidf_vectorizer(documents):
    """Train TF-IDF vectorizer"""
    print("Training TF-IDF vectorizer...")
    
    # Initialize vectorizer
    vectorizer = TfidfVectorizer(
        min_df=2,
        max_df=0.8,
        ngram_range=(1, 2)
    )
    
    # Fit vectorizer
    vectorizer.fit(documents)
    
    # Save vectorizer
    os.makedirs("models", exist_ok=True)
    with open("models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    
    print(f"Vectorizer trained with {len(vectorizer.get_feature_names_out())} features")
    return vectorizer

def evaluate_similarity(vectorizer, documents):
    """Evaluate similarity calculation"""
    print("Evaluating similarity calculation...")
    
    # Transform documents to vectors
    vectors = vectorizer.transform(documents)
    
    # Split data for evaluation
    X_train, X_test = train_test_split(vectors, test_size=0.2, random_state=42)
    
    # Calculate cosine similarity between documents
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Sample some pairs for evaluation
    n_samples = min(100, X_test.shape[0])
    similarities = cosine_similarity(X_test[:n_samples], X_test[:n_samples])
    
    # Print statistics
    print(f"Similarity statistics:")
    print(f"  Mean: {np.mean(similarities):.4f}")
    print(f"  Min: {np.min(similarities):.4f}")
    print(f"  Max: {np.max(similarities):.4f}")
    print(f"  Std: {np.std(similarities):.4f}")

def main():
    """Main function to train models"""
    # Load data
    resumes, jobs = load_data()
    print(f"Loaded {len(resumes)} resumes and {len(jobs)} jobs")
    
    # Extract documents
    documents = extract_documents(resumes, jobs)
    print(f"Extracted {len(documents)} documents")
    
    # Train vectorizer
    vectorizer = train_tfidf_vectorizer(documents)
    
    # Evaluate similarity
    evaluate_similarity(vectorizer, documents)
    
    print("Model training completed!")

if __name__ == "__main__":
    main()