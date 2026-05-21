import { useQuery, useQueries } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Eye, Users, Activity, Clock, Globe, ArrowRight } from 'lucide-react';
import { useState } from 'react';
import { sitesApi } from '@/api/sites';
import { analyticsApi } from '@/api/analytics';
import { MetricCard } from '@/components/charts/MetricCard';
import { DateRangePicker, DateRange } from '@/components/ui/DateRangePicker';
import { formatDuration, formatNumber, formatPercent, getDateRange } from '@/lib/format';

export default function DashboardPage() {
  const [range, setRange] = useState<DateRange>(getDateRange(7));

  const sitesQ = useQuery({ queryKey: ['sites'], queryFn: () => sitesApi.list() });
  const sites = sitesQ.data?.results || [];

  const overviewQs = useQueries({
    queries: sites.map((s) => ({
      queryKey: ['overview', s.id, range],
      queryFn: () => analyticsApi.overview(s.id, range),
      enabled: !!s.id,
    })),
  });

  const totals = overviewQs.reduce(
    (acc, q) => {
      if (q.data) {
        acc.pageviews += q.data.total_pageviews;
        acc.visitors += q.data.unique_visitors;
        acc.sessions += q.data.total_sessions;
        acc.bounceSum += q.data.bounce_rate * q.data.total_sessions;
        acc.durationSum += q.data.avg_session_duration_sec * q.data.total_sessions;
      }
      return acc;
    },
    { pageviews: 0, visitors: 0, sessions: 0, bounceSum: 0, durationSum: 0 }
  );

  const bounceRate = totals.sessions ? totals.bounceSum / totals.sessions : 0;
  const avgDuration = totals.sessions ? Math.round(totals.durationSum / totals.sessions) : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-sm text-gray-500">Barcha saytlaringiz bo'yicha umumiy ko'rsatkichlar</p>
        </div>
        <DateRangePicker value={range} onChange={setRange} />
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Sahifa ko'rishlari" value={formatNumber(totals.pageviews)} icon={<Eye size={18} />} />
        <MetricCard label="Tashrif buyuruvchilar" value={formatNumber(totals.visitors)} icon={<Users size={18} />} />
        <MetricCard label="Sessiyalar" value={formatNumber(totals.sessions)} icon={<Activity size={18} />} />
        <MetricCard
          label="O'rtacha vaqt"
          value={formatDuration(avgDuration)}
          hint={`Bounce: ${formatPercent(bounceRate)}`}
          icon={<Clock size={18} />}
        />
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold">Saytlar</h2>
          <Link to="/sites" className="text-sm text-brand-600 hover:text-brand-700">
            Barchasi →
          </Link>
        </div>

        {sites.length === 0 ? (
          <div className="text-center py-12">
            <Globe className="mx-auto text-gray-300 mb-3" size={40} />
            <p className="text-gray-500 mb-3">Saytlar yo'q</p>
            <Link to="/sites" className="btn-primary">
              Birinchi saytni qo'shish
            </Link>
          </div>
        ) : (
          <div className="divide-y">
            {sites.map((s, idx) => {
              const ov = overviewQs[idx]?.data;
              return (
                <Link
                  key={s.id}
                  to={`/sites/${s.id}`}
                  className="flex items-center justify-between py-3 hover:bg-gray-50 -mx-3 px-3 rounded transition-colors"
                >
                  <div className="min-w-0 flex-1">
                    <div className="font-medium truncate">{s.name}</div>
                    <div className="text-xs text-gray-500 truncate">{s.domain}</div>
                  </div>
                  <div className="flex items-center gap-6 ml-4">
                    <div className="text-right hidden sm:block">
                      <div className="text-xs text-gray-500">Ko'rishlar</div>
                      <div className="text-sm font-semibold">
                        {ov ? formatNumber(ov.total_pageviews) : '—'}
                      </div>
                    </div>
                    <div className="text-right hidden md:block">
                      <div className="text-xs text-gray-500">Tashriflar</div>
                      <div className="text-sm font-semibold">
                        {ov ? formatNumber(ov.unique_visitors) : '—'}
                      </div>
                    </div>
                    <ArrowRight size={16} className="text-gray-400" />
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
