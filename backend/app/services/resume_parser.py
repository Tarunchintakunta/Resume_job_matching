import io
import json
import re
from typing import Dict, Any, List, Optional
import PyPDF2
from app.services.text_processor import TextProcessor

class ResumeParser:
    def __init__(self, skills_database: List[str]):
        self.text_processor = TextProcessor()
        self.skills_database = skills_database
    
    def parse_pdf(self, content: bytes) -> Dict[str, Any]:
        """Parse resume from PDF file"""
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(content))
        text = ""
        
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
        
        return self._process_text(text)
    
    def parse_json(self, content: bytes) -> Dict[str, Any]:
        """Parse resume from JSON file"""
        resume_data = json.loads(content)
        
        # Extract raw text for processing
        raw_text = ""
        if "summary" in resume_data:
            raw_text += resume_data["summary"] + " "
        
        if "experience" in resume_data:
            for exp in resume_data["experience"]:
                if "description" in exp:
                    raw_text += exp["description"] + " "
        
        # Process skills
        if "skills" not in resume_data or not resume_data["skills"]:
            skills = self.text_processor.extract_skills(raw_text, self.skills_database)
            resume_data["skills"] = skills
        
        resume_data["raw_text"] = raw_text
        return resume_data
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Process extracted text to get structured resume data"""
        # Basic info extraction using regex
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phone_match = re.search(r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', text)
        
        # Extract entities
        entities = self.text_processor.extract_entities(text)
        
        # Extract skills
        skills = self.text_processor.extract_skills(text, self.skills_database)
        
        # Create structured resume data
        resume_data = {
            "raw_text": text,
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "skills": skills,
            "entities": entities
        }
        
        return resume_data