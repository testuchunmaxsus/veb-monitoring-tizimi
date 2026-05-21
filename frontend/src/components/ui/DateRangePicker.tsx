import { useState } from 'react';
import clsx from 'clsx';
import { getDateRange } from '@/lib/format';

export type DateRange = { from: string; to: string };

interface Props {
  value: DateRange;
  onChange: (range: DateRange) => void;
}

const PRESETS: Array<{ label: string; days: number }> = [
  { label: 'Bugun', days: 1 },
  { label: '7 kun', days: 7 },
  { label: '30 kun', days: 30 },
  { label: '90 kun', days: 90 },
];

export function DateRangePicker({ value, onChange }: Props) {
  const [activeDays, setActiveDays] = useState(7);

  const select = (days: number) => {
    setActiveDays(days);
    onChange(getDateRange(days));
  };

  return (
    <div className="inline-flex items-center gap-1 bg-white rounded-lg border border-gray-200 p-1">
      {PRESETS.map((p) => (
        <button
          key={p.days}
          onClick={() => select(p.days)}
          className={clsx(
            'px-3 py-1 text-sm rounded transition-colors',
            activeDays === p.days
              ? 'bg-brand-100 text-brand-700 font-medium'
              : 'text-gray-600 hover:bg-gray-50'
          )}
        >
          {p.label}
        </button>
      ))}
      <div className="hidden sm:block text-xs text-gray-400 ml-2 mr-1">
        {value.from} → {value.to}
      </div>
    </div>
  );
}
