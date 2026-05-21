import { apiClient } from './client';

export interface Overview {
  total_pageviews: number;
  unique_visitors: number;
  total_sessions: number;
  bounce_rate: number;
  avg_session_duration_sec: number;
  comparison: {
    pageviews_delta_pct: number;
    visitors_delta_pct: number;
    sessions_delta_pct: number;
  };
}

export interface TimeseriesPoint {
  timestamp: string;
  value: number;
}

export interface TopPage {
  url: string;
  title: string;
  views: number;
  unique_visitors: number;
}

export interface TopReferrer {
  referrer: string;
  visits: number;
}

export interface DeviceBreakdown {
  by_type: Array<{ name: string; count: number }>;
  by_browser: Array<{ name: string; count: number }>;
  by_os: Array<{ name: string; count: number }>;
  by_device: Array<{ name: string; count: number }>;
}

export interface GeoBreakdown {
  by_country: Array<{ code: string; name: string; visits: number }>;
  by_city: Array<{ name: string; country: string; visits: number }>;
}

export interface DateRange {
  from: string;
  to: string;
}

const params = (siteId: number, range: DateRange, extra: Record<string, string> = {}) =>
  ({ site_id: String(siteId), from: range.from, to: range.to, ...extra });

export const analyticsApi = {
  overview: (siteId: number, range: DateRange) =>
    apiClient.get<Overview>('/analytics/overview/', { params: params(siteId, range) }).then((r) => r.data),

  timeseries: (siteId: number, range: DateRange, interval = 'day', metric = 'pageviews') =>
    apiClient
      .get<{ interval: string; metric: string; data: TimeseriesPoint[] }>(
        '/analytics/timeseries/',
        { params: params(siteId, range, { interval, metric }) }
      )
      .then((r) => r.data),

  topPages: (siteId: number, range: DateRange, limit = 10) =>
    apiClient
      .get<{ results: TopPage[] }>('/analytics/top-pages/', { params: params(siteId, range, { limit: String(limit) }) })
      .then((r) => r.data.results),

  topReferrers: (siteId: number, range: DateRange, limit = 10) =>
    apiClient
      .get<{ results: TopReferrer[] }>('/analytics/top-referrers/', {
        params: params(siteId, range, { limit: String(limit) }),
      })
      .then((r) => r.data.results),

  devices: (siteId: number, range: DateRange) =>
    apiClient.get<DeviceBreakdown>('/analytics/devices/', { params: params(siteId, range) }).then((r) => r.data),

  geo: (siteId: number, range: DateRange) =>
    apiClient.get<GeoBreakdown>('/analytics/geo/', { params: params(siteId, range) }).then((r) => r.data),
};
