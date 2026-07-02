from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health_check(request):
    return HttpResponse("healthy")


urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/chat/', include('chatbot.urls')),
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api_docs'),
    # Health check
    path('health/', health_check, name='health_check'),
]
