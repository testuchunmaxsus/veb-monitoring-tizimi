"""Auth endpoints testlari."""
import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestRegister:
    URL = "/api/v1/auth/register/"

    def test_register_creates_user_and_tokens(self, api_client):
        resp = api_client.post(self.URL, {
            "email": "new@example.com",
            "password": "Strongpass123",
            "full_name": "Yangi",
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["user"]["email"] == "new@example.com"
        assert "access" in resp.data["tokens"]
        assert "refresh" in resp.data["tokens"]

    def test_register_rejects_short_password(self, api_client):
        resp = api_client.post(self.URL, {
            "email": "x@example.com",
            "password": "123",
            "full_name": "X",
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in resp.data

    def test_register_rejects_duplicate_email(self, api_client, user):
        resp = api_client.post(self.URL, {
            "email": "test@example.com",
            "password": "Strongpass123",
            "full_name": "Boshqa",
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


class TestLogin:
    URL = "/api/v1/auth/login/"

    def test_login_with_valid_credentials(self, api_client, user):
        resp = api_client.post(self.URL, {
            "email": "test@example.com",
            "password": "testpass123",
        }, format="json")
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data
        assert resp.data["user"]["email"] == "test@example.com"

    def test_login_with_invalid_password(self, api_client, user):
        resp = api_client.post(self.URL, {
            "email": "test@example.com",
            "password": "wrong",
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


class TestMe:
    URL = "/api/v1/auth/me/"

    def test_unauthenticated_returns_401(self, api_client):
        resp = api_client.get(self.URL)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_returns_user(self, auth_client, user):
        resp = auth_client.get(self.URL)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["email"] == user.email
