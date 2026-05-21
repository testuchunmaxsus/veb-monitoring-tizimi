import { Cell, Legend, Pie, PieChart as RPieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { formatNumber } from '@/lib/format';

interface Props {
  data: Array<{ name: string; count: number }>;
  height?: number;
}

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16'];

export function PieChart({ data, height = 300 }: Props) {
  const total = data.reduce((acc, d) => acc + d.count, 0) || 1;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RPieChart>
        <Pie
          data={data}
          dataKey="count"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={90}
          label={({ name, count }) => `${name}: ${((count / total) * 100).toFixed(0)}%`}
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(v: number) => formatNumber(v)} />
        <Legend />
      </RPieChart>
    </ResponsiveContainer>
  );
}
