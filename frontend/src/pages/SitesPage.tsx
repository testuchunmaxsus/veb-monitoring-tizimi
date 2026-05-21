import { useState, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Code, Trash2, RefreshCw, Globe, BarChart3 } from 'lucide-react';
import toast from 'react-hot-toast';
import { sitesApi, Site } from '@/api/sites';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Modal } from '@/components/ui/Modal';

export default function SitesPage() {
  const qc = useQueryClient();
  const [createOpen, setCreateOpen] = useState(false);
  const [snippetSite, setSnippetSite] = useState<Site | null>(null);
  const [name, setName] = useState('');
  const [domain, setDomain] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['sites'],
    queryFn: () => sitesApi.list(),
  });

  const createMut = useMutation({
    mutationFn: () => sitesApi.create({ name, domain }),
    onSuccess: (site) => {
      qc.invalidateQueries({ queryKey: ['sites'] });
      setCreateOpen(false);
      setName('');
      setDomain('');
      toast.success('Sayt qo\'shildi');
      setSnippetSite(site);
    },
    onError: (err: any) => {
      const detail = err.response?.data?.domain?.[0] || err.response?.data?.detail || 'Xato yuz berdi';
      toast.error(detail);
    },
  });

  const deleteMut = useMutation({
    mutationFn: (id: number) => sitesApi.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['sites'] });
      toast.success('Sayt o\'chirildi');
    },
  });

  const regenMut = useMutation({
    mutationFn: (id: number) => sitesApi.regenerateApiKey(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['sites'] });
      toast.success('API kalit yangilandi');
    },
  });

  const handleCreate = (e: FormEvent) => {
    e.preventDefault();
    createMut.mutate();
  };

  const handleDelete = (site: Site) => {
    if (confirm(`"${site.name}" saytini o'chirishga ishonchingiz komilmi? Barcha statistika yo'qoladi.`)) {
      deleteMut.mutate(site.id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Saytlar</h1>
          <p className="text-sm text-gray-500">Kuzatilayotgan saytlaringizni boshqaring</p>
        </div>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus size={16} className="mr-1" /> Sayt qo'shish
        </Button>
      </div>

      {isLoading && <div className="text-gray-500">Yuklanmoqda...</div>}

      {data?.results.length === 0 && (
        <div className="card text-center py-16">
          <Globe className="mx-auto text-gray-300 mb-4" size={48} />
          <h3 className="text-lg font-medium">Saytlar yo'q</h3>
          <p className="text-sm text-gray-500 mb-4">Birinchi saytingizni qo'shish bilan boshlang</p>
          <Button onClick={() => setCreateOpen(true)}>
            <Plus size={16} className="mr-1" /> Sayt qo'shish
          </Button>
        </div>
      )}

      {data && data.results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.results.map((site) => (
            <div key={site.id} className="card">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{site.name}</h3>
                  <p className="text-sm text-gray-500">{site.domain}</p>
                </div>
                <span
                  className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                    site.is_active
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {site.is_active ? 'Faol' : 'O\'chirilgan'}
                </span>
              </div>

              <div className="text-xs font-mono bg-gray-50 px-2 py-1 rounded mb-3 truncate">
                {site.api_key}
              </div>

              <div className="flex gap-2 flex-wrap">
                <Link
                  to={`/sites/${site.id}`}
                  className="inline-flex items-center px-2 py-1 text-xs font-medium rounded-lg bg-brand-50 text-brand-700 hover:bg-brand-100 transition-colors"
                >
                  <BarChart3 size={12} className="mr-1" /> Statistika
                </Link>
                <Button variant="secondary" onClick={() => setSnippetSite(site)} className="!px-2 !py-1 !text-xs">
                  <Code size={12} className="mr-1" /> Kod
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => regenMut.mutate(site.id)}
                  className="!px-2 !py-1 !text-xs"
                  loading={regenMut.isPending && regenMut.variables === site.id}
                >
                  <RefreshCw size={12} className="mr-1" /> Yangilash
                </Button>
                <Button
                  variant="danger"
                  onClick={() => handleDelete(site)}
                  className="!px-2 !py-1 !text-xs"
                >
                  <Trash2 size={12} className="mr-1" /> O'chirish
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal open={createOpen} onClose={() => setCreateOpen(false)} title="Yangi sayt qo'shish">
        <form onSubmit={handleCreate} className="space-y-4">
          <Input
            label="Sayt nomi"
            placeholder="Mening blogim"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <Input
            label="Domen"
            placeholder="example.com"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            required
          />
          <div className="flex gap-2 justify-end">
            <Button type="button" variant="secondary" onClick={() => setCreateOpen(false)}>
              Bekor qilish
            </Button>
            <Button type="submit" loading={createMut.isPending}>
              Qo'shish
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        open={!!snippetSite}
        onClose={() => setSnippetSite(null)}
        title="Tracker kodini saytingizga qo'ying"
        maxWidth="xl"
      >
        {snippetSite && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              Quyidagi kodni saytingizning <code className="bg-gray-100 px-1 rounded">&lt;head&gt;</code> teglari ichiga
              joylashtiring:
            </p>
            <pre className="bg-gray-900 text-gray-100 text-xs p-4 rounded-lg overflow-x-auto">
{`<script
  async
  src="${window.location.protocol}//${window.location.host.replace('5173', '8000')}/static/tracker.min.js"
  data-api-key="${snippetSite.api_key}"
  data-endpoint="${window.location.protocol}//${window.location.host.replace('5173', '8000')}/api/v1/track">
</script>`}
            </pre>
            <Button
              variant="secondary"
              onClick={() => {
                const code = `<script async src="/static/tracker.min.js" data-api-key="${snippetSite.api_key}" data-endpoint="/api/v1/track"></script>`;
                navigator.clipboard.writeText(code);
                toast.success('Kod nusxalandi');
              }}
            >
              Nusxalash
            </Button>
          </div>
        )}
      </Modal>
    </div>
  );
}
