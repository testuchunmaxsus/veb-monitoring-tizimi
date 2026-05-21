import { useState, FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/store/auth';

export default function RegisterPage() {
  const navigate = useNavigate();
  const register = useAuth((s) => s.register);
  const isLoading = useAuth((s) => s.isLoading);
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrors({});
    try {
      await register(form);
      toast.success('Hisob yaratildi!');
      navigate('/dashboard', { replace: true });
    } catch (err: any) {
      const data = err.response?.data || {};
      const newErrors: Record<string, string> = {};
      Object.entries(data).forEach(([key, value]) => {
        newErrors[key] = Array.isArray(value) ? value[0] : String(value);
      });
      setErrors(newErrors);
      toast.error('Ro\'yxatdan o\'tish muvaffaqiyatsiz');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-brand-50 to-gray-100">
      <div className="w-full max-w-md card">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-brand-700">Ro'yxatdan o'tish</h1>
          <p className="text-sm text-gray-500 mt-1">Yangi hisob yarating</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="To'liq ism"
            name="full_name"
            placeholder="Ismoilov Javohir"
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            required
            error={errors.full_name}
          />
          <Input
            type="email"
            name="email"
            label="Email"
            placeholder="user@example.com"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
            autoComplete="email"
            error={errors.email}
          />
          <Input
            type="password"
            name="password"
            label="Parol (kamida 8 belgi)"
            placeholder="••••••••"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
            minLength={8}
            autoComplete="new-password"
            error={errors.password}
          />
          <Button type="submit" className="w-full" loading={isLoading}>
            Ro'yxatdan o'tish
          </Button>
        </form>
        <p className="mt-6 text-center text-sm text-gray-600">
          Akkauntingiz bormi?{' '}
          <Link to="/login" className="font-medium text-brand-600 hover:text-brand-700">
            Kirish
          </Link>
        </p>
      </div>
    </div>
  );
}
