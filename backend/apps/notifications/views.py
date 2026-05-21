"""Notifications views."""
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user).order_by("-created_at")
        if self.request.query_params.get("unread_only") in ("true", "1"):
            qs = qs.filter(is_read=False)
        return qs

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request: Request) -> Response:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({"count": count})

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request: Request, pk=None) -> Response:
        n = self.get_object()
        if not n.is_read:
            n.is_read = True
            n.save(update_fields=["is_read"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request: Request) -> Response:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
