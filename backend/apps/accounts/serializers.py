"""Auth serializers."""
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "date_joined")
        read_only_fields = ("id", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], min_length=8,
    )

    class Meta:
        model = User
        fields = ("email", "password", "full_name")

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError({"detail": "Email yoki parol noto'g'ri."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Hisob bloklangan."})
        attrs["user"] = user
        return attrs


def issue_tokens(user: User) -> dict:
    """Foydalanuvchi uchun JWT tokenlar yaratadi."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
