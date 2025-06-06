import pyotp
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    TwoFAVerifySerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        profile = user.profile
        if profile.two_factor_enabled:
            request.session["pre_2fa_user"] = user.id
            return Response({"detail": "2fa required"}, status=202)
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class TwoFALoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.session.get("pre_2fa_user")
        if not user_id:
            return Response({"detail": "No pending authentication"}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Invalid session"}, status=400)
        serializer = TwoFAVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        totp = pyotp.TOTP(user.profile.totp_secret)
        if not totp.verify(serializer.validated_data["token"]):
            return Response({"detail": "Invalid token"}, status=400)
        refresh = RefreshToken.for_user(user)
        del request.session["pre_2fa_user"]
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class Enable2FAView(APIView):
    def post(self, request):
        profile = request.user.profile
        if profile.two_factor_enabled:
            return Response({"detail": "2fa already enabled"}, status=400)
        profile.totp_secret = pyotp.random_base32()
        profile.save()
        totp = pyotp.TOTP(profile.totp_secret)
        return Response({"secret": profile.totp_secret, "otp_uri": totp.provisioning_uri(name=request.user.username, issuer_name="BOMP")})


class ConfirmEnable2FAView(APIView):
    def post(self, request):
        profile = request.user.profile
        if not profile.totp_secret:
            return Response({"detail": "2fa not initiated"}, status=400)
        serializer = TwoFAVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        totp = pyotp.TOTP(profile.totp_secret)
        if totp.verify(serializer.validated_data["token"]):
            profile.two_factor_enabled = True
            profile.save()
            return Response({"detail": "2fa enabled"})
        return Response({"detail": "Invalid token"}, status=400)
