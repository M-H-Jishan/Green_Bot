from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('chat/', views.ChatbotView.as_view(), name='chatbot-ask'),
]
