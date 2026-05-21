import { ReactNode } from 'react';
import clsx from 'clsx';

interface Props {
  label: string;
  value: string | number;
  delta?: number;
  icon: ReactNode;
  hint?: string;
}

export function MetricCard({ label, value, delta, icon, hint }: Props) {
  const deltaPositive = delta !== undefined && delta >= 0;
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <div className="text-sm text-gray-500">{label}</div>
        <div className="p-2 bg-brand-50 rounded-lg text-brand-600">{icon}</div>
      </div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="flex items-center justify-between mt-1">
        {hint && <span className="text-xs text-gray-400">{hint}</span>}
        {delta !== undefined && (
          <span
            className={clsx(
              'text-xs font-medium',
              deltaPositive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {deltaPositive ? '↑' : '↓'} {Math.abs(delta).toFixed(1)}%
          </span>
        )}
      </div>
    </div>
  );
}
