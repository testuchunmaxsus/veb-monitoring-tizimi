import { ReactNode, useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/store/auth';
import { STORAGE_KEYS } from '@/lib/constants';

interface Props {
  children: ReactNode;
}

export function ProtectedRoute({ children }: Props) {
  const location = useLocation();
  const { isAuthenticated, loadProfile } = useAuth();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const access = localStorage.getItem(STORAGE_KEYS.ACCESS);
    if (access && !isAuthenticated) {
      loadProfile().finally(() => setChecked(true));
    } else {
      setChecked(true);
    }
  }, [isAuthenticated, loadProfile]);

  if (!checked) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-500">Yuklanmoqda...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  return <>{children}</>;
}
