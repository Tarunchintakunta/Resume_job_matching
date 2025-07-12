import os
import json
import random
import pandas as pd
from datetime import datetime, timedelta

def create_synthetic_resumes(count=100):
    """Create synthetic resume data for development"""
    print(f"Creating {count} synthetic resumes...")
    
    # Sample data
    skills = [
        "Python", "JavaScript", "React", "Node.js", "MongoDB", "SQL", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP", "Java",
        "C++", "C#", "Angular", "Vue.js", "FastAPI", "Django", "Flask", "Spring Boot",
        "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing"
    ]
    
    education_degrees = ["Bachelor's", "Master's", "PhD", "Associate's"]
    education_fields = ["Computer Science", "Information Technology", "Data Science", 
                      "Software Engineering", "Electrical Engineering", "Mathematics"]
    
    companies = ["Google", "Microsoft", "Amazon", "Facebook", "Apple", "IBM", "Oracle",
                "Twitter", "LinkedIn", "Uber", "Airbnb", "Netflix", "Spotify"]
    
    job_titles = ["Software Engineer", "Data Scientist", "Full Stack Developer", 
                 "Frontend Developer", "Backend Developer", "DevOps Engineer",
                 "Machine Learning Engineer", "Data Analyst", "Product Manager"]
    
    # Generate resumes
    resumes = []
    for i in range(count):
        # Generate basic info
        name = f"Candidate {i+1}"
        email = f"candidate{i+1}@example.com"
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        # Generate skills (random subset)
        candidate_skills = random.sample(skills, random.randint(5, 15))
        
        # Generate education
        education = []
        for _ in range(random.randint(1, 3)):
            edu = {
                "institution": f"University {random.randint(1, 30)}",
                "degree": random.choice(education_degrees),
                "field_of_study": random.choice(education_fields),
                "start_date": (datetime.now() - timedelta(days=random.randint(365*2, 365*8))).isoformat(),
                "end_date": (datetime.now() - timedelta(days=random.randint(0, 365*2))).isoformat(),
                "gpa": round(random.uniform(3.0, 4.0), 2)
            }
            education.append(edu)
        
        # Generate experience
        experience = []
        for _ in range(random.randint(1, 4)):
            exp = {
                "company": random.choice(companies),
                "title": random.choice(job_titles),
                "description": f"Worked on various projects using {', '.join(random.sample(candidate_skills, min(3, len(candidate_skills))))}.",
                "start_date": (datetime.now() - timedelta(days=random.randint(365, 365*5))).isoformat(),
                "end_date": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
                "location": f"City {random.randint(1, 20)}"
            }
            experience.append(exp)
        
        # Generate summary
        summary = f"Experienced professional with skills in {', '.join(random.sample(candidate_skills, min(5, len(candidate_skills))))}."
        
        # Create resume object
        resume = {
            "name": name,
            "email": email,
            "phone": phone,
            "summary": summary,
            "skills": candidate_skills,
            "education": education,
            "experience": experience,
            "raw_text": summary + " " + " ".join([exp["description"] for exp in experience])
        }
        
        resumes.append(resume)
    
    # Save to file
    output_path = "data/processed_resumes.json"
    with open(output_path, 'w') as f:
        json.dump(resumes, f, indent=2)
    
    print(f"Created {len(resumes)} synthetic resumes and saved to {output_path}")
    return resumes

def create_synthetic_jobs(count=20):
    """Create synthetic job posting data for development"""
    print(f"Creating {count} synthetic job postings...")
    
    # Sample data
    skills = [
        "Python", "JavaScript", "React", "Node.js", "MongoDB", "SQL", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP", "Java",
        "C++", "C#", "Angular", "Vue.js", "FastAPI", "Django", "Flask", "Spring Boot",
        "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing"
    ]
    
    companies = ["TechCorp", "DataSystems", "WebFrontier", "CloudNine", "InnovateIT",
                "CodeMasters", "DigitalDynamics", "ByteWorks", "AlgorithmEx", "NexusTech"]
    
    job_titles = ["Software Engineer", "Data Scientist", "Full Stack Developer", 
                 "Frontend Developer", "Backend Developer", "DevOps Engineer",
                 "Machine Learning Engineer", "Data Analyst", "Product Manager"]
    
    locations = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
                "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Atlanta, GA"]
    
    job_types = ["Full-time", "Part-time", "Contract", "Remote"]
    
    # Generate job postings
    jobs = []
    for i in range(count):
        # Select job title and skills
        title = random.choice(job_titles)
        required_skills = random.sample(skills, random.randint(5, 10))
        
        # Generate description and requirements
        description = f"We are looking for a talented {title} to join our team."
        description += f" The ideal candidate will have experience with {', '.join(required_skills[:-1])} and {required_skills[-1]}."
        description += f" This role will involve developing and maintaining applications, collaborating with cross-functional teams, and staying up-to-date with industry trends."
        
        requirements = [
            f"Proficiency in {', '.join(required_skills[:3])}",
            f"{random.randint(2, 5)}+ years of experience in {title} role",
            "Bachelor's degree in Computer Science or related field",
            "Strong problem-solving skills and attention to detail",
            "Excellent communication and teamwork abilities"
        ]
        
        qualifications = [
            f"Experience with {', '.join(random.sample(list(set(skills) - set(required_skills)), 3))} is a plus",
            "Previous experience in Agile development environments",
            "Understanding of software design patterns and best practices"
        ]
        
        # Create job object
        job = {
            "title": title,
            "company": random.choice(companies),
            "description": description,
            "requirements": requirements,
            "qualifications": qualifications,
            "skills_required": required_skills,
            "experience_required": random.randint(1, 5),
            "location": random.choice(locations),
            "job_type": random.choice(job_types),
            "salary_range": f"${random.randint(70, 180)}K - ${random.randint(180, 250)}K"
        }
        
        jobs.append(job)
    
    # Save to file
    output_path = "data/processed_jobs.json"
    with open(output_path, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print(f"Created {len(jobs)} synthetic job postings and saved to {output_path}")
    return jobs

def create_skills_database():
    """Create skills database for development"""
    print("Creating skills database...")
    
    # Sample skills
    skills = [
        "Python", "JavaScript", "React", "Node.js", "MongoDB", "SQL", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP", "Java",
        "C++", "C#", "Angular", "Vue.js", "FastAPI", "Django", "Flask", "Spring Boot",
        "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing",
        "HTML", "CSS", "TypeScript", "Redux", "Express.js", "REST API", "GraphQL",
        "PostgreSQL", "MySQL", "Oracle", "NoSQL", "Firebase", "Heroku", "Netlify",
        "Azure", "GCP", "Linux", "Unix", "Bash", "PowerShell", "R", "Tableau",
        "Power BI", "Excel", "VBA", "Hadoop", "Spark", "Kafka", "Airflow", "ETL",
        "Big Data", "Blockchain", "IoT", "AR/VR", "Mobile Development", "iOS",
        "Android", "Swift", "Kotlin", "React Native", "Flutter", "Unity", "Cybersecurity",
        "Network Security", "Ethical Hacking", "Penetration Testing", "Cryptography"
    ]
    
    # Save to file
    output_path = "data/skills_database.json"
    with open(output_path, 'w') as f:
        json.dump(skills, f, indent=2)
    
    print(f"Created skills database with {len(skills)} skills and saved to {output_path}")
    return skills

def main():
    """Main function to prepare synthetic datasets"""
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    # Create synthetic datasets
    resumes = create_synthetic_resumes(100)
    jobs = create_synthetic_jobs(20)
    skills = create_skills_database()
    
    print("Data preparation completed!")

if __name__ == "__main__":
    main()