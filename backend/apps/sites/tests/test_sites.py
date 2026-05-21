"""Sites endpoints testlari."""
import pytest
from rest_framework import status

from apps.sites.models import Site

pytestmark = pytest.mark.django_db


class TestSiteCRUD:
    URL = "/api/v1/sites/"

    def test_list_returns_only_user_sites(self, auth_client, user, site):
        # Boshqa userning sayti
        from apps.accounts.models import User
        other = User.objects.create_user(email="other@example.com", password="x")
        Site.objects.create(user=other, name="Other", domain="other.com")

        resp = auth_client.get(self.URL)
        assert resp.status_code == 200
        domains = [s["domain"] for s in resp.data["results"]]
        assert "test.com" in domains
        assert "other.com" not in domains

    def test_create_site_generates_api_key(self, auth_client):
        resp = auth_client.post(self.URL, {
            "name": "Yangi sayt",
            "domain": "https://www.example.com/",
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["domain"] == "example.com"
        assert resp.data["api_key"].startswith("vmt_")
        assert len(resp.data["api_key"]) > 30

    def test_create_rejects_invalid_domain(self, auth_client):
        resp = auth_client.post(self.URL, {
            "name": "Bad", "domain": "not a domain",
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_regenerate_api_key(self, auth_client, site):
        old_key = site.api_key
        resp = auth_client.post(f"{self.URL}{site.id}/regenerate-api-key/")
        assert resp.status_code == 200
        assert resp.data["api_key"] != old_key
        assert resp.data["api_key"].startswith("vmt_")

    def test_cannot_access_other_user_site(self, auth_client):
        from apps.accounts.models import User
        other = User.objects.create_user(email="other@example.com", password="x")
        other_site = Site.objects.create(user=other, name="Other", domain="other.com")

        resp = auth_client.get(f"{self.URL}{other_site.id}/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
