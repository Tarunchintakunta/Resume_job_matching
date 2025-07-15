import io
import json
import re
from typing import Dict, Any, List, Optional
from PyPDF2 import PdfReader  # Updated from PdfFileReader to PdfReader
from app.services.text_processor import TextProcessor
import pdfplumber
import docx
import re
import spacy

nlp = spacy.load('en_core_web_sm')

class ResumeParser:
    def __init__(self, skills_database: List[str]):
        self.text_processor = TextProcessor()
        self.skills_database = skills_database
    
    def parse_pdf(self, content: bytes) -> Dict[str, Any]:
        """Parse resume from PDF file"""
        try:
            pdf_reader = PdfReader(io.BytesIO(content))  # Updated from PdfFileReader to PdfReader
            text = ""
            
            for page in pdf_reader.pages:  # Updated from getPage(page_num).extractText()
                text += page.extract_text()  # Updated method name
            
            return self._process_text(text)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def parse_json(self, content: bytes) -> Dict[str, Any]:
        """Parse resume from JSON file"""
        try:
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
            
            # Ensure required fields are present
            if "name" not in resume_data or not resume_data["name"]:
                resume_data["name"] = "Unknown"
                
            if "education" not in resume_data or not resume_data["education"]:
                resume_data["education"] = []
                
            if "experience" not in resume_data or not resume_data["experience"]:
                resume_data["experience"] = []
            
            # Ensure required fields for education entries
            for edu in resume_data.get("education", []):
                if "institution" not in edu or not edu["institution"]:
                    edu["institution"] = "Unknown Institution"
                if "degree" not in edu or not edu["degree"]:
                    edu["degree"] = "Unknown Degree"
            
            # Ensure required fields for experience entries
            for exp in resume_data.get("experience", []):
                if "company" not in exp or not exp["company"]:
                    exp["company"] = "Unknown Company"
                if "title" not in exp or not exp["title"]:
                    exp["title"] = "Unknown Title"
            
            return resume_data
        except Exception as e:
            raise Exception(f"Error parsing JSON: {str(e)}")
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Process extracted text to get structured resume data"""
        # Basic info extraction using regex
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phone_match = re.search(r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', text)
        
        # Try to extract name (improved pattern to better extract names from resumes)
        # First try to find a name at the beginning of the document (often in capitals)
        name_match = re.search(r'^([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+)', text.strip())
        
        # If that fails, try to find a name with a common format anywhere in the first few lines
        if not name_match:
            first_lines = '\n'.join(text.split('\n')[:5])
            name_match = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+)', first_lines)
        
        # If we found a PDF file name, use that as a fallback
        file_name = getattr(self, 'current_file_name', None)
        extracted_name = name_match.group(0) if name_match else None
        
        if file_name and not extracted_name:
            # Try to extract a name from the file name
            file_name = file_name.replace('_', ' ').replace('-', ' ')
            name_parts = file_name.split()
            if len(name_parts) >= 2:
                extracted_name = ' '.join(name_parts[:2])
        
        # Extract entities
        entities = self.text_processor.extract_entities(text)
        
        # Extract skills
        skills = self.text_processor.extract_skills(text, self.skills_database)
        
        # Create structured resume data
        resume_data = {
            "raw_text": text,
            "name": extracted_name or "Unknown",
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "skills": skills,
            "entities": entities,
            "summary": ""  # Add default summary
        }
            
        # Try to extract education and experience sections
        sections = self._extract_sections(text)
        if "education" in sections:
            resume_data["education"] = self._parse_education(sections["education"])
        else:
            resume_data["education"] = []
            
        if "experience" in sections:
            resume_data["experience"] = self._parse_experience(sections["experience"])
        else:
            resume_data["experience"] = []
        
        # Ensure required fields for education entries
        for edu in resume_data.get("education", []):
            if "institution" not in edu or not edu["institution"]:
                edu["institution"] = "Unknown Institution"
            if "degree" not in edu or not edu["degree"]:
                edu["degree"] = "Unknown Degree"
            
            # Convert any None values to empty strings to avoid validation errors
            for key in edu:
                if edu[key] is None:
                    edu[key] = ""
        
        # Ensure required fields for experience entries
        for exp in resume_data.get("experience", []):
            if "company" not in exp or not exp["company"]:
                exp["company"] = "Unknown Company"
            if "title" not in exp or not exp["title"]:
                exp["title"] = "Unknown Title"
                
            # Convert any None values to empty strings to avoid validation errors
            for key in exp:
                if exp[key] is None:
                    exp[key] = ""
        
        # Add a default summary if none exists
        if "summary" not in resume_data or not resume_data["summary"]:
            resume_data["summary"] = "No summary provided."
        
        return resume_data
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the resume text"""
        # Common section headers in resumes
        section_headers = [
            "education", "experience", "work experience", "employment", 
            "skills", "technical skills", "projects", "certifications",
            "achievements", "publications", "languages", "interests"
        ]
        
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            is_header = False
            for header in section_headers:
                if re.search(r'\b' + header + r'\b', line.lower()):
                    # If we've been collecting content for a section, save it
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    # Start new section
                    current_section = header.lower()
                    section_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                section_content.append(line)
        
        # Save the last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _parse_education(self, education_text: str) -> List[Dict[str, Any]]:
        """Parse education section to structured format"""
        education_entries = []
        # Simple parsing - split by line breaks and look for degree information
        lines = education_text.split('\n')
        
        current_entry = {"institution": "Unknown Institution", "degree": "Unknown Degree"}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for institution
            if re.search(r'university|college|institute|school', line.lower()):
                if current_entry and 'institution' in current_entry:
                    # Only add the entry if it has both required fields
                    if current_entry["institution"] != "Unknown Institution" or current_entry["degree"] != "Unknown Degree":
                        education_entries.append(current_entry)
                    current_entry = {"institution": "Unknown Institution", "degree": "Unknown Degree"}
                
                current_entry['institution'] = line
            
            # Look for degree
            elif re.search(r'bachelor|master|phd|b\.?s|m\.?s|b\.?tech|m\.?tech', line.lower()):
                current_entry['degree'] = line
            
            # Look for date ranges
            elif re.search(r'\d{4}\s*-\s*\d{4}|\d{4}\s*to\s*\d{4}|present', line.lower()):
                match = re.search(r'(\d{4})\s*-\s*(\d{4}|\w+)', line)
                if match:
                    current_entry['start_date'] = match.group(1)
                    current_entry['end_date'] = match.group(2)
            
            # Look for GPA
            elif re.search(r'gpa|grade', line.lower()):
                match = re.search(r'(\d\.\d+)', line)
                if match:
                    current_entry['gpa'] = float(match.group(1))
        
        # Add the last entry if it exists
        if current_entry and 'institution' in current_entry:
            # Only add the entry if it has more than just the default values
            if current_entry["institution"] != "Unknown Institution" or current_entry["degree"] != "Unknown Degree":
                education_entries.append(current_entry)
        
        # If no entries were found, add a default one
        if not education_entries:
            education_entries.append({
                "institution": "Unknown Institution",
                "degree": "Unknown Degree",
                "field_of_study": "",
                "start_date": "",
                "end_date": ""
            })
        
        return education_entries
    
    def _parse_experience(self, experience_text: str) -> List[Dict[str, Any]]:
        """Parse experience section to structured format"""
        experience_entries = []
        # Split by lines to process
        lines = experience_text.split('\n')
        
        current_entry = {"company": "Unknown Company", "title": "Unknown Title"}
        description_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for company name (often has Inc, LLC, etc. or is all caps)
            if re.search(r'\b(Inc|LLC|Ltd|Corp|Corporation)\b', line) or line.isupper():
                if current_entry and 'company' in current_entry:
                    if description_lines:
                        current_entry['description'] = ' '.join(description_lines)
                    # Only add the entry if it has more than just the default values
                    if current_entry["company"] != "Unknown Company" or current_entry["title"] != "Unknown Title":
                        experience_entries.append(current_entry)
                    current_entry = {"company": "Unknown Company", "title": "Unknown Title"}
                    description_lines = []
                
                current_entry['company'] = line
            
            # Look for job title (often starts with common titles)
            elif re.search(r'\b(Software|Developer|Engineer|Manager|Director|Analyst|Consultant|Designer)\b', line):
                if 'title' not in current_entry or current_entry["title"] == "Unknown Title":
                    current_entry['title'] = line
                else:
                    description_lines.append(line)
            
            # Look for date ranges
            elif re.search(r'\d{4}\s*-\s*\d{4}|\d{4}\s*to\s*\d{4}|present', line.lower()):
                match = re.search(r'(\d{4})\s*-\s*(\d{4}|\w+)', line)
                if match:
                    current_entry['start_date'] = match.group(1)
                    current_entry['end_date'] = match.group(2)
            
            # Everything else is probably description
            else:
                description_lines.append(line)
        
        # Add the last entry if it exists
        if current_entry and 'company' in current_entry:
            if description_lines:
                current_entry['description'] = ' '.join(description_lines)
            # Only add the entry if it has more than just the default values
            if current_entry["company"] != "Unknown Company" or current_entry["title"] != "Unknown Title":
                experience_entries.append(current_entry)
        
        # If no entries were found, add a default one
        if not experience_entries:
            experience_entries.append({
                "company": "Unknown Company",
                "title": "Unknown Title",
                "description": "",
                "start_date": "",
                "end_date": "",
                "location": ""
            })
        
        return experience_entries