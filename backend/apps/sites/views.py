"""Site views."""
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Site
from .serializers import SiteCreateSerializer, SiteSerializer


class SiteViewSet(viewsets.ModelViewSet):
    """
    Saytlarni boshqarish.

    list: Foydalanuvchining barcha saytlari
    create: Yangi sayt qo'shish
    retrieve: Bitta sayt
    update/partial_update: Sayt sozlamalarini yangilash
    destroy: Saytni o'chirish (barcha statistika bilan)
    regenerate_api_key: Yangi API kalit generatsiya qilish
    """

    permission_classes = (IsAuthenticated,)
    search_fields = ("name", "domain")
    ordering_fields = ("created_at", "name")
    ordering = ("-created_at",)

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return SiteCreateSerializer
        return SiteSerializer

    @action(detail=True, methods=["post"], url_path="regenerate-api-key")
    def regenerate_api_key(self, request, pk=None):
        site = get_object_or_404(self.get_queryset(), pk=pk)
        new_key = site.regenerate_api_key()
        return Response({"api_key": new_key}, status=status.HTTP_200_OK)
