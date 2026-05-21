import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Bell, AlertTriangle, Info, CheckCircle, AlertCircle, Check } from 'lucide-react';
import clsx from 'clsx';
import toast from 'react-hot-toast';
import { notificationsApi, NotificationType } from '@/api/notifications';
import { Button } from '@/components/ui/Button';

const TYPE_META: Record<NotificationType, { icon: typeof Bell; color: string }> = {
  anomaly: { icon: AlertTriangle, color: 'text-red-500 bg-red-50' },
  warning: { icon: AlertCircle, color: 'text-yellow-600 bg-yellow-50' },
  info: { icon: Info, color: 'text-blue-500 bg-blue-50' },
  success: { icon: CheckCircle, color: 'text-green-500 bg-green-50' },
};

export default function NotificationsPage() {
  const qc = useQueryClient();
  const [unreadOnly, setUnreadOnly] = useState(false);

  const listQ = useQuery({
    queryKey: ['notifications', unreadOnly],
    queryFn: () => notificationsApi.list(unreadOnly),
  });

  const markReadMut = useMutation({
    mutationFn: (id: number) => notificationsApi.markRead(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['notifications'] });
      qc.invalidateQueries({ queryKey: ['unread-count'] });
    },
  });

  const markAllMut = useMutation({
    mutationFn: () => notificationsApi.markAllRead(),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['notifications'] });
      qc.invalidateQueries({ queryKey: ['unread-count'] });
      toast.success('Barchasi o\'qildi deb belgilandi');
    },
  });

  const items = listQ.data?.results || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold">Bildirishnomalar</h1>
          <p className="text-sm text-gray-500">Tizim xabarlari va anomaliyalar</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setUnreadOnly((v) => !v)}
            className={clsx(
              'px-3 py-1.5 rounded-lg text-sm border',
              unreadOnly ? 'border-brand-500 bg-brand-50 text-brand-700' : 'border-gray-300 text-gray-700'
            )}
          >
            Faqat o'qilmaganlar
          </button>
          <Button variant="secondary" onClick={() => markAllMut.mutate()} loading={markAllMut.isPending}>
            <Check size={14} className="mr-1" /> Barchasini o'qildi
          </Button>
        </div>
      </div>

      {listQ.isLoading && <div className="text-gray-500">Yuklanmoqda...</div>}

      {items.length === 0 && !listQ.isLoading && (
        <div className="card text-center py-16">
          <Bell className="mx-auto text-gray-300 mb-3" size={40} />
          <p className="text-gray-500">Bildirishnomalar yo'q</p>
        </div>
      )}

      <div className="space-y-2">
        {items.map((n) => {
          const meta = TYPE_META[n.type];
          const Icon = meta.icon;
          return (
            <div
              key={n.id}
              className={clsx(
                'card flex items-start gap-3 transition-colors',
                !n.is_read && 'ring-2 ring-brand-200'
              )}
            >
              <div className={clsx('p-2 rounded-lg flex-shrink-0', meta.color)}>
                <Icon size={18} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{n.title}</h3>
                  {!n.is_read && <span className="w-2 h-2 bg-brand-500 rounded-full" />}
                </div>
                <p className="text-sm text-gray-600 mt-1">{n.message}</p>
                <div className="flex items-center gap-3 text-xs text-gray-400 mt-2">
                  {n.site_name && <span>{n.site_name}</span>}
                  <span>{new Date(n.created_at).toLocaleString('uz-UZ')}</span>
                </div>
              </div>
              {!n.is_read && (
                <button
                  onClick={() => markReadMut.mutate(n.id)}
                  className="text-xs text-brand-600 hover:text-brand-700 font-medium flex-shrink-0"
                >
                  O'qildi
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
