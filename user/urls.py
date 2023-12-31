from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                         ResetPasswordConfirmView, GetMeView)

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view()),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
    path('reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('get-me', GetMeView.as_view())
]
