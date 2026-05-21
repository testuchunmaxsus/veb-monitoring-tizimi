"""Reports views."""
import threading

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Report
from .serializers import ReportCreateSerializer, ReportSerializer
from .tasks import generate_report


class ReportViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Hisobotlarni boshqarish."""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return ReportCreateSerializer
        return ReportSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save()

        # Synchronous generatsiya alohida thread'da (django-q2 mavjud bo'lsa, queue.async_task)
        threading.Thread(target=generate_report, args=(report.pk,), daemon=True).start()

        return Response(
            ReportSerializer(report, context={"request": request}).data,
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=True, methods=["get"])
    def download(self, request: Request, pk=None) -> FileResponse:
        report = get_object_or_404(self.get_queryset(), pk=pk)
        if not report.file or report.status != Report.Status.DONE:
            raise Http404("Fayl tayyor emas")
        response = FileResponse(report.file.open("rb"), as_attachment=True)
        return response
