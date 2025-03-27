from rest_framework import serializers
from .models import KnowledgeBase, QueryLog

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'question', 'answer', 'source_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = ['id', 'query', 'response', 'source', 'timestamp', 'success', 'error_message']
        read_only_fields = ['timestamp']

class ChatbotQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="User's question")

class ChatbotResponseSerializer(serializers.Serializer):
    response = serializers.CharField(help_text="Bot's answer")
    source_url = serializers.URLField(required=False, allow_null=True, help_text="Reference URL if available")
    source = serializers.CharField(help_text="Source of the response (KB/AI/FB)")
    success = serializers.BooleanField(default=True, help_text="Whether the response was successful")
    error_message = serializers.CharField(required=False, allow_null=True, help_text="Error message if any")
