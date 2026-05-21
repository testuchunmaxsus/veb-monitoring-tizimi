import { TopPage } from '@/api/analytics';
import { formatNumber } from '@/lib/format';

interface Props {
  data: TopPage[];
}

export function TopPagesTable({ data }: Props) {
  if (data.length === 0) {
    return <div className="text-sm text-gray-400 text-center py-8">Ma'lumot yo'q</div>;
  }
  const max = Math.max(...data.map((p) => p.views), 1);
  return (
    <div className="space-y-2">
      {data.map((p) => (
        <div key={p.url} className="relative">
          <div
            className="absolute inset-y-0 left-0 bg-brand-50 rounded"
            style={{ width: `${(p.views / max) * 100}%` }}
          />
          <div className="relative flex items-center justify-between px-3 py-2">
            <div className="min-w-0 flex-1">
              <div className="text-sm font-medium truncate">{p.title || p.url}</div>
              <div className="text-xs text-gray-500 truncate">{p.url}</div>
            </div>
            <div className="ml-4 text-sm font-semibold text-gray-700">
              {formatNumber(p.views)}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
