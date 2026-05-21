import { GeoBreakdown } from '@/api/analytics';
import { formatNumber } from '@/lib/format';

interface Props {
  data: GeoBreakdown;
}

const flag = (code: string) => {
  if (!code || code.length !== 2) return '🌐';
  return code
    .toUpperCase()
    .split('')
    .map((c) => String.fromCodePoint(0x1f1e6 - 65 + c.charCodeAt(0)))
    .join('');
};

export function GeoTable({ data }: Props) {
  if (data.by_country.length === 0) {
    return <div className="text-sm text-gray-400 text-center py-8">Geo ma'lumot yo'q</div>;
  }
  const max = Math.max(...data.by_country.map((c) => c.visits), 1);
  return (
    <div className="space-y-2">
      {data.by_country.slice(0, 10).map((c) => (
        <div key={c.code} className="relative">
          <div
            className="absolute inset-y-0 left-0 bg-purple-50 rounded"
            style={{ width: `${(c.visits / max) * 100}%` }}
          />
          <div className="relative flex items-center justify-between px-3 py-2">
            <div className="flex items-center gap-2">
              <span className="text-lg">{flag(c.code)}</span>
              <span className="text-sm font-medium">{c.name}</span>
            </div>
            <div className="text-sm font-semibold text-gray-700">{formatNumber(c.visits)}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
