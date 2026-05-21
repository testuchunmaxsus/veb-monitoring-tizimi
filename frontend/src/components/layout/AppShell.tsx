import { ReactNode } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { LayoutDashboard, Globe, FileBarChart, Bell, LogOut, Settings, Activity } from 'lucide-react';
import { useAuth } from '@/store/auth';
import { notificationsApi } from '@/api/notifications';

interface Props {
  children: ReactNode;
}

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, key: 'dashboard' },
  { to: '/sites', label: 'Saytlar', icon: Globe, key: 'sites' },
  { to: '/realtime', label: 'Real-time', icon: Activity, key: 'realtime' },
  { to: '/reports', label: 'Hisobotlar', icon: FileBarChart, key: 'reports' },
  { to: '/notifications', label: 'Bildirishnomalar', icon: Bell, key: 'notifications' },
  { to: '/settings', label: 'Sozlamalar', icon: Settings, key: 'settings' },
] as const;

export function AppShell({ children }: Props) {
  const navigate = useNavigate();
  const user = useAuth((s) => s.user);
  const logout = useAuth((s) => s.logout);

  const unreadQ = useQuery({
    queryKey: ['unread-count'],
    queryFn: () => notificationsApi.unreadCount(),
    refetchInterval: 30_000,
  });
  const unread = unreadQ.data ?? 0;

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-xl font-bold text-brand-700">Veb-Monitoring</h1>
          <p className="text-xs text-gray-500">Tizim</p>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-brand-50 text-brand-700' : 'text-gray-700 hover:bg-gray-50'
                }`
              }
            >
              <item.icon size={18} />
              <span className="flex-1">{item.label}</span>
              {item.key === 'notifications' && unread > 0 && (
                <span className="inline-flex items-center justify-center min-w-[20px] h-5 px-1.5 text-xs font-bold rounded-full bg-red-500 text-white">
                  {unread > 99 ? '99+' : unread}
                </span>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t">
          <div className="text-sm mb-2">
            <div className="font-medium truncate">{user?.full_name || 'Foydalanuvchi'}</div>
            <div className="text-xs text-gray-500 truncate">{user?.email}</div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <LogOut size={16} />
            Chiqish
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
}
