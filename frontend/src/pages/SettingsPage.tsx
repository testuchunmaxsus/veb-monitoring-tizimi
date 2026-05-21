import { useQuery } from '@tanstack/react-query';
import { User, Mail, Calendar, Shield } from 'lucide-react';
import { authApi } from '@/api/auth';

export default function SettingsPage() {
  const meQ = useQuery({ queryKey: ['me'], queryFn: () => authApi.me() });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Sozlamalar</h1>
        <p className="text-sm text-gray-500">Profilingiz va sozlamalar</p>
      </div>

      <div className="card max-w-2xl">
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <User size={18} /> Profil ma'lumotlari
        </h2>
        {meQ.isLoading && <div className="text-gray-500">Yuklanmoqda...</div>}
        {meQ.data && (
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3 py-2 border-b">
              <User size={16} className="text-gray-400" />
              <div className="flex-1">
                <div className="text-xs text-gray-500">To'liq ism</div>
                <div className="font-medium">{meQ.data.full_name || '—'}</div>
              </div>
            </div>
            <div className="flex items-center gap-3 py-2 border-b">
              <Mail size={16} className="text-gray-400" />
              <div className="flex-1">
                <div className="text-xs text-gray-500">Email</div>
                <div className="font-medium">{meQ.data.email}</div>
              </div>
            </div>
            <div className="flex items-center gap-3 py-2 border-b">
              <Calendar size={16} className="text-gray-400" />
              <div className="flex-1">
                <div className="text-xs text-gray-500">Ro'yxatdan o'tgan</div>
                <div className="font-medium">
                  {new Date(meQ.data.date_joined).toLocaleDateString('uz-UZ', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="card max-w-2xl">
        <h2 className="font-semibold mb-3 flex items-center gap-2">
          <Shield size={18} /> Xavfsizlik
        </h2>
        <p className="text-sm text-gray-600">
          Parolni o'zgartirish va boshqa xavfsizlik sozlamalari kelgusi versiyalarda qo'shiladi.
        </p>
      </div>

      <div className="card max-w-2xl">
        <h2 className="font-semibold mb-3">Tizim haqida</h2>
        <dl className="text-sm space-y-2">
          <div className="flex justify-between">
            <dt className="text-gray-500">Versiya</dt>
            <dd className="font-medium">1.0.0</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-gray-500">Backend</dt>
            <dd className="font-medium">Django 5.0 + Channels</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-gray-500">Frontend</dt>
            <dd className="font-medium">React 18 + Vite</dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
