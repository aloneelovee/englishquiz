import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from user.models import User, getKey
from user.serializers import (UserRegisterSerializer, CheckActivationCodeSerializer, ResetPasswordSerializer,
                               ResetPasswordConfirmSerializer)
from rest_framework.views import APIView

class UserRegisterCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckActivationCodeGenericAPIView(GenericAPIView):
    serializer_class = CheckActivationCodeSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = getKey(key=data['email'])['user']
        user.is_active = True
        user.save()
        return Response({"message": "Your email has been confirmed"}, status=status.HTTP_200_OK)


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            activation_code = str(random.randint(100000, 999999))
            user.set_password(activation_code)
            user.save()

            send_mail(
                'Password Reset Confirmation',
                f'Your password reset code is: {activation_code}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )

            return Response({"detail": "Password reset code sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this email."}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(activation_code):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "New password and confirm password do not match."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Invalid activation code."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetMeView(APIView):
    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            user_data = {
                'id': request.user.id,
                'full_name': request.user.full_name,
                'username': request.user.username,
                'email': request.user.email,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
