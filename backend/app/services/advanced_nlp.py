import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import re
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
import joblib
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except:
    pass

class AdvancedNLPProcessor:
    def __init__(self, use_bert: bool = True, use_word2vec: bool = True):
        self.use_bert = use_bert
        self.use_word2vec = use_word2vec
        
        # Load spaCy model for advanced NLP
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Initialize NLTK components
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Initialize vectorizers
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        # Load or initialize Word2Vec model
        self.word2vec_model = None
        if self.use_word2vec:
            self._initialize_word2vec()
        
        # Load or initialize BERT model
        self.bert_model = None
        self.bert_tokenizer = None
        if self.use_bert:
            self._initialize_bert()
        
        # Entity patterns for advanced recognition
        self.entity_patterns = {
            'skills': [
                r'\b(?:Python|JavaScript|Java|C\+\+|C#|Go|Rust|Swift|Kotlin|TypeScript|PHP|Ruby|Scala|R|MATLAB)\b',
                r'\b(?:React|Angular|Vue\.js|Node\.js|Express\.js|Django|Flask|Spring Boot|ASP\.NET|Laravel)\b',
                r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Oracle|SQLite|Cassandra|DynamoDB)\b',
                r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Terraform|Jenkins|GitLab CI|GitHub Actions)\b',
                r'\b(?:Machine Learning|Deep Learning|Neural Networks|TensorFlow|PyTorch|Scikit-learn|NLP)\b'
            ],
            'education': [
                r'\b(?:Bachelor|Master|PhD|Associate|Diploma|Certificate)\b',
                r'\b(?:Computer Science|Information Technology|Data Science|Software Engineering)\b',
                r'\b(?:University|College|Institute|School)\b'
            ],
            'experience': [
                r'\b(?:years?|months?|experience|senior|junior|lead|manager|director)\b',
                r'\b(?:Software Engineer|Developer|Data Scientist|Product Manager|DevOps Engineer)\b'
            ],
            'companies': [
                r'\b(?:Google|Microsoft|Amazon|Facebook|Apple|IBM|Oracle|Twitter|LinkedIn|Uber|Airbnb|Netflix)\b'
            ]
        }
    
    def _initialize_word2vec(self):
        """Initialize Word2Vec model (simulated for now)"""
        try:
            # In a real implementation, you would load a pre-trained Word2Vec model
            # from gensim.models import Word2Vec
            # self.word2vec_model = Word2Vec.load('path/to/word2vec.model')
            
            # For now, create a simple word embedding simulation
            self.word2vec_model = {
                'vector_size': 100,
                'vocab': set(['python', 'javascript', 'react', 'node', 'mongodb', 'aws', 'docker', 
                             'java', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'typescript', 
                             'php', 'ruby', 'scala', 'r', 'matlab', 'sql', 'mysql', 'postgresql', 
                             'redis', 'oracle', 'sqlite', 'cassandra', 'dynamodb', 'elasticsearch', 
                             'neo4j', 'influxdb', 'couchdb', 'mariadb', 'azure', 'gcp', 'kubernetes', 
                             'terraform', 'jenkins', 'gitlab', 'github', 'ansible', 'chef', 'puppet', 
                             'vagrant', 'vmware', 'openstack', 'machine', 'learning', 'deep', 'neural', 
                             'networks', 'tensorflow', 'pytorch', 'scikit', 'nlp', 'computer', 'vision', 
                             'data', 'mining', 'predictive', 'analytics', 'statistical', 'reinforcement', 
                             'ios', 'android', 'react', 'native', 'flutter', 'xamarin', 'mobile', 'app', 
                             'cybersecurity', 'network', 'security', 'information', 'penetration', 'testing', 
                             'ethical', 'hacking', 'cryptography', 'security', 'auditing', 'incident', 'response', 
                             'siem', 'agile', 'scrum', 'kanban', 'project', 'management', 'jira', 'confluence', 
                             'trello', 'asana', 'microsoft', 'waterfall', 'lean', 'six', 'sigma', 'pmi', 
                             'leadership', 'communication', 'teamwork', 'problem', 'solving', 'critical', 
                             'thinking', 'time', 'management', 'customer', 'service', 'sales', 'marketing', 
                             'public', 'speaking', 'negotiation'])
            }
            print("Word2Vec model initialized (simulated)")
        except Exception as e:
            print(f"Warning: Could not initialize Word2Vec model: {e}")
            self.word2vec_model = None
    
    def _initialize_bert(self):
        """Initialize BERT model (simulated for now)"""
        try:
            # In a real implementation, you would load a pre-trained BERT model
            # from transformers import BertModel, BertTokenizer
            # self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            # self.bert_model = BertModel.from_pretrained('bert-base-uncased')
            
            # For now, create a simple BERT simulation
            self.bert_model = {
                'model_name': 'bert-base-uncased',
                'max_length': 512,
                'vector_size': 768
            }
            self.bert_tokenizer = {
                'vocab_size': 30522,
                'max_length': 512
            }
            print("BERT model initialized (simulated)")
        except Exception as e:
            print(f"Warning: Could not initialize BERT model: {e}")
            self.bert_model = None
            self.bert_tokenizer = None
    
    def get_bert_embeddings(self, text: str) -> np.ndarray:
        """Get BERT embeddings for text"""
        if not self.bert_model:
            # Fallback to TF-IDF if BERT is not available
            return self.get_tfidf_embeddings(text)
        
        try:
            # Simulate BERT embeddings
            # In real implementation:
            # inputs = self.bert_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            # with torch.no_grad():
            #     outputs = self.bert_model(**inputs)
            # embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
            
            # For now, create a simulated BERT embedding
            words = text.lower().split()
            embedding = np.zeros(self.bert_model['vector_size'])
            
            for word in words[:50]:  # Limit to first 50 words
                # Simple hash-based embedding simulation
                word_hash = hash(word) % self.bert_model['vector_size']
                embedding[word_hash] = 1.0
            
            return embedding / (np.linalg.norm(embedding) + 1e-8)
        
        except Exception as e:
            print(f"Error getting BERT embeddings: {e}")
            return self.get_tfidf_embeddings(text)
    
    def get_word2vec_embeddings(self, text: str) -> np.ndarray:
        """Get Word2Vec embeddings for text"""
        if not self.word2vec_model:
            return self.get_tfidf_embeddings(text)
        
        try:
            words = text.lower().split()
            word_vectors = []
            
            for word in words:
                if word in self.word2vec_model['vocab']:
                    # Simulate Word2Vec vector
                    word_vector = np.random.randn(self.word2vec_model['vector_size'])
                    word_vector = word_vector / np.linalg.norm(word_vector)
                    word_vectors.append(word_vector)
            
            if word_vectors:
                return np.mean(word_vectors, axis=0)
            else:
                return np.zeros(self.word2vec_model['vector_size'])
        
        except Exception as e:
            print(f"Error getting Word2Vec embeddings: {e}")
            return self.get_tfidf_embeddings(text)
    
    def get_tfidf_embeddings(self, text: str) -> np.ndarray:
        """Get TF-IDF embeddings for text"""
        try:
            # Fit and transform the text
            embedding = self.tfidf_vectorizer.fit_transform([text])
            return embedding.toarray()[0]
        except Exception as e:
            print(f"Error getting TF-IDF embeddings: {e}")
            return np.zeros(1000)  # Default size
    
    def get_hybrid_embeddings(self, text: str) -> Dict[str, np.ndarray]:
        """Get multiple types of embeddings for comprehensive analysis"""
        embeddings = {
            'tfidf': self.get_tfidf_embeddings(text)
        }
        
        if self.use_bert:
            embeddings['bert'] = self.get_bert_embeddings(text)
        
        if self.use_word2vec:
            embeddings['word2vec'] = self.get_word2vec_embeddings(text)
        
        return embeddings
    
    def advanced_entity_recognition(self, text: str) -> Dict[str, List[str]]:
        """Advanced entity recognition using multiple methods"""
        entities = {
            'skills': [],
            'education': [],
            'experience': [],
            'companies': [],
            'locations': [],
            'dates': [],
            'emails': [],
            'phones': []
        }
        
        # Pattern-based extraction
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities[entity_type].extend(matches)
        
        # spaCy-based extraction
        if self.nlp:
            doc = self.nlp(text)
            
            # Named entities
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['companies'].append(ent.text)
                elif ent.label_ == 'GPE':
                    entities['locations'].append(ent.text)
                elif ent.label_ == 'DATE':
                    entities['dates'].append(ent.text)
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = re.findall(email_pattern, text)
        
        # Phone extraction
        phone_pattern = r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
        entities['phones'] = re.findall(phone_pattern, text)
        
        # Remove duplicates and clean
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Perform sentiment analysis on text"""
        try:
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity
            
            # Categorize sentiment
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Analyze sentiment by sentences
            sentences = sent_tokenize(text)
            sentence_sentiments = []
            
            for sentence in sentences[:10]:  # Limit to first 10 sentences
                sentence_blob = TextBlob(sentence)
                sentence_sentiments.append({
                    'sentence': sentence,
                    'polarity': sentence_blob.sentiment.polarity,
                    'subjectivity': sentence_blob.sentiment.subjectivity
                })
            
            return {
                'overall_sentiment': sentiment,
                'polarity_score': sentiment_score,
                'subjectivity_score': subjectivity_score,
                'sentence_sentiments': sentence_sentiments,
                'confidence': abs(sentiment_score)  # Higher absolute score = more confident
            }
        
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'overall_sentiment': 'neutral',
                'polarity_score': 0.0,
                'subjectivity_score': 0.0,
                'sentence_sentiments': [],
                'confidence': 0.0
            }
    
    def extract_key_phrases(self, text: str, num_phrases: int = 10) -> List[Dict[str, Any]]:
        """Extract key phrases from text using multiple methods"""
        try:
            # Tokenize and preprocess
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalnum() and token not in self.stop_words]
            
            # Get bigrams and trigrams
            bigrams = list(zip(tokens, tokens[1:]))
            trigrams = list(zip(tokens, tokens[1:], tokens[2:]))
            
            # Calculate phrase frequencies
            phrase_freq = {}
            
            # Single words
            for token in tokens:
                phrase_freq[token] = phrase_freq.get(token, 0) + 1
            
            # Bigrams
            for bigram in bigrams:
                phrase = ' '.join(bigram)
                phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1
            
            # Trigrams
            for trigram in trigrams:
                phrase = ' '.join(trigram)
                phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1
            
            # Sort by frequency and return top phrases
            sorted_phrases = sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)
            
            key_phrases = []
            for phrase, frequency in sorted_phrases[:num_phrases]:
                key_phrases.append({
                    'phrase': phrase,
                    'frequency': frequency,
                    'length': len(phrase.split()),
                    'type': 'word' if len(phrase.split()) == 1 else 'phrase'
                })
            
            return key_phrases
        
        except Exception as e:
            print(f"Error extracting key phrases: {e}")
            return []
    
    def analyze_text_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity and readability"""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalnum()]
            
            # Basic statistics
            num_sentences = len(sentences)
            num_words = len(words)
            num_characters = len(text)
            
            # Average sentence length
            avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
            
            # Average word length
            avg_word_length = sum(len(word) for word in words) / num_words if num_words > 0 else 0
            
            # Unique words ratio
            unique_words = set(words)
            lexical_diversity = len(unique_words) / num_words if num_words > 0 else 0
            
            # Flesch Reading Ease (simplified)
            # Formula: 206.835 - 1.015 × (total words ÷ total sentences) - 84.6 × (total syllables ÷ total words)
            syllables = sum(self._count_syllables(word) for word in words)
            flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * (syllables / num_words) if num_words > 0 else 0
            flesch_score = max(0, min(100, flesch_score))  # Clamp between 0 and 100
            
            # Readability level
            if flesch_score >= 90:
                readability_level = "Very Easy"
            elif flesch_score >= 80:
                readability_level = "Easy"
            elif flesch_score >= 70:
                readability_level = "Fairly Easy"
            elif flesch_score >= 60:
                readability_level = "Standard"
            elif flesch_score >= 50:
                readability_level = "Fairly Difficult"
            elif flesch_score >= 30:
                readability_level = "Difficult"
            else:
                readability_level = "Very Difficult"
            
            return {
                'statistics': {
                    'sentences': num_sentences,
                    'words': num_words,
                    'characters': num_characters,
                    'unique_words': len(unique_words)
                },
                'averages': {
                    'sentence_length': avg_sentence_length,
                    'word_length': avg_word_length
                },
                'complexity': {
                    'lexical_diversity': lexical_diversity,
                    'flesch_score': flesch_score,
                    'readability_level': readability_level
                }
            }
        
        except Exception as e:
            print(f"Error analyzing text complexity: {e}")
            return {
                'statistics': {'sentences': 0, 'words': 0, 'characters': 0, 'unique_words': 0},
                'averages': {'sentence_length': 0, 'word_length': 0},
                'complexity': {'lexical_diversity': 0, 'flesch_score': 0, 'readability_level': 'Unknown'}
            }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
        
        return count
    
    def comprehensive_text_analysis(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive text analysis"""
        return {
            'embeddings': self.get_hybrid_embeddings(text),
            'entities': self.advanced_entity_recognition(text),
            'sentiment': self.sentiment_analysis(text),
            'key_phrases': self.extract_key_phrases(text),
            'complexity': self.analyze_text_complexity(text)
        }
    
    def save_model(self, filepath: str):
        """Save the NLP model"""
        try:
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'word2vec_model': self.word2vec_model,
                'bert_model': self.bert_model,
                'entity_patterns': self.entity_patterns
            }
            joblib.dump(model_data, filepath)
            print(f"NLP model saved to {filepath}")
        except Exception as e:
            print(f"Error saving NLP model: {e}")
    
    def load_model(self, filepath: str):
        """Load the NLP model"""
        try:
            model_data = joblib.load(filepath)
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.word2vec_model = model_data['word2vec_model']
            self.bert_model = model_data['bert_model']
            self.entity_patterns = model_data['entity_patterns']
            print(f"NLP model loaded from {filepath}")
        except Exception as e:
            print(f"Error loading NLP model: {e}")

# Global NLP processor instance
nlp_processor = AdvancedNLPProcessor() 