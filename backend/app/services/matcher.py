import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

class ResumeMatcher:
    def __init__(self, vector_weight: float = 0.6, skills_weight: float = 0.4):
        self.vector_weight = vector_weight
        self.skills_weight = skills_weight
    
    def calculate_match_score(self, 
                             resume_vector: np.ndarray, 
                             job_vector: np.ndarray,
                             resume_skills: List[str], 
                             job_skills: List[str]) -> Dict[str, Any]:
        """
        Calculate match score between resume and job
        
        Args:
            resume_vector: Vector representation of resume
            job_vector: Vector representation of job
            resume_skills: List of skills extracted from resume
            job_skills: List of skills required for job
            
        Returns:
            Dictionary with match score and details
        """
        # Calculate vector similarity (cosine similarity)
        vector_similarity = cosine_similarity([resume_vector], [job_vector])[0][0]
        
        # Calculate skills match
        if job_skills and len(job_skills) > 0:
            matching_skills = set(resume_skills).intersection(set(job_skills))
            missing_skills = set(job_skills) - set(resume_skills)
            skills_match_ratio = len(matching_skills) / len(job_skills)
        else:
            matching_skills = set()
            missing_skills = set()
            skills_match_ratio = 0.0
        
        # Calculate weighted score
        weighted_score = (self.vector_weight * vector_similarity) + (self.skills_weight * skills_match_ratio)
        
        return {
            "score": weighted_score,
            "details": {
                "vector_similarity": float(vector_similarity),
                "skills_match_ratio": skills_match_ratio,
                "matching_skills": list(matching_skills),
                "missing_skills": list(missing_skills)
            }
        }
    
    def rank_resumes(self, job: Dict[str, Any], resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank resumes based on match score for a given job
        
        Args:
            job: Job posting data with vector and skills
            resumes: List of resume data with vector and skills
            
        Returns:
            List of match results with scores and ranking
        """
        match_results = []
        
        for idx, resume in enumerate(resumes):
            match_data = self.calculate_match_score(
                resume.get("vector", []),
                job.get("vector", []),
                resume.get("skills", []),
                job.get("skills_required", [])
            )
            
            match_results.append({
                "resume_id": resume["id"],
                "job_id": job["id"],
                "score": match_data["score"],
                "details": match_data["details"]
            })
        
        # Sort by score in descending order
        match_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Add ranking
        for i, result in enumerate(match_results):
            result["rank"] = i + 1
        
        return match_results