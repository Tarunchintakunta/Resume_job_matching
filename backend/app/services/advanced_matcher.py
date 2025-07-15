import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
import re
from collections import defaultdict
import json

class AdvancedResumeMatcher:
    def __init__(self, 
                 vector_weight: float = 0.5, 
                 skills_weight: float = 0.3,
                 experience_weight: float = 0.2,
                 bias_detection: bool = True):
        self.vector_weight = vector_weight
        self.skills_weight = skills_weight
        self.experience_weight = experience_weight
        self.bias_detection = bias_detection
        
        # Load skill synonyms for semantic matching
        self.skill_synonyms = self._load_skill_synonyms()
        
        # Bias detection patterns
        self.bias_patterns = {
            'gender': {
                'male_indicators': ['he', 'him', 'his', 'male', 'man', 'men', 'guy', 'guys'],
                'female_indicators': ['she', 'her', 'hers', 'female', 'woman', 'women', 'lady', 'ladies']
            },
            'age': {
                'young_indicators': ['recent graduate', 'fresh', 'entry-level', 'junior', 'young'],
                'experienced_indicators': ['senior', 'veteran', 'experienced', 'seasoned', 'mature']
            },
            'education': {
                'elite_schools': ['harvard', 'stanford', 'mit', 'yale', 'princeton', 'oxford', 'cambridge'],
                'general_schools': ['university', 'college', 'institute']
            }
        }
    
    def _load_skill_synonyms(self) -> Dict[str, List[str]]:
        """Load skill synonyms for semantic matching"""
        return {
            # Programming Languages
            "Python": ["python", "py", "python3", "python programming"],
            "JavaScript": ["javascript", "js", "ecmascript", "es6", "es2015"],
            "Java": ["java", "j2ee", "j2se", "spring java"],
            "C++": ["c++", "cpp", "c plus plus", "c++ programming"],
            "C#": ["c#", "csharp", "dotnet", ".net", "asp.net"],
            
            # Frameworks
            "React": ["react", "reactjs", "react.js", "react frontend"],
            "Angular": ["angular", "angularjs", "angular.js", "angular frontend"],
            "Vue.js": ["vue", "vuejs", "vue.js", "vue frontend"],
            "Node.js": ["node", "nodejs", "node.js", "express", "express.js"],
            "Django": ["django", "django framework", "python django"],
            "Flask": ["flask", "flask framework", "python flask"],
            
            # Databases
            "SQL": ["sql", "mysql", "postgresql", "oracle sql", "database"],
            "MongoDB": ["mongodb", "mongo", "nosql", "document database"],
            "Redis": ["redis", "cache", "in-memory database"],
            
            # Cloud & DevOps
            "AWS": ["aws", "amazon web services", "amazon aws", "cloud aws"],
            "Docker": ["docker", "containerization", "docker containers"],
            "Kubernetes": ["kubernetes", "k8s", "container orchestration"],
            
            # Machine Learning
            "Machine Learning": ["ml", "machine learning", "ai", "artificial intelligence"],
            "TensorFlow": ["tensorflow", "tf", "google tensorflow"],
            "PyTorch": ["pytorch", "torch", "facebook pytorch"],
            "NLP": ["nlp", "natural language processing", "text processing"],
            
            # Data Science
            "Data Analysis": ["data analysis", "analytics", "data analytics", "statistical analysis"],
            "Pandas": ["pandas", "python pandas", "data manipulation"],
            "NumPy": ["numpy", "numerical python", "array processing"]
        }
    
    def semantic_skill_matching(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        """
        Perform semantic skill matching using synonyms and fuzzy matching
        """
        if not job_skills:
            return {
                "matching_skills": [],
                "missing_skills": [],
                "skills_match_ratio": 0.0,
                "semantic_matches": []
            }
        
        matching_skills = []
        missing_skills = []
        semantic_matches = []
        
        # Convert to lowercase for matching
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        for job_skill in job_skills:
            job_skill_lower = job_skill.lower()
            matched = False
            
            # Direct match
            if job_skill_lower in resume_skills_lower:
                matching_skills.append(job_skill)
                matched = True
            
            # Synonym match
            if not matched and job_skill in self.skill_synonyms:
                synonyms = self.skill_synonyms[job_skill]
                for synonym in synonyms:
                    if synonym in resume_skills_lower:
                        matching_skills.append(job_skill)
                        semantic_matches.append({
                            "job_skill": job_skill,
                            "resume_skill": resume_skills[resume_skills_lower.index(synonym)],
                            "match_type": "synonym"
                        })
                        matched = True
                        break
            
            # Partial match (fuzzy matching)
            if not matched:
                for resume_skill in resume_skills_lower:
                    if (job_skill_lower in resume_skill or 
                        resume_skill in job_skill_lower or
                        self._calculate_similarity(job_skill_lower, resume_skill) > 0.8):
                        matching_skills.append(job_skill)
                        semantic_matches.append({
                            "job_skill": job_skill,
                            "resume_skill": resume_skills[resume_skills_lower.index(resume_skill)],
                            "match_type": "partial"
                        })
                        matched = True
                        break
            
            if not matched:
                missing_skills.append(job_skill)
        
        skills_match_ratio = len(matching_skills) / len(job_skills) if job_skills else 0.0
        
        return {
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "skills_match_ratio": skills_match_ratio,
            "semantic_matches": semantic_matches
        }
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using Levenshtein distance"""
        if len(str1) < len(str2):
            return self._calculate_similarity(str2, str1)
        
        if len(str2) == 0:
            return 0.0
        
        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        max_len = max(len(str1), len(str2))
        return 1 - (previous_row[-1] / max_len) if max_len > 0 else 1.0
    
    def detect_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect potential bias in text based on patterns
        """
        if not self.bias_detection:
            return {"bias_detected": False, "bias_score": 0.0, "bias_types": []}
        
        text_lower = text.lower()
        bias_types = []
        bias_score = 0.0
        
        # Gender bias detection
        male_count = sum(text_lower.count(indicator) for indicator in self.bias_patterns['gender']['male_indicators'])
        female_count = sum(text_lower.count(indicator) for indicator in self.bias_patterns['gender']['female_indicators'])
        
        if male_count > 0 or female_count > 0:
            total_gender_mentions = male_count + female_count
            gender_imbalance = abs(male_count - female_count) / total_gender_mentions
            if gender_imbalance > 0.7:  # More than 70% imbalance
                bias_types.append("gender")
                bias_score += gender_imbalance
        
        # Age bias detection
        young_count = sum(text_lower.count(indicator) for indicator in self.bias_patterns['age']['young_indicators'])
        experienced_count = sum(text_lower.count(indicator) for indicator in self.bias_patterns['age']['experienced_indicators'])
        
        if young_count > 0 or experienced_count > 0:
            total_age_mentions = young_count + experienced_count
            age_imbalance = abs(young_count - experienced_count) / total_age_mentions
            if age_imbalance > 0.7:
                bias_types.append("age")
                bias_score += age_imbalance
        
        # Education bias detection
        elite_count = sum(text_lower.count(school) for school in self.bias_patterns['education']['elite_schools'])
        if elite_count > 2:  # Multiple mentions of elite schools
            bias_types.append("education")
            bias_score += min(elite_count / 5, 1.0)  # Normalize to 0-1
        
        bias_detected = len(bias_types) > 0
        bias_score = min(bias_score, 1.0)  # Cap at 1.0
        
        return {
            "bias_detected": bias_detected,
            "bias_score": bias_score,
            "bias_types": bias_types,
            "details": {
                "gender_mentions": {"male": male_count, "female": female_count},
                "age_mentions": {"young": young_count, "experienced": experienced_count},
                "elite_schools": elite_count
            }
        }
    
    def calculate_experience_match(self, resume_experience: List[Dict], job_requirements: List[str]) -> float:
        """
        Calculate experience match based on job requirements and resume experience
        """
        if not resume_experience or not job_requirements:
            return 0.0
        
        # Extract experience years from requirements
        experience_years = 0
        for req in job_requirements:
            years_match = re.search(r'(\d+)\+?\s*years?', req.lower())
            if years_match:
                experience_years = max(experience_years, int(years_match.group(1)))
        
        if experience_years == 0:
            return 0.5  # Default match if no specific years mentioned
        
        # Calculate total experience from resume
        total_resume_years = 0
        for exp in resume_experience:
            if 'duration' in exp:
                duration = exp['duration']
                years_match = re.search(r'(\d+)', duration)
                if years_match:
                    total_resume_years += int(years_match.group(1))
        
        # Calculate match ratio
        if total_resume_years >= experience_years:
            return 1.0
        elif total_resume_years > 0:
            return total_resume_years / experience_years
        else:
            return 0.0
    
    def calculate_advanced_match_score(self, 
                                     resume_vector: np.ndarray, 
                                     job_vector: np.ndarray,
                                     resume_skills: List[str], 
                                     job_skills: List[str],
                                     resume_experience: List[Dict],
                                     job_requirements: List[str],
                                     resume_text: str = "",
                                     job_text: str = "") -> Dict[str, Any]:
        """
        Calculate advanced match score with multiple factors
        """
        # Vector similarity
        vector_similarity = cosine_similarity([resume_vector], [job_vector])[0][0]
        
        # Semantic skills matching
        skills_match = self.semantic_skill_matching(resume_skills, job_skills)
        
        # Experience matching
        experience_match = self.calculate_experience_match(resume_experience, job_requirements)
        
        # Bias detection
        resume_bias = self.detect_bias(resume_text)
        job_bias = self.detect_bias(job_text)
        
        # Calculate weighted score
        weighted_score = (
            self.vector_weight * vector_similarity +
            self.skills_weight * skills_match["skills_match_ratio"] +
            self.experience_weight * experience_match
        )
        
        # Apply bias penalty
        total_bias_score = (resume_bias["bias_score"] + job_bias["bias_score"]) / 2
        bias_penalty = total_bias_score * 0.1  # 10% penalty for bias
        final_score = max(0, weighted_score - bias_penalty)
        
        return {
            "score": final_score,
            "details": {
                "vector_similarity": float(vector_similarity),
                "skills_match_ratio": skills_match["skills_match_ratio"],
                "experience_match": experience_match,
                "matching_skills": skills_match["matching_skills"],
                "missing_skills": skills_match["missing_skills"],
                "semantic_matches": skills_match["semantic_matches"],
                "bias_detection": {
                    "resume_bias": resume_bias,
                    "job_bias": job_bias,
                    "total_bias_score": total_bias_score,
                    "bias_penalty": bias_penalty
                }
            }
        }
    
    def rank_resumes_advanced(self, job: Dict[str, Any], resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank resumes using advanced matching algorithm
        """
        match_results = []
        
        for resume in resumes:
            match_data = self.calculate_advanced_match_score(
                resume.get("vector", []),
                job.get("vector", []),
                resume.get("skills", []),
                job.get("skills_required", []),
                resume.get("experience", []),
                job.get("requirements", []),
                resume.get("raw_text", ""),
                f"{job.get('title', '')} {job.get('description', '')}"
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