import os
import json
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO

def download_dataset(url, save_path):
    """Download a dataset from URL"""
    print(f"Downloading dataset from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        f.write(response.content)
    
    print(f"Dataset saved to {save_path}")

def process_resume_dataset():
    """Process the resume dataset"""
    print("Processing resume dataset...")
    
    # Define paths
    zip_path = "data/resume_dataset.zip"
    extract_path = "data"
    output_path = "data/processed_resumes.json"
    
    # Download dataset if not exists
    if not os.path.exists(zip_path):
        download_dataset(
            "https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset/download",
            zip_path
        )
    
    # Extract zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Process the dataset
    resumes = []
    resume_dir = os.path.join(extract_path, "data")
    
    for file in os.listdir(resume_dir):
        if file.endswith(".json"):
            with open(os.path.join(resume_dir, file), 'r') as f:
                resume_data = json.load(f)
                resumes.append(resume_data)
    
    # Save processed data
    with open(output_path, 'w') as f:
        json.dump(resumes, f)
    
    print(f"Processed {len(resumes)} resumes and saved to {output_path}")
    return resumes

def process_job_dataset():
    """Process the job dataset"""
    print("Processing job dataset...")
    
    # Define paths
    zip_path = "data/job_dataset.zip"
    extract_path = "data"
    output_path = "data/processed_jobs.json"
    
    # Download dataset if not exists
    if not os.path.exists(zip_path):
        download_dataset(
            "https://www.kaggle.com/datasets/madhab/jobposts/download",
            zip_path
        )
    
    # Extract zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Process the dataset
    jobs_df = pd.read_csv(os.path.join(extract_path, "job_posts.csv"))
    
    # Clean and transform data
    jobs = []
    for _, row in jobs_df.iterrows():
        job = {
            "title": row.get("title", ""),
            "company": row.get("company", ""),
            "description": row.get("description", ""),
            "requirements": row.get("requirements", "").split("\n") if pd.notna(row.get("requirements")) else [],
            "qualifications": [],
            "skills_required": [],
            "location": row.get("location", ""),
            "job_type": row.get("job_type", "")
        }
        jobs.append(job)
    
    # Save processed data
    with open(output_path, 'w') as f:
        json.dump(jobs, f)
    
    print(f"Processed {len(jobs)} jobs and saved to {output_path}")
    return jobs

def process_skills_database():
    """Process the skills database"""
    print("Processing skills database...")
    
    # Define paths
    zip_path = "data/skills_database.zip"
    extract_path = "data"
    output_path = "data/skills_database.json"
    
    # Download dataset if not exists
    if not os.path.exists(zip_path):
        download_dataset(
            "https://www.kaggle.com/datasets/jruvika/linkedin-skills-database/download",
            zip_path
        )
    
    # Extract zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Process the dataset
    skills_df = pd.read_csv(os.path.join(extract_path, "linkedin_skills.csv"))
    skills_list = skills_df["skill"].tolist()
    
    # Save processed data
    with open(output_path, 'w') as f:
        json.dump(skills_list, f)
    
    print(f"Processed {len(skills_list)} skills and saved to {output_path}")
    return skills_list

def main():
    """Main function to prepare all datasets"""
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    # Process datasets
    resumes = process_resume_dataset()
    jobs = process_job_dataset()
    skills = process_skills_database()
    
    print("Data preparation completed!")

if __name__ == "__main__":
    main()