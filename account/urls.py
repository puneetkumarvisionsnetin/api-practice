from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from account.views import UserProfileView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]