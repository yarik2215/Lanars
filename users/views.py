from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from users.serializer import RegisterSerializer, UpdatePasswordSerializer, ProfileModelSerializer
from utils.permissions import IsOwner


class ProfileView(APIView):
    permission_classes = [IsOwner]
    
    def get(self, request):
        user = request.user
        serializer = ProfileModelSerializer(user)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=ProfileModelSerializer)
    def put(self, request):
        serializer = ProfileModelSerializer(request.user ,data=request.data)
        serializer.is_valid(True)
        user = serializer.save()
        return Response(ProfileModelSerializer(user).data, status=200)

    @swagger_auto_schema(request_body=ProfileModelSerializer)
    def patch(self, request):
        serializer = ProfileModelSerializer(request.user ,data=request.data, is_partial=True)
        serializer.is_valid(True)
        user = serializer.save()
        return Response(ProfileModelSerializer(user).data, status=200)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.pop("password2")
        password = data.pop("password")
        user = User(**data)
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UpdatePasswordSerializer)
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.validated_data["password"])
        self.request.user.save()
