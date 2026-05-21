"""Analytics endpointlari."""
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sites.models import Site

from . import aggregations
from .filters import get_date_range, get_previous_range


SITE_PARAM = OpenApiParameter("site_id", int, required=True, description="Sayt ID")
FROM_PARAM = OpenApiParameter("from", str, description="Sana boshi (YYYY-MM-DD)")
TO_PARAM = OpenApiParameter("to", str, description="Sana oxiri (YYYY-MM-DD)")


class _AnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_site(self, request: Request) -> Site:
        site_id = request.query_params.get("site_id")
        if not site_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"site_id": "Majburiy parametr"})
        return get_object_or_404(Site, pk=site_id, user=request.user)


class OverviewView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        prev = get_previous_range(rng)

        cur = aggregations.overview(site.id, rng)
        old = aggregations.overview(site.id, prev)

        def delta(a: int, b: int) -> float:
            if not b:
                return 100.0 if a else 0.0
            return round((a - b) / b * 100, 1)

        cur["comparison"] = {
            "pageviews_delta_pct": delta(cur["total_pageviews"], old["total_pageviews"]),
            "visitors_delta_pct": delta(cur["unique_visitors"], old["unique_visitors"]),
            "sessions_delta_pct": delta(cur["total_sessions"], old["total_sessions"]),
        }
        return Response(cur)


class TimeseriesView(_AnalyticsView):
    @extend_schema(parameters=[
        SITE_PARAM, FROM_PARAM, TO_PARAM,
        OpenApiParameter("interval", str, description="day | hour"),
        OpenApiParameter("metric", str, description="pageviews | visitors | sessions"),
    ])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        interval = request.query_params.get("interval", "day")
        metric = request.query_params.get("metric", "pageviews")
        if interval not in ("day", "hour"):
            interval = "day"
        if metric not in ("pageviews", "visitors", "sessions"):
            metric = "pageviews"
        data = aggregations.timeseries(site.id, rng, interval=interval, metric=metric)
        return Response({"interval": interval, "metric": metric, "data": data})


class TopPagesView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        limit = min(int(request.query_params.get("limit", 10)), 50)
        return Response({"results": aggregations.top_pages(site.id, rng, limit=limit)})


class TopReferrersView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        limit = min(int(request.query_params.get("limit", 10)), 50)
        return Response({"results": aggregations.top_referrers(site.id, rng, limit=limit)})


class DevicesView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        return Response(aggregations.devices(site.id, rng))


class GeoView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        return Response(aggregations.geo(site.id, rng))


class EventsBreakdownView(_AnalyticsView):
    @extend_schema(parameters=[SITE_PARAM, FROM_PARAM, TO_PARAM])
    def get(self, request: Request) -> Response:
        site = self.get_site(request)
        rng = get_date_range(request.query_params)
        return Response({"results": aggregations.event_breakdown(site.id, rng)})
