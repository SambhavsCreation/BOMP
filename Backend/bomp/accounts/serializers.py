from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Basic email validation (presence) is handled by EmailField
        # More complex validation (e.g. uniqueness) is handled by Django's User model
        # We should also check for email uniqueness here if not handled by the model's clean method
        # For now, relying on model's default behavior.
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
            # is_2fa_enabled is not set here, defaults to False as per model
        )
        # Do not set user.is_active = False here unless email verification is implemented
        return user
