import json
import os
import logging

from django.conf import settings
from rapidfuzz import fuzz

from .models import KnowledgeBase, QueryLog
from .llm_provider import get_llm_provider

logger = logging.getLogger(__name__)


class CustomDataService:
    """Load and search custom JSON data for relevant information."""

    def __init__(self):
        data_path = settings.DATA_FILE_PATH
        if not os.path.isabs(data_path):
            data_path = os.path.join(settings.BASE_DIR, data_path)
        self.data_file = data_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.data_file}")
            return {}
        except Exception as e:
            logger.error(f"Error loading data file: {e}")
            return {}

    def search_data(self, query):
        """Search all data for relevant information matching the query."""
        query = query.lower()
        results = []

        try:
            # Search academic programs
            if 'academic_programs' in self.data:
                for level, programs in self.data['academic_programs'].items():
                    for program in programs:
                        program_name = program['name'].lower()
                        program_name_similarity = fuzz.token_set_ratio(query, program_name)
                        asks_about_requirements = 'requirement' in query or 'admission' in query
                        asks_about_specific = program_name in query or program.get('degree', '').lower() in query

                        if program_name_similarity > 60 or asks_about_specific or (
                            asks_about_requirements and any(kw in program_name for kw in query.split())
                        ):
                            content = f"{program['name']} ({program.get('degree', '')}):\n{program.get('description', '')}\n"

                            if asks_about_requirements and 'requirements' in program:
                                content += "\nAdmission Requirements:\n- " + "\n- ".join(program['requirements'])

                            if 'career_prospects' in program and not asks_about_requirements:
                                content += "\n\nCareer Prospects:\n- " + "\n- ".join(program['career_prospects'])

                            score = 90 if asks_about_specific else program_name_similarity
                            results.append({
                                'type': 'program',
                                'content': content,
                                'score': score
                            })

            # Search facilities
            if 'facilities' in self.data:
                facility_keywords = ['facility', 'facilities', 'campus', 'library', 'lab', 'hostel']
                if any(keyword in query for keyword in facility_keywords):
                    content = "Campus Facilities:\n"

                    if 'libraries' in self.data['facilities'] and ('library' in query or 'libraries' in query):
                        for lib in self.data['facilities']['libraries']:
                            content += f"\n{lib['name']}:\n"
                            content += f"Location: {lib.get('location', 'N/A')}\n"
                            content += f"Hours: {lib.get('hours', 'N/A')}\n"
                            if 'resources' in lib:
                                content += "Resources:\n- " + "\n- ".join(lib['resources'])

                    if 'laboratories' in self.data['facilities'] and ('lab' in query or 'laboratory' in query):
                        for lab in self.data['facilities']['laboratories']:
                            content += f"\n{lab['name']} ({lab.get('department', '')}):\n"
                            if 'equipment' in lab:
                                content += "Equipment:\n- " + "\n- ".join(lab['equipment'])

                    results.append({
                        'type': 'facilities',
                        'content': content,
                        'score': 85
                    })

            # General university info
            if not results and any(word in query for word in ['university', 'contact', 'about']):
                if 'university_info' in self.data:
                    info = self.data['university_info']
                    content = f"Welcome to {info.get('name', 'our institution')}!\n\n"
                    content += f"Established: {info.get('established', 'N/A')}\n"
                    if 'location' in info:
                        content += f"Location: {info['location'].get('city', '')}, {info['location'].get('country', '')}\n"
                    if 'contact' in info:
                        content += "Contact:\n"
                        content += f"Email: {info['contact'].get('email', 'N/A')}\n"
                        content += f"Phone: {info['contact'].get('phone', 'N/A')}"
                    results.append({
                        'type': 'general',
                        'content': content,
                        'score': 70
                    })

            results.sort(key=lambda x: x['score'], reverse=True)
            return results

        except Exception as e:
            logger.error(f"Error in search_data: {e}")
            return [{'type': 'error', 'content': 'I encountered an error while searching. Please try asking differently.', 'score': 0}]

    def get_context_string(self):
        """Return a compact string representation of the data for LLM context injection."""
        if not self.data:
            return ""
        try:
            return json.dumps(self.data, ensure_ascii=False)[:3000]
        except Exception:
            return ""


class ChatbotService:
    """Main chatbot service: hybrid search (KB + custom data) with LLM fallback."""

    def __init__(self):
        self.data_service = CustomDataService()
        self.llm_provider = get_llm_provider()

    def search_knowledge_base(self, query):
        """Search the KnowledgeBase model for a matching entry."""
        try:
            entries = KnowledgeBase.objects.all()
            best_match = None
            best_score = 0

            for entry in entries:
                score = fuzz.token_set_ratio(query.lower(), entry.question.lower())
                if score > best_score:
                    best_score = score
                    best_match = entry

            if best_match and best_score > 60:
                return {
                    'response': best_match.answer,
                    'source': 'KB',
                    'source_url': best_match.source_url or None,
                    'success': True,
                    'error': None
                }
            return None
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return None

    def process_query(self, query):
        """Process a user query using the hybrid approach: KB → custom data → LLM fallback."""
        result = None

        if not query or len(query.strip()) == 0:
            result = {
                'response': "Please ask me a question.",
                'source': 'system',
                'source_url': None,
                'success': True,
                'error': None
            }
            self._log_query(query, result)
            return result

        # 1. Try KnowledgeBase
        result = self.search_knowledge_base(query)

        # 2. Try custom JSON data
        if not result:
            data_results = self.data_service.search_data(query)
            if data_results and data_results[0]['score'] > 0:
                best = data_results[0]
                result = {
                    'response': best['content'],
                    'source': best['type'],
                    'source_url': None,
                    'success': True,
                    'error': None
                }

        # 3. LLM fallback
        if not result and self.llm_provider:
            context = self.data_service.get_context_string()
            llm_result = self.llm_provider.get_response(query, context=context)
            if llm_result['success']:
                result = {
                    'response': llm_result['response'],
                    'source': 'AI',
                    'source_url': None,
                    'success': True,
                    'error': None
                }
            else:
                logger.error(f"LLM error: {llm_result['error']}")

        # 4. Default fallback
        if not result:
            result = {
                'response': "I apologize, but I couldn't find specific information about that. Could you please rephrase your question?",
                'source': 'system',
                'source_url': None,
                'success': True,
                'error': None
            }

        self._log_query(query, result)
        return result

    def _log_query(self, query, result):
        """Log the query and response to QueryLog for analytics."""
        try:
            QueryLog.objects.create(
                query=query[:5000],
                response=result.get('response', '')[:5000],
                source=result.get('source', 'unknown'),
                success=result.get('success', True),
                error_message=result.get('error')
            )
        except Exception as e:
            logger.error(f"Failed to log query: {e}")
