import os
import requests
import zipfile
import json
import pandas as pd
from typing import List, Dict, Any

def download_kaggle_dataset(dataset_url: str, filename: str, target_dir: str = "data"):
    """Download dataset from Kaggle (simulated - you'll need Kaggle API)"""
    print(f"Downloading {filename} from Kaggle...")
    
    # Create target directory
    os.makedirs(target_dir, exist_ok=True)
    
    # For now, we'll create sample data that mimics the Kaggle datasets
    # In production, you would use: kaggle datasets download -d gauravduttakiit/resume-dataset
    if "resume-dataset" in dataset_url:
        create_sample_resume_dataset(f"{target_dir}/{filename}")
    elif "jobposts" in dataset_url:
        create_sample_job_dataset(f"{target_dir}/{filename}")
    elif "linkedin-skills" in dataset_url:
        create_sample_skills_dataset(f"{target_dir}/{filename}")
    
    print(f"Created sample {filename} in {target_dir}/")

def create_sample_resume_dataset(filename: str):
    """Create sample resume dataset mimicking Kaggle structure"""
    sample_resumes = []
    
    # Sample resume data structure based on Kaggle format
    resume_templates = [
        {
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "+1-555-0123",
            "summary": "Experienced software engineer with 5+ years in full-stack development",
            "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB", "AWS"],
            "education": [
                {
                    "institution": "Stanford University",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "graduation_year": 2018
                }
            ],
            "experience": [
                {
                    "company": "Google",
                    "title": "Senior Software Engineer",
                    "duration": "2020-2023",
                    "description": "Led development of scalable web applications"
                }
            ]
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "+1-555-0456",
            "summary": "Data scientist specializing in machine learning and analytics",
            "skills": ["Python", "TensorFlow", "PyTorch", "SQL", "Pandas", "Scikit-learn"],
            "education": [
                {
                    "institution": "MIT",
                    "degree": "Master of Science",
                    "field": "Data Science",
                    "graduation_year": 2019
                }
            ],
            "experience": [
                {
                    "company": "Netflix",
                    "title": "Data Scientist",
                    "duration": "2019-2023",
                    "description": "Developed recommendation algorithms"
                }
            ]
        }
    ]
    
    # Generate 100 sample resumes
    for i in range(100):
        template = resume_templates[i % len(resume_templates)]
        resume = {
            "id": f"resume_{i+1}",
            "name": f"{template['name']} {i+1}",
            "email": template['email'].replace("@", f"{i+1}@"),
            "phone": template['phone'],
            "summary": template['summary'],
            "skills": template['skills'],
            "education": template['education'],
            "experience": template['experience'],
            "raw_text": f"{template['summary']} Skills: {', '.join(template['skills'])}"
        }
        sample_resumes.append(resume)
    
    with open(filename, 'w') as f:
        json.dump(sample_resumes, f, indent=2)

def create_sample_job_dataset(filename: str):
    """Create sample job dataset mimicking Kaggle structure"""
    sample_jobs = []
    
    job_templates = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "description": "We are looking for a talented software engineer to join our team",
            "requirements": ["5+ years experience", "Python", "JavaScript", "React"],
            "qualifications": ["Bachelor's degree", "Strong problem-solving skills"],
            "skills_required": ["Python", "JavaScript", "React", "Node.js"],
            "location": "San Francisco, CA",
            "salary_range": "$120K - $180K",
            "job_type": "Full-time"
        },
        {
            "title": "Data Scientist",
            "company": "DataTech",
            "description": "Join our data science team to build ML models",
            "requirements": ["3+ years experience", "Python", "Machine Learning"],
            "qualifications": ["Master's degree", "Experience with ML frameworks"],
            "skills_required": ["Python", "TensorFlow", "PyTorch", "SQL"],
            "location": "New York, NY",
            "salary_range": "$100K - $150K",
            "job_type": "Full-time"
        }
    ]
    
    # Generate 50 sample jobs
    for i in range(50):
        template = job_templates[i % len(job_templates)]
        job = {
            "id": f"job_{i+1}",
            "title": template['title'],
            "company": f"{template['company']} {i+1}",
            "description": template['description'],
            "requirements": template['requirements'],
            "qualifications": template['qualifications'],
            "skills_required": template['skills_required'],
            "location": template['location'],
            "salary_range": template['salary_range'],
            "job_type": template['job_type']
        }
        sample_jobs.append(job)
    
    with open(filename, 'w') as f:
        json.dump(sample_jobs, f, indent=2)

def create_sample_skills_dataset(filename: str):
    """Create sample LinkedIn skills database"""
    skills = [
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript",
        "PHP", "Ruby", "Scala", "R", "MATLAB", "Perl", "Shell", "Bash", "PowerShell",
        
        # Web Technologies
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "Spring Boot", "ASP.NET", "Laravel", "Ruby on Rails", "GraphQL", "REST API",
        
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite", "Cassandra",
        "DynamoDB", "Elasticsearch", "Neo4j", "InfluxDB",
        
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins", "GitLab CI",
        "GitHub Actions", "Ansible", "Chef", "Puppet", "Vagrant", "VMware",
        
        # Machine Learning & AI
        "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch",
        "Scikit-learn", "Keras", "OpenCV", "NLP", "Computer Vision", "Natural Language Processing",
        "Data Mining", "Predictive Analytics", "Statistical Analysis",
        
        # Data Science
        "Data Analysis", "Data Visualization", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Plotly", "Tableau", "Power BI", "Jupyter", "Apache Spark", "Hadoop", "Kafka",
        
        # Mobile Development
        "iOS Development", "Android Development", "React Native", "Flutter", "Xamarin",
        "Mobile App Development", "App Store", "Google Play",
        
        # Cybersecurity
        "Cybersecurity", "Network Security", "Information Security", "Penetration Testing",
        "Ethical Hacking", "Cryptography", "Security Auditing", "Incident Response",
        
        # Project Management
        "Agile", "Scrum", "Kanban", "Project Management", "JIRA", "Confluence", "Trello",
        "Asana", "Microsoft Project", "Waterfall", "Lean", "Six Sigma",
        
        # Soft Skills
        "Leadership", "Communication", "Teamwork", "Problem Solving", "Critical Thinking",
        "Time Management", "Customer Service", "Sales", "Marketing", "Public Speaking"
    ]
    
    with open(filename, 'w') as f:
        json.dump(skills, f, indent=2)

def main():
    """Download and prepare all Kaggle datasets"""
    print("Downloading Kaggle datasets...")
    
    # Download resume dataset
    download_kaggle_dataset(
        "https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset",
        "kaggle_resumes.json"
    )
    
    # Download job posting dataset
    download_kaggle_dataset(
        "https://www.kaggle.com/datasets/madhab/jobposts",
        "kaggle_jobs.json"
    )
    
    # Download LinkedIn skills database
    download_kaggle_dataset(
        "https://www.kaggle.com/datasets/jruvika/linkedin-skills-database",
        "linkedin_skills.json"
    )
    
    print("All datasets downloaded and prepared!")

if __name__ == "__main__":
    main() 