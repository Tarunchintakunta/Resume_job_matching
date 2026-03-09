import os
import json
import random

def create_training_corpus():
    """Create a training corpus for the TF-IDF vectorizer without inserting fake data into DB"""
    print("Creating training corpus for model training...")

    # Common skills in tech industry
    skills = [
        "Python", "JavaScript", "React", "Node.js", "MongoDB", "SQL", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP", "Java",
        "C++", "C#", "Angular", "Vue.js", "FastAPI", "Django", "Flask", "Spring Boot",
        "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing",
        "HTML", "CSS", "TypeScript", "Redux", "Express.js", "REST API", "GraphQL",
        "PostgreSQL", "MySQL", "NoSQL", "Firebase", "Azure", "GCP", "Linux",
        "R", "Tableau", "Power BI", "Hadoop", "Spark", "Kafka", "ETL",
        "Mobile Development", "iOS", "Android", "Swift", "Kotlin", "React Native",
        "Cybersecurity", "Network Security", "Blockchain", "IoT"
    ]

    # Job titles
    job_titles = [
        "Software Engineer", "Data Scientist", "Full Stack Developer",
        "Frontend Developer", "Backend Developer", "DevOps Engineer",
        "Machine Learning Engineer", "Data Analyst", "Product Manager",
        "Cloud Architect", "Security Engineer", "Mobile Developer",
        "QA Engineer", "Systems Administrator", "Database Administrator"
    ]

    # Generate training documents (these are just for TF-IDF training, NOT inserted into DB)
    documents = []

    # Generate resume-like training documents
    for i in range(50):
        candidate_skills = random.sample(skills, random.randint(5, 15))
        title = random.choice(job_titles)
        doc = f"experienced {title} proficient in {' '.join(candidate_skills)} "
        doc += f"strong background in software development and problem solving "
        doc += f"skilled in {' '.join(random.sample(candidate_skills, min(3, len(candidate_skills))))} "
        documents.append(doc.lower())

    # Generate job-like training documents
    for i in range(30):
        required_skills = random.sample(skills, random.randint(5, 10))
        title = random.choice(job_titles)
        doc = f"{title} position requiring {' '.join(required_skills)} "
        doc += f"looking for candidates with experience in {' '.join(random.sample(required_skills, min(3, len(required_skills))))} "
        doc += f"must have strong technical skills and ability to work in a team "
        documents.append(doc.lower())

    # Save training corpus
    output_path = "data/training_corpus.json"
    with open(output_path, 'w') as f:
        json.dump(documents, f, indent=2)

    print(f"Created training corpus with {len(documents)} documents")
    return documents

def create_skills_database():
    """Create skills database for skill matching"""
    print("Creating skills database...")

    skills = [
        "Python", "JavaScript", "React", "Node.js", "MongoDB", "SQL", "AWS", "Docker",
        "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP", "Java",
        "C++", "C#", "Angular", "Vue.js", "FastAPI", "Django", "Flask", "Spring Boot",
        "Kubernetes", "Git", "CI/CD", "Agile", "Scrum", "DevOps", "Cloud Computing",
        "HTML", "CSS", "TypeScript", "Redux", "Express.js", "REST API", "GraphQL",
        "PostgreSQL", "MySQL", "Oracle", "NoSQL", "Firebase", "Heroku", "Netlify",
        "Azure", "GCP", "Linux", "Unix", "Bash", "PowerShell", "R", "Tableau",
        "Power BI", "Excel", "Hadoop", "Spark", "Kafka", "Airflow", "ETL",
        "Big Data", "Blockchain", "IoT", "Mobile Development", "iOS",
        "Android", "Swift", "Kotlin", "React Native", "Flutter", "Cybersecurity",
        "Network Security", "Penetration Testing", "Cryptography"
    ]

    output_path = "data/skills_database.json"
    with open(output_path, 'w') as f:
        json.dump(skills, f, indent=2)

    print(f"Created skills database with {len(skills)} skills")
    return skills

def main():
    """Prepare training data (no fake resumes/jobs are inserted into DB)"""
    os.makedirs("data", exist_ok=True)

    create_training_corpus()
    create_skills_database()

    print("\nData preparation completed! Training corpus ready for model training.")

if __name__ == "__main__":
    main()
