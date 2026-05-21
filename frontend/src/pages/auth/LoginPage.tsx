import { useState, FormEvent } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/store/auth';

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuth((s) => s.login);
  const isLoading = useAuth((s) => s.isLoading);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const from = (location.state as { from?: string })?.from || '/dashboard';

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login({ email, password });
      toast.success('Xush kelibsiz!');
      navigate(from, { replace: true });
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Kirish muvaffaqiyatsiz tugadi';
      setError(msg);
      toast.error(msg);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-brand-50 to-gray-100">
      <div className="w-full max-w-md card">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-brand-700">Tizimga kirish</h1>
          <p className="text-sm text-gray-500 mt-1">Email va parolingizni kiriting</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="email"
            name="email"
            label="Email"
            placeholder="user@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <Input
            type="password"
            name="password"
            label="Parol"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" className="w-full" loading={isLoading}>
            Kirish
          </Button>
        </form>
        <p className="mt-6 text-center text-sm text-gray-600">
          Akkauntingiz yo'qmi?{' '}
          <Link to="/register" className="font-medium text-brand-600 hover:text-brand-700">
            Ro'yxatdan o'tish
          </Link>
        </p>
      </div>
    </div>
  );
}
