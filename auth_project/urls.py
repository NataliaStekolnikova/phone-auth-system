from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

def api_info(request):
    return JsonResponse({
        'message': 'Phone Auth System API',
        'status': 'active',
        'version': '1.0.0',
        'documentation': {
            'redoc': '/api/docs/',
            'swagger': '/api/swagger/',
            'openapi_schema': '/api/schema/'
        },
        'endpoints': {
            'send_code': '/api/users/send-code/',
            'verify_code': '/api/users/verify-code/', 
            'profile': '/api/users/profile/',
            'activate_invite': '/api/users/activate-invite/'
        },
        'web_interface': '/users/',
        'description': 'Реферальная система с авторизацией по телефону'
    })

def redirect_to_web(request):
    return redirect('/users/')

urlpatterns = [
    # Главная страница и веб-интерфейс
    path('', redirect_to_web, name='home'),
    path('users/', include('users.urls')),
    
    # API endpoints
    path('api/', api_info, name='api_info'),
    path('api/users/', include('users.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Admin
    path('admin/', admin.site.urls),
]