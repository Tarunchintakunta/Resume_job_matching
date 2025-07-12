import os
import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data():
    """Load processed datasets"""
    try:
        with open("data/processed_resumes.json", "r") as f:
            resumes = json.load(f)
        
        with open("data/processed_jobs.json", "r") as f:
            jobs = json.load(f)
        
        return resumes, jobs
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please run prepare_data.py first to generate the datasets.")
        return [], []

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
        
        documents.append(doc.lower())
    
    # Extract job documents
    for job in jobs:
        doc = ""
        doc += job["title"] + " "
        doc += job["description"] + " "
        doc += " ".join(job["requirements"]) + " "
        
        documents.append(doc.lower())
    
    return documents

def train_tfidf_vectorizer(documents):
    """Train TF-IDF vectorizer"""
    print("Training TF-IDF vectorizer...")
    
    # Initialize vectorizer
    vectorizer = TfidfVectorizer(
        min_df=1,
        max_df=0.9,
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

def main():
    """Main function to train models"""
    # Load data
    resumes, jobs = load_data()
    if not resumes or not jobs:
        return
        
    print(f"Loaded {len(resumes)} resumes and {len(jobs)} jobs")
    
    # Extract documents
    documents = extract_documents(resumes, jobs)
    print(f"Extracted {len(documents)} documents")
    
    # Train vectorizer
    vectorizer = train_tfidf_vectorizer(documents)
    
    print("Model training completed!")

if __name__ == "__main__":
    main()