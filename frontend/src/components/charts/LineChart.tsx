import {
  CartesianGrid,
  Line,
  LineChart as RLineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { formatDate, formatNumber } from '@/lib/format';
import { TimeseriesPoint } from '@/api/analytics';

interface Props {
  data: TimeseriesPoint[];
  height?: number;
  color?: string;
  label?: string;
}

export function LineChart({ data, height = 300, color = '#2563eb', label = 'Qiymat' }: Props) {
  const chartData = data.map((d) => ({ ...d, _label: formatDate(d.timestamp) }));
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RLineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="_label" stroke="#6b7280" fontSize={12} />
        <YAxis stroke="#6b7280" fontSize={12} tickFormatter={formatNumber} />
        <Tooltip
          formatter={(v: number) => [formatNumber(v), label]}
          contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb' }}
        />
        <Line
          type="monotone"
          dataKey="value"
          stroke={color}
          strokeWidth={2}
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
        />
      </RLineChart>
    </ResponsiveContainer>
  );
}
