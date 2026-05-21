"""Tracking views — public endpointlar (autentifikatsiyasiz)."""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.realtime.broadcast import broadcast_event

from .serializers import (
    EventIngestSerializer,
    PageViewIngestSerializer,
    SessionEndSerializer,
)
from .services import (
    end_session,
    find_site,
    get_client_ip,
    get_or_create_session,
    record_event,
    record_pageview,
)
from .throttles import TrackingRateThrottle


class _PublicIngestView(APIView):
    """Public ingest view'lar uchun umumiy logika."""

    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_classes = (TrackingRateThrottle,)


class PageViewIngestView(_PublicIngestView):
    """Tracker'dan sahifa ko'rishini qabul qiladi."""

    serializer_class = PageViewIngestSerializer

    @extend_schema(request=PageViewIngestSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        site = find_site(data["api_key"])
        if not site:
            return Response({"detail": "Noto'g'ri API kalit"}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        ua_string = request.META.get("HTTP_USER_AGENT", "")

        session = get_or_create_session(
            site=site,
            session_uid=data["session_uid"],
            ip=ip,
            ua_string=ua_string,
            referrer=data.get("referrer", ""),
        )
        pv = record_pageview(site=site, session=session, data=data)

        broadcast_event(
            site_id=site.id,
            event_type="pageview",
            payload={
                "url": pv.url,
                "title": pv.title,
                "country": session.country_code,
                "browser": session.browser,
                "is_mobile": session.is_mobile,
                "timestamp": pv.timestamp.isoformat(),
            },
        )

        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class EventIngestView(_PublicIngestView):
    """Custom event qabul qiladi."""

    serializer_class = EventIngestSerializer

    @extend_schema(request=EventIngestSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        site = find_site(data["api_key"])
        if not site:
            return Response({"detail": "Noto'g'ri API kalit"}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        ua_string = request.META.get("HTTP_USER_AGENT", "")

        session = get_or_create_session(
            site=site,
            session_uid=data["session_uid"],
            ip=ip,
            ua_string=ua_string,
            referrer="",
        )
        event = record_event(site=site, session=session, data=data)

        broadcast_event(
            site_id=site.id,
            event_type="event",
            payload={
                "type": event.type,
                "target": event.target,
                "timestamp": event.timestamp.isoformat(),
            },
        )

        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class SessionEndView(_PublicIngestView):
    """Sessiya tugashini qayd etadi (sendBeacon target)."""

    serializer_class = SessionEndSerializer

    @extend_schema(request=SessionEndSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        site = find_site(data["api_key"])
        if not site:
            return Response({"ok": True})

        from .models import Session
        session = (
            Session.objects.filter(site=site, session_uid=data["session_uid"])
            .order_by("-started_at")
            .first()
        )
        if session:
            end_session(session=session, duration_sec=data.get("duration_sec", 0))

        return Response({"ok": True})
