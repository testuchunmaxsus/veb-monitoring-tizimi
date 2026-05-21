import { TopReferrer } from '@/api/analytics';
import { formatNumber } from '@/lib/format';

interface Props {
  data: TopReferrer[];
}

export function TopReferrersTable({ data }: Props) {
  if (data.length === 0) {
    return <div className="text-sm text-gray-400 text-center py-8">Ma'lumot yo'q</div>;
  }
  const max = Math.max(...data.map((p) => p.visits), 1);
  return (
    <div className="space-y-2">
      {data.map((r) => (
        <div key={r.referrer} className="relative">
          <div
            className="absolute inset-y-0 left-0 bg-green-50 rounded"
            style={{ width: `${(r.visits / max) * 100}%` }}
          />
          <div className="relative flex items-center justify-between px-3 py-2">
            <div className="text-sm font-medium truncate">
              {r.referrer === 'direct' ? '(to\'g\'ridan-to\'g\'ri)' : r.referrer}
            </div>
            <div className="ml-4 text-sm font-semibold text-gray-700">
              {formatNumber(r.visits)}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
