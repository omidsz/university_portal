import json
from rest_framework.generics import (ListAPIView,CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailVerificationCode
from .token_serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsModerator, IsMember
from .serializers import RegisterSerializer, VerifyCodeSerializer
from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework import permissions, viewsets

from .serializers import UserSerializer
# from .serializers import EmailSendCodeSerializer, EmailVerifyCodeSerializer

###################################################################################
class UserListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserPageView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "صفحه کاربر عادی"})


def showuserpage(request):
    return render(request, 'accounts/users.html')


####################################################################################

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class RegistePageView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "صفحه register"})

def show_register_page_view(request):
    return render(request, 'accounts/signup.html')

#################################################################################################
def login_page(request):
    return render(request, 'accounts/login.html')

###############################################################################################
class VerifyCodeAndRegisterAPIView(APIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        serializer = VerifyCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        email = serializer.validated_data['email']
        username = request.session.get('reg_username')
        password = request.session.get('reg_password')

        if not all([email, username, password]):
            return Response({'error': 'اطلاعات ثبت‌نام در session یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = EmailVerificationCode.objects.get(email=email, code=code)
        except EmailVerificationCode.DoesNotExist:
            return Response({'error': 'کد تأیید نادرست است.'}, status=status.HTTP_400_BAD_REQUEST)

        if record.is_expired():
            return Response({'error': 'کد منقضی شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'این نام کاربری قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'این ایمیل قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        record.delete()
        request.session.flush()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)


def verify_code_page(request):
    return render(request, 'accounts/verify_code.html')


################################################################################################
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MemberPageView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request):
        return Response({"message": "صفحه عضو انجمن"})


class ModeratorPageView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        return Response({"message": "داشبورد مدیر انجمن"})

#################################################################################









