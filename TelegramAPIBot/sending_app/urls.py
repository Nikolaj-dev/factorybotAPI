from django.urls import path
from .views import UserRegistrationView, TokenGenerationView, LoginView, MessageCreateAPIView, MessageListAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='custom-user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create-token/', TokenGenerationView.as_view(), name='token-create'),
    path('send_message/', MessageCreateAPIView.as_view(), name='send_message'),
    path('my_messages/', MessageListAPIView.as_view(), name='my_messages'),
]
