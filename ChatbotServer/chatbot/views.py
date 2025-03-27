from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .services import ChatbotService

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    permission_classes = [AllowAny]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatbot_service = ChatbotService()

    def post(self, request, *args, **kwargs):
        try:
            # Get message from request data
            message = request.data.get('message', '')
            
            if not message:
                return Response({
                    'error': 'No message provided',
                    'response': 'Please provide a message to get a response.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Process the message
            result = self.chatbot_service.process_query(message)
            
            # Return the response
            return Response({
                'response': result.get('response', 'Sorry, I could not process your request.'),
                'source': result.get('source', 'system')
            })
            
        except Exception as e:
            print(f"Error in ChatbotView: {e}")
            return Response({
                'error': 'Internal server error',
                'response': 'Sorry, I encountered an error. Please try again.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
