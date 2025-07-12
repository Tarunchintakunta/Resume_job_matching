import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Ensure NLTK resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess_text(self, text):
        """
        Preprocess text by lowercasing, removing special characters,
        tokenizing, removing stopwords, and lemmatizing
        """
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        tokens = [t for t in tokens if t not in self.stop_words]
        
        # Lemmatization
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        
        return ' '.join(tokens)
    
    def extract_skills(self, text, skills_database):
        """
        Extract skills from text based on a skills database
        """
        # Convert skills database to lowercase for matching
        skills_db_lower = [skill.lower() for skill in skills_database]
        
        # Create a pattern for skills matching
        skills_pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills_db_lower) + r')\b'
        
        # Find all matches
        found_skills = re.findall(skills_pattern, text.lower())
        
        # Return unique skills
        return list(set(found_skills))
    
    def extract_entities(self, text):
        """
        Extract named entities using spaCy
        """
        doc = nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        return entities