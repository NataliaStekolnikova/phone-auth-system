from django.urls import path
from . import views, web_views

urlpatterns = [
    # API endpoints
    path('send-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('profile/', views.get_profile, name='get_profile'),
    path('activate-invite/', views.activate_invite_code, name='activate_invite_code'),
    path('drf-login/', views.drf_login, name='drf_login'),
    
    # Web interface endpoints
    path('', web_views.index_view, name='index'),  # Добавляем корневой путь
    path('web/', web_views.index_view, name='web_index'),
    path('web/send-code/', web_views.send_code_view, name='web_send_code'),
    path('web/verify/', web_views.verify_code_view, name='web_verify'),
    path('web/profile/', web_views.profile_view, name='profile'),
    path('web/logout/', web_views.logout_view, name='logout'),
]