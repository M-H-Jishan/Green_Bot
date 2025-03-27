from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from .models import KnowledgeBase, QueryLog
from .services import ChatbotService

class KnowledgeBaseTests(TestCase):
    def setUp(self):
        self.kb_entry = KnowledgeBase.objects.create(
            question="What is Python?",
            answer="Python is a programming language.",
            source_url="https://python.org"
        )

    def test_knowledge_base_creation(self):
        self.assertEqual(self.kb_entry.question, "What is Python?")
        self.assertTrue(isinstance(self.kb_entry, KnowledgeBase))

class ChatbotServiceTests(TestCase):
    def setUp(self):
        self.service = ChatbotService()
        self.kb_entry = KnowledgeBase.objects.create(
            question="What is Python?",
            answer="Python is a programming language.",
            source_url="https://python.org"
        )

    def test_knowledge_base_search(self):
        response = self.service.search_knowledge_base("What is Python?")
        self.assertIsNotNone(response)
        self.assertEqual(response['source'], 'KB')

    @patch('openai.ChatCompletion.acreate')
    async def test_openai_response(self, mock_openai):
        mock_openai.return_value.choices = [
            type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': 'Mocked OpenAI response'
                })
            })
        ]
        
        response = await self.service.get_openai_response("Test question")
        self.assertEqual(response['source'], 'AI')
        self.assertTrue(response['success'])

class ChatbotAPITests(APITestCase):
    def setUp(self):
        self.kb_entry = KnowledgeBase.objects.create(
            question="What is Python?",
            answer="Python is a programming language.",
            source_url="https://python.org"
        )

    @patch('chatbot.services.ChatbotService.process_query')
    async def test_ask_endpoint(self, mock_process):
        mock_process.return_value = {
            'response': 'Test response',
            'source': 'KB',
            'success': True
        }
        
        url = reverse('chatbot-ask')
        data = {'query': 'What is Python?'}
        response = await self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source'], 'KB')

    def test_rate_limiting(self):
        url = reverse('chatbot-ask')
        data = {'query': 'Test query'}
        
        # Make 11 requests (1 over limit)
        for _ in range(11):
            response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
