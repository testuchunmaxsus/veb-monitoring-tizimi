"""Auth views."""
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    UserSerializer,
    issue_tokens,
)


class RegisterView(APIView):
    """Yangi foydalanuvchini ro'yxatdan o'tkazadi va JWT tokenlar qaytaradi."""

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses={201: OpenApiResponse(description="Foydalanuvchi yaratildi")},
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = issue_tokens(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Email va parol orqali tizimga kiradi va JWT tokenlar qaytaradi."""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(request=LoginSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = issue_tokens(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                **tokens,
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    """Joriy foydalanuvchi profilini qaytaradi."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=UserSerializer)
    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    """Refresh tokenni blacklist qiladi."""

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    @extend_schema(request=LogoutSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Token noto'g'ri yoki muddati o'tgan."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
