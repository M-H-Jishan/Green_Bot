from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

def health_check(request):
    return HttpResponse("healthy")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chatbot/ask/', include('chatbot.urls')),
    path('api-token-auth/', token_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('health/', health_check, name='health_check'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]
