from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from account.views import UserProfileView, UserRegistrationView, UserLoginView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetEmailView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetEmailView.as_view(), name='send-reset-password-email'),

]