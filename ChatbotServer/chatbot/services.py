from django.conf import settings
from django.db.models import Q
from asgiref.sync import sync_to_async
from .models import KnowledgeBase, QueryLog, Category, Intent
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rapidfuzz import fuzz
import json
import os

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class UniversityDataService:
    def __init__(self):
        self.data_file = os.path.join(settings.BASE_DIR, 'chatbot', 'data', 'university_data.json')
        self.data = self._load_data()

    def _load_data(self):
        """Load university data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading university data: {e}")
            return {}

    def search_data(self, query):
        """Search all university data for relevant information."""
        query = query.lower()
        results = []
        
        try:
            print(f"Debug - Query: {query}")
            print(f"Debug - Data keys: {self.data.keys()}")
            
            # Search academic programs
            if 'academic_programs' in self.data:
                print(f"Debug - Found academic_programs")
                for level, programs in self.data['academic_programs'].items():
                    print(f"Debug - Checking level: {level}")
                    for program in programs:
                        # Check for exact program matches
                        program_name = program['name'].lower()
                        program_name_similarity = fuzz.token_set_ratio(query, program_name)
                        asks_about_requirements = 'requirement' in query or 'admission' in query
                        asks_about_specific = program_name in query or program['degree'].lower() in query
                        
                        print(f"Debug - Program: {program_name}")
                        print(f"Debug - Similarity: {program_name_similarity}")
                        print(f"Debug - Asks requirements: {asks_about_requirements}")
                        print(f"Debug - Asks specific: {asks_about_specific}")
                        
                        # Match if:
                        # 1. High similarity to program name
                        # 2. Contains program name or degree
                        # 3. Asking about requirements and mentions program keywords
                        if program_name_similarity > 60 or asks_about_specific or (asks_about_requirements and any(keyword in program_name for keyword in query.split())):
                            content = f"{program['name']} ({program['degree']}):\n{program['description']}\n"
                            
                            # Add requirements if specifically asked or if it's an admission query
                            if asks_about_requirements and 'requirements' in program:
                                content += "\nAdmission Requirements:\n- " + "\n- ".join(program['requirements'])
                            
                            # Add career prospects if available and not asking about requirements
                            if 'career_prospects' in program and not asks_about_requirements:
                                content += "\n\nCareer Prospects:\n- " + "\n- ".join(program['career_prospects'])
                            
                            score = 90 if asks_about_specific else program_name_similarity
                            print(f"Debug - Adding result with score: {score}")
                            
                            results.append({
                                'type': 'program',
                                'content': content,
                                'score': score
                            })

            # Search facilities
            if 'facilities' in self.data:
                facility_keywords = ['facility', 'facilities', 'campus', 'library', 'lab', 'hostel']
                if any(keyword in query for keyword in facility_keywords):
                    print(f"Debug - Found facilities")
                    content = "Campus Facilities:\n"
                    
                    # Handle libraries
                    if 'libraries' in self.data['facilities'] and ('library' in query or 'libraries' in query):
                        print(f"Debug - Found libraries")
                        for lib in self.data['facilities']['libraries']:
                            content += f"\n{lib['name']}:\n"
                            content += f"Location: {lib['location']}\n"
                            content += f"Hours: {lib['hours']}\n"
                            if 'resources' in lib:
                                content += "Resources:\n- " + "\n- ".join(lib['resources'])
                    
                    # Handle laboratories
                    if 'laboratories' in self.data['facilities'] and ('lab' in query or 'laboratory' in query):
                        print(f"Debug - Found laboratories")
                        for lab in self.data['facilities']['laboratories']:
                            content += f"\n{lab['name']} ({lab['department']}):\n"
                            if 'equipment' in lab:
                                content += "Equipment:\n- " + "\n- ".join(lab['equipment'])
                    
                    print(f"Debug - Adding facilities result with score: 85")
                    results.append({
                        'type': 'facilities',
                        'content': content,
                        'score': 85
                    })

            # If no specific matches and query is about university info, provide general info
            if not results and any(word in query for word in ['university', 'contact', 'about']):
                print(f"Debug - Found university info")
                if 'university_info' in self.data:
                    info = self.data['university_info']
                    content = f"Welcome to {info['name']}!\n\n"
                    content += f"Established: {info['established']}\n"
                    if 'location' in info:
                        content += f"Location: {info['location']['city']}, {info['location']['country']}\n"
                    if 'contact' in info:
                        content += "Contact:\n"
                        content += f"Email: {info['contact']['email']}\n"
                        content += f"Phone: {info['contact']['phone']}"
                    print(f"Debug - Adding general result with score: 70")
                    results.append({
                        'type': 'general',
                        'content': content,
                        'score': 70
                    })

            # Sort results by score and return the best match
            print(f"Debug - Sorting results")
            results.sort(key=lambda x: x['score'], reverse=True)
            return results

        except Exception as e:
            print(f"Error in search_data: {e}")
            return [{'type': 'error', 'content': 'I encountered an error while searching. Please try asking your question differently.', 'score': 0}]

class ChatbotService:
    def __init__(self):
        self.university_service = UniversityDataService()
        # Keywords for topic detection
        self.university_keywords = {
            'academic': ['course', 'program', 'degree', 'major', 'minor', 'faculty', 'study', 'semester', 'credit', 'class'],
            'admission': ['admission', 'apply', 'application', 'enrollment', 'register', 'registration', 'requirement'],
            'facilities': ['library', 'lab', 'laboratory', 'hostel', 'dorm', 'cafeteria', 'wifi', 'campus'],
            'administrative': ['fee', 'tuition', 'payment', 'deadline', 'schedule', 'office', 'department'],
            'general': ['university', 'college', 'student', 'teacher', 'professor', 'exam', 'grade', 'academic']
        }
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def is_university_related(self, query):
        """Check if the query is related to university topics."""
        try:
            tokens = word_tokenize(query.lower())
            lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
            
            for category_keywords in self.university_keywords.values():
                for keyword in category_keywords:
                    if keyword in lemmatized_tokens:
                        return True
            return False
        except Exception as e:
            print(f"Error in is_university_related: {e}")
            return True  # Default to True to avoid blocking valid queries

    def process_query(self, query):
        """Process a user query using the hybrid approach."""
        try:
            print(f"Debug - Processing query: {query}")
            
            if not query or len(query.strip()) == 0:
                return {
                    'response': "Please ask me a question about the university.",
                    'source': 'system'
                }

            # Get search results
            results = self.university_service.search_data(query)
            print(f"Debug - Got {len(results)} results")
            
            if results:
                # Get the best match
                best_match = results[0]
                print(f"Debug - Best match type: {best_match['type']}, score: {best_match['score']}")
                return {
                    'response': best_match['content'],
                    'source': best_match['type']
                }
            
            return {
                'response': "I apologize, but I couldn't find specific information about that. Could you please rephrase your question or ask about something else?",
                'source': 'system'
            }

        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                'response': "I apologize, but I encountered an error while processing your question. Please try asking in a different way.",
                'source': 'error'
            }
