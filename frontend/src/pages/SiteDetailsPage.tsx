import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Eye, Users, Activity, Clock, ArrowLeft } from 'lucide-react';
import clsx from 'clsx';
import { sitesApi } from '@/api/sites';
import { analyticsApi } from '@/api/analytics';
import { MetricCard } from '@/components/charts/MetricCard';
import { LineChart } from '@/components/charts/LineChart';
import { BarChart } from '@/components/charts/BarChart';
import { PieChart } from '@/components/charts/PieChart';
import { TopPagesTable } from '@/components/analytics/TopPagesTable';
import { TopReferrersTable } from '@/components/analytics/TopReferrersTable';
import { GeoTable } from '@/components/analytics/GeoTable';
import { DateRangePicker, DateRange } from '@/components/ui/DateRangePicker';
import { formatDuration, formatNumber, formatPercent, getDateRange } from '@/lib/format';

const TABS = [
  { id: 'overview', label: 'Umumiy' },
  { id: 'pages', label: 'Sahifalar' },
  { id: 'devices', label: 'Qurilmalar' },
  { id: 'geo', label: 'Geografiya' },
] as const;

type TabId = (typeof TABS)[number]['id'];

export default function SiteDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const siteId = Number(id);
  const [tab, setTab] = useState<TabId>('overview');
  const [range, setRange] = useState<DateRange>(getDateRange(7));

  const siteQ = useQuery({ queryKey: ['site', siteId], queryFn: () => sitesApi.get(siteId), enabled: !!siteId });
  const overviewQ = useQuery({
    queryKey: ['overview', siteId, range],
    queryFn: () => analyticsApi.overview(siteId, range),
    enabled: !!siteId,
  });
  const tsQ = useQuery({
    queryKey: ['ts', siteId, range],
    queryFn: () => analyticsApi.timeseries(siteId, range, 'day', 'pageviews'),
    enabled: !!siteId,
  });
  const topPagesQ = useQuery({
    queryKey: ['top-pages', siteId, range],
    queryFn: () => analyticsApi.topPages(siteId, range),
    enabled: !!siteId && (tab === 'overview' || tab === 'pages'),
  });
  const topRefsQ = useQuery({
    queryKey: ['top-refs', siteId, range],
    queryFn: () => analyticsApi.topReferrers(siteId, range),
    enabled: !!siteId && tab === 'overview',
  });
  const devicesQ = useQuery({
    queryKey: ['devices', siteId, range],
    queryFn: () => analyticsApi.devices(siteId, range),
    enabled: !!siteId && tab === 'devices',
  });
  const geoQ = useQuery({
    queryKey: ['geo', siteId, range],
    queryFn: () => analyticsApi.geo(siteId, range),
    enabled: !!siteId && tab === 'geo',
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <Link to="/sites" className="text-xs text-gray-500 hover:text-brand-600 inline-flex items-center gap-1">
            <ArrowLeft size={12} /> Saytlar
          </Link>
          <h1 className="text-2xl font-bold mt-1">{siteQ.data?.name || 'Yuklanmoqda...'}</h1>
          <p className="text-sm text-gray-500">{siteQ.data?.domain}</p>
        </div>
        <DateRangePicker value={range} onChange={setRange} />
      </div>

      <div className="border-b border-gray-200">
        <div className="flex gap-1">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={clsx(
                'px-4 py-2 text-sm font-medium border-b-2 transition-colors',
                tab === t.id
                  ? 'border-brand-600 text-brand-700'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              )}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {tab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              label="Sahifa ko'rishlari"
              value={overviewQ.data ? formatNumber(overviewQ.data.total_pageviews) : '—'}
              delta={overviewQ.data?.comparison.pageviews_delta_pct}
              icon={<Eye size={18} />}
            />
            <MetricCard
              label="Tashrif buyuruvchilar"
              value={overviewQ.data ? formatNumber(overviewQ.data.unique_visitors) : '—'}
              delta={overviewQ.data?.comparison.visitors_delta_pct}
              icon={<Users size={18} />}
            />
            <MetricCard
              label="Sessiyalar"
              value={overviewQ.data ? formatNumber(overviewQ.data.total_sessions) : '—'}
              delta={overviewQ.data?.comparison.sessions_delta_pct}
              icon={<Activity size={18} />}
            />
            <MetricCard
              label="O'rtacha vaqt"
              value={overviewQ.data ? formatDuration(overviewQ.data.avg_session_duration_sec) : '—'}
              hint={overviewQ.data ? `Bounce: ${formatPercent(overviewQ.data.bounce_rate)}` : ''}
              icon={<Clock size={18} />}
            />
          </div>

          <div className="card">
            <h2 className="font-semibold mb-4">Sahifa ko'rishlari (vaqt bo'yicha)</h2>
            {tsQ.data && tsQ.data.data.length > 0 ? (
              <LineChart data={tsQ.data.data} />
            ) : (
              <div className="text-sm text-gray-400 text-center py-8">Ma'lumot yo'q</div>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="font-semibold mb-4">Eng mashhur sahifalar</h2>
              {topPagesQ.data ? <TopPagesTable data={topPagesQ.data} /> : null}
            </div>
            <div className="card">
              <h2 className="font-semibold mb-4">Manbalar (Referrers)</h2>
              {topRefsQ.data ? <TopReferrersTable data={topRefsQ.data} /> : null}
            </div>
          </div>
        </div>
      )}

      {tab === 'pages' && (
        <div className="card">
          <h2 className="font-semibold mb-4">Barcha sahifalar</h2>
          {topPagesQ.data ? <TopPagesTable data={topPagesQ.data} /> : null}
        </div>
      )}

      {tab === 'devices' && devicesQ.data && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="font-semibold mb-4">Qurilma turi</h2>
            <PieChart data={devicesQ.data.by_type} />
          </div>
          <div className="card">
            <h2 className="font-semibold mb-4">Brauzerlar</h2>
            <PieChart data={devicesQ.data.by_browser} />
          </div>
          <div className="card">
            <h2 className="font-semibold mb-4">Operatsion tizimlar</h2>
            <BarChart data={devicesQ.data.by_os} />
          </div>
          <div className="card">
            <h2 className="font-semibold mb-4">Qurilmalar</h2>
            <BarChart data={devicesQ.data.by_device} />
          </div>
        </div>
      )}

      {tab === 'geo' && geoQ.data && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="font-semibold mb-4">Mamlakatlar</h2>
            <GeoTable data={geoQ.data} />
          </div>
          <div className="card">
            <h2 className="font-semibold mb-4">Shaharlar</h2>
            {geoQ.data.by_city.length === 0 ? (
              <div className="text-sm text-gray-400 text-center py-8">Ma'lumot yo'q</div>
            ) : (
              <div className="space-y-1">
                {geoQ.data.by_city.slice(0, 15).map((c) => (
                  <div key={`${c.country}-${c.name}`} className="flex justify-between px-3 py-1.5 text-sm">
                    <span>{c.name}</span>
                    <span className="text-gray-500">{formatNumber(c.visits)}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
