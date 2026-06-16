from django.urls import path
from . import views
from .views import PasswordResetRequestView, PasswordResetVerifyView, PasswordResetConfirmView





urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/',    views.login_user,    name='login'),
    path('logout/',   views.logout_user,   name='logout'),
    
    path('password-reset/', PasswordResetRequestView.as_view()),
    path('password-reset/verify/',  PasswordResetVerifyView.as_view()),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view()),
]
    