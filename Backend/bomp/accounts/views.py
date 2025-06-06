from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer # Assuming serializers.py is in the same app
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Anyone can register

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] # Only authenticated users can logout

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required.", "detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            # Optionally, if you want to invalidate the access token as well,
            # you would need a more complex setup, possibly involving a client-side mechanism
            # or a server-side token store for access tokens if they are long-lived.
            # For simplejwt, blacklisting the refresh token is the standard way to "logout".
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except TokenError as e: # Catch specific TokenError
            return Response({"error": "Invalid token.", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: # Catch any other unexpected errors
            # It's good practice to log this exception server-side
            return Response({"error": "An unexpected error occurred.", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Note: Login view (TokenObtainPairView) and TokenRefreshView from simplejwt
# will be added directly to urls.py in the next subtask.
