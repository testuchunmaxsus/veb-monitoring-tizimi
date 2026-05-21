"""pytest umumiy fixturalar."""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db):
    from apps.accounts.models import User
    return User.objects.create_user(
        email="test@example.com", password="testpass123", full_name="Test User",
    )


@pytest.fixture
def auth_client(api_client: APIClient, user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def site(db, user):
    from apps.sites.models import Site
    return Site.objects.create(user=user, name="Test sayt", domain="test.com")
