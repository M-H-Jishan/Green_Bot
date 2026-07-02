import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit

from .serializers import ChatbotQuerySerializer, ChatbotResponseSerializer
from .services import ChatbotService

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='user', rate='20/m', method='POST', block=True)
def chatbot_ask(request):
    """
    Process a chatbot query.
    Requires JWT authentication. Rate limited to 20 requests/minute per user.
    """
    serializer = ChatbotQuerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    query = serializer.validated_data['query']

    logger.info(f"Chatbot query from user {request.user.username}: {query[:100]}")

    try:
        service = ChatbotService()
        result = service.process_query(query)

        response_data = {
            'response': result['response'],
            'source': result['source'],
            'source_url': result.get('source_url'),
            'success': result.get('success', True),
            'error_message': result.get('error'),
        }
        response_serializer = ChatbotResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Unexpected error in chatbot_ask: {e}")
        return Response(
            {
                'response': 'An internal error occurred. Please try again.',
                'source': 'error',
                'source_url': None,
                'success': False,
                'error_message': str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
