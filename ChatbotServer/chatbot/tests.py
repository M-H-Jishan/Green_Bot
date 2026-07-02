from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock

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
        result = self.service.search_knowledge_base("What is Python?")
        self.assertIsNotNone(result)
        self.assertEqual(result['source'], 'KB')
        self.assertTrue(result['success'])

    def test_knowledge_base_no_match(self):
        result = self.service.search_knowledge_base("xyzabc12345")
        self.assertIsNone(result)

    def test_process_query_empty(self):
        result = self.service.process_query("")
        self.assertEqual(result['source'], 'system')
        self.assertIn('ask me', result['response'].lower())

    def test_process_query_kb_match(self):
        result = self.service.process_query("What is Python?")
        self.assertEqual(result['source'], 'KB')
        self.assertEqual(result['response'], "Python is a programming language.")

    def test_process_query_logs_to_querylog(self):
        self.service.process_query("What is Python?")
        self.assertTrue(QueryLog.objects.filter(query="What is Python?").exists())

    @patch('chatbot.services.get_llm_provider')
    def test_process_query_llm_fallback(self, mock_get_provider):
        mock_provider = MagicMock()
        mock_provider.get_response.return_value = {
            'response': 'AI generated answer',
            'success': True,
            'error': None
        }
        mock_get_provider.return_value = mock_provider

        service = ChatbotService()
        service.llm_provider = mock_provider
        # Use a query with no word overlap with the KB entry about Python
        result = service.process_query("xyzabc12345")
        self.assertEqual(result['source'], 'AI')
        self.assertEqual(result['response'], 'AI generated answer')

    @patch('chatbot.services.get_llm_provider')
    def test_process_query_llm_failure_falls_back(self, mock_get_provider):
        mock_provider = MagicMock()
        mock_provider.get_response.return_value = {
            'response': '',
            'success': False,
            'error': 'API key invalid'
        }
        mock_get_provider.return_value = mock_provider

        service = ChatbotService()
        service.llm_provider = mock_provider
        result = service.process_query("xyzabc12345")
        self.assertEqual(result['source'], 'system')
        self.assertIn("couldn't find", result['response'].lower())


class ChatbotAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.kb_entry = KnowledgeBase.objects.create(
            question="What is Python?",
            answer="Python is a programming language.",
            source_url="https://python.org"
        )
        self.url = reverse('chatbot-ask')

    def test_ask_endpoint_requires_auth(self):
        response = self.client.post(self.url, {'query': 'What is Python?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ask_endpoint_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'query': 'What is Python?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source'], 'KB')

    def test_ask_endpoint_accepts_message_alias(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'message': 'What is Python?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ask_endpoint_empty_query(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ask_endpoint_response_format(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'query': 'What is Python?'}, format='json')
        self.assertIn('response', response.data)
        self.assertIn('source', response.data)
        self.assertIn('success', response.data)
