import {
  Bar,
  BarChart as RBarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { formatNumber } from '@/lib/format';

interface Props {
  data: Array<{ name: string; count: number }>;
  height?: number;
  color?: string;
  layout?: 'vertical' | 'horizontal';
}

export function BarChart({ data, height = 300, color = '#2563eb', layout = 'horizontal' }: Props) {
  const isVertical = layout === 'vertical';
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RBarChart
        data={data}
        layout={layout}
        margin={{ top: 10, right: 20, left: isVertical ? 100 : 0, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        {isVertical ? (
          <>
            <XAxis type="number" stroke="#6b7280" fontSize={12} tickFormatter={formatNumber} />
            <YAxis type="category" dataKey="name" stroke="#6b7280" fontSize={12} width={100} />
          </>
        ) : (
          <>
            <XAxis dataKey="name" stroke="#6b7280" fontSize={12} />
            <YAxis stroke="#6b7280" fontSize={12} tickFormatter={formatNumber} />
          </>
        )}
        <Tooltip
          formatter={(v: number) => [formatNumber(v), 'Soni']}
          contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb' }}
        />
        <Bar dataKey="count" fill={color} radius={[4, 4, 0, 0]} />
      </RBarChart>
    </ResponsiveContainer>
  );
}
