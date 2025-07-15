from fastapi import APIRouter, HTTPException, status, Body
from typing import Dict, List, Any, Optional
import numpy as np

from app.services.advanced_nlp import nlp_processor
from app.services.performance_monitor import performance_monitor

router = APIRouter()

@router.post("/embeddings/bert")
@performance_monitor.monitor_performance("bert_embeddings_endpoint")
async def get_bert_embeddings(
    request: Dict[str, Any] = Body(...)
):
    """Get BERT embeddings for text"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for BERT embeddings"
            )
        
        embeddings = nlp_processor.get_bert_embeddings(text)
        
        return {
            "text": text,
            "embeddings": embeddings.tolist(),
            "vector_size": len(embeddings),
            "model": "bert-base-uncased"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting BERT embeddings: {str(e)}"
        )

@router.post("/embeddings/word2vec")
@performance_monitor.monitor_performance("word2vec_embeddings_endpoint")
async def get_word2vec_embeddings(
    request: Dict[str, Any] = Body(...)
):
    """Get Word2Vec embeddings for text"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for Word2Vec embeddings"
            )
        
        embeddings = nlp_processor.get_word2vec_embeddings(text)
        
        return {
            "text": text,
            "embeddings": embeddings.tolist(),
            "vector_size": len(embeddings),
            "model": "word2vec"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting Word2Vec embeddings: {str(e)}"
        )

@router.post("/embeddings/hybrid")
@performance_monitor.monitor_performance("hybrid_embeddings_endpoint")
async def get_hybrid_embeddings(
    request: Dict[str, Any] = Body(...)
):
    """Get multiple types of embeddings for comprehensive analysis"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for hybrid embeddings"
            )
        
        embeddings = nlp_processor.get_hybrid_embeddings(text)
        
        # Convert numpy arrays to lists for JSON serialization
        result = {}
        for key, embedding in embeddings.items():
            result[key] = {
                "embeddings": embedding.tolist(),
                "vector_size": len(embedding)
            }
        
        return {
            "text": text,
            "embeddings": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting hybrid embeddings: {str(e)}"
        )

@router.post("/entities/recognize")
@performance_monitor.monitor_performance("entity_recognition_endpoint")
async def recognize_entities(
    request: Dict[str, Any] = Body(...)
):
    """Perform advanced entity recognition on text"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for entity recognition"
            )
        
        entities = nlp_processor.advanced_entity_recognition(text)
        
        return {
            "text": text,
            "entities": entities,
            "total_entities": sum(len(entities[key]) for key in entities)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in entity recognition: {str(e)}"
        )

@router.post("/sentiment/analyze")
@performance_monitor.monitor_performance("sentiment_analysis_endpoint")
async def analyze_sentiment(
    request: Dict[str, Any] = Body(...)
):
    """Perform sentiment analysis on text"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for sentiment analysis"
            )
        
        sentiment = nlp_processor.sentiment_analysis(text)
        
        return {
            "text": text,
            "sentiment": sentiment
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in sentiment analysis: {str(e)}"
        )

@router.post("/phrases/extract")
@performance_monitor.monitor_performance("key_phrases_endpoint")
async def extract_key_phrases(
    request: Dict[str, Any] = Body(...)
):
    """Extract key phrases from text"""
    try:
        text = request.get("text", "")
        num_phrases = request.get("num_phrases", 10)
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for key phrase extraction"
            )
        
        phrases = nlp_processor.extract_key_phrases(text, num_phrases)
        
        return {
            "text": text,
            "key_phrases": phrases,
            "num_phrases": len(phrases)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting key phrases: {str(e)}"
        )

@router.post("/complexity/analyze")
@performance_monitor.monitor_performance("complexity_analysis_endpoint")
async def analyze_complexity(
    request: Dict[str, Any] = Body(...)
):
    """Analyze text complexity and readability"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for complexity analysis"
            )
        
        complexity = nlp_processor.analyze_text_complexity(text)
        
        return {
            "text": text,
            "complexity": complexity
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing text complexity: {str(e)}"
        )

@router.post("/analysis/comprehensive")
@performance_monitor.monitor_performance("comprehensive_analysis_endpoint")
async def comprehensive_analysis(
    request: Dict[str, Any] = Body(...)
):
    """Perform comprehensive text analysis including all NLP features"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for comprehensive analysis"
            )
        
        analysis = nlp_processor.comprehensive_text_analysis(text)
        
        # Convert numpy arrays to lists for JSON serialization
        if 'embeddings' in analysis:
            for key, embedding in analysis['embeddings'].items():
                analysis['embeddings'][key] = embedding.tolist()
        
        return {
            "text": text,
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in comprehensive analysis: {str(e)}"
        )

@router.post("/resume/analyze")
@performance_monitor.monitor_performance("resume_analysis_endpoint")
async def analyze_resume(
    request: Dict[str, Any] = Body(...)
):
    """Analyze a complete resume with all NLP features"""
    try:
        resume_data = request.get("resume", {})
        
        if not resume_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume data is required"
            )
        
        # Combine all text from resume
        text_parts = []
        
        if "summary" in resume_data:
            text_parts.append(resume_data["summary"])
        
        if "skills" in resume_data:
            text_parts.append("Skills: " + ", ".join(resume_data["skills"]))
        
        if "experience" in resume_data:
            for exp in resume_data["experience"]:
                if "description" in exp:
                    text_parts.append(exp["description"])
        
        if "education" in resume_data:
            for edu in resume_data["education"]:
                if "field" in edu:
                    text_parts.append(f"Education: {edu['field']}")
        
        combined_text = " ".join(text_parts)
        
        # Perform comprehensive analysis
        analysis = nlp_processor.comprehensive_text_analysis(combined_text)
        
        # Convert numpy arrays to lists
        if 'embeddings' in analysis:
            for key, embedding in analysis['embeddings'].items():
                analysis['embeddings'][key] = embedding.tolist()
        
        return {
            "resume_id": resume_data.get("id", "unknown"),
            "analysis": analysis,
            "text_length": len(combined_text)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}"
        )

@router.post("/job/analyze")
@performance_monitor.monitor_performance("job_analysis_endpoint")
async def analyze_job(
    request: Dict[str, Any] = Body(...)
):
    """Analyze a complete job posting with all NLP features"""
    try:
        job_data = request.get("job", {})
        
        if not job_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job data is required"
            )
        
        # Combine all text from job posting
        text_parts = []
        
        if "title" in job_data:
            text_parts.append(job_data["title"])
        
        if "description" in job_data:
            text_parts.append(job_data["description"])
        
        if "requirements" in job_data:
            text_parts.append("Requirements: " + " ".join(job_data["requirements"]))
        
        if "qualifications" in job_data:
            text_parts.append("Qualifications: " + " ".join(job_data["qualifications"]))
        
        if "skills_required" in job_data:
            text_parts.append("Skills: " + ", ".join(job_data["skills_required"]))
        
        combined_text = " ".join(text_parts)
        
        # Perform comprehensive analysis
        analysis = nlp_processor.comprehensive_text_analysis(combined_text)
        
        # Convert numpy arrays to lists
        if 'embeddings' in analysis:
            for key, embedding in analysis['embeddings'].items():
                analysis['embeddings'][key] = embedding.tolist()
        
        return {
            "job_id": job_data.get("id", "unknown"),
            "analysis": analysis,
            "text_length": len(combined_text)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing job: {str(e)}"
        )

@router.get("/models/status")
async def get_model_status():
    """Get status of NLP models"""
    try:
        status = {
            "bert_model": nlp_processor.bert_model is not None,
            "word2vec_model": nlp_processor.word2vec_model is not None,
            "spacy_model": nlp_processor.nlp is not None,
            "tfidf_vectorizer": nlp_processor.tfidf_vectorizer is not None
        }
        
        return {
            "models": status,
            "available_features": list(status.keys()),
            "total_models": sum(status.values())
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting model status: {str(e)}"
        ) 