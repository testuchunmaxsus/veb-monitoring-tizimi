import { useState, FormEvent } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { FileBarChart, Download, FileText, Plus, RefreshCw, FileSpreadsheet } from 'lucide-react';
import toast from 'react-hot-toast';
import { reportsApi } from '@/api/reports';
import { sitesApi } from '@/api/sites';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Modal } from '@/components/ui/Modal';
import { getDateRange } from '@/lib/format';

const STATUS_LABELS: Record<string, { text: string; color: string }> = {
  pending: { text: 'Kutilmoqda', color: 'bg-gray-100 text-gray-700' },
  processing: { text: 'Bajarilmoqda', color: 'bg-yellow-100 text-yellow-700' },
  done: { text: 'Tayyor', color: 'bg-green-100 text-green-700' },
  failed: { text: 'Xato', color: 'bg-red-100 text-red-700' },
};

export default function ReportsPage() {
  const qc = useQueryClient();
  const [createOpen, setCreateOpen] = useState(false);
  const defaultRange = getDateRange(7);
  const [form, setForm] = useState({
    site: 0,
    format: 'pdf' as 'pdf' | 'csv',
    date_from: defaultRange.from,
    date_to: defaultRange.to,
  });

  const reportsQ = useQuery({
    queryKey: ['reports'],
    queryFn: () => reportsApi.list(),
    refetchInterval: (query) => {
      const data = query.state.data as { results?: Array<{ status: string }> } | undefined;
      const hasPending = data?.results?.some(
        (r) => r.status === 'pending' || r.status === 'processing'
      );
      return hasPending ? 3000 : false;
    },
  });
  const sitesQ = useQuery({ queryKey: ['sites'], queryFn: () => sitesApi.list() });

  const createMut = useMutation({
    mutationFn: () => reportsApi.create(form),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['reports'] });
      setCreateOpen(false);
      toast.success('Hisobot generatsiyasi boshlandi');
    },
    onError: () => toast.error('Hisobot yaratilmadi'),
  });

  const handleDownload = async (id: number, format: string) => {
    try {
      const blob = await reportsApi.download(id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `hisobot_${id}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error('Yuklab olishda xato');
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!form.site) {
      toast.error('Sayt tanlang');
      return;
    }
    createMut.mutate();
  };

  const sites = sitesQ.data?.results || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Hisobotlar</h1>
          <p className="text-sm text-gray-500">PDF va CSV hisobotlarni yarating va yuklab oling</p>
        </div>
        <Button onClick={() => setCreateOpen(true)} disabled={sites.length === 0}>
          <Plus size={16} className="mr-1" /> Yangi hisobot
        </Button>
      </div>

      {sites.length === 0 && (
        <div className="card text-center py-12">
          <FileBarChart className="mx-auto text-gray-300 mb-3" size={40} />
          <p className="text-gray-500">Avval kamida bitta sayt qo'shing</p>
        </div>
      )}

      <div className="card">
        {reportsQ.isLoading && <div className="text-gray-500">Yuklanmoqda...</div>}
        {reportsQ.data && reportsQ.data.results.length === 0 && (
          <div className="text-center py-8 text-gray-400 text-sm">Hozircha hisobotlar yo'q</div>
        )}
        {reportsQ.data && reportsQ.data.results.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-xs text-gray-500 uppercase">
                  <th className="px-3 py-2">ID</th>
                  <th className="px-3 py-2">Sayt</th>
                  <th className="px-3 py-2">Davr</th>
                  <th className="px-3 py-2">Format</th>
                  <th className="px-3 py-2">Holat</th>
                  <th className="px-3 py-2">Yaratilgan</th>
                  <th className="px-3 py-2 text-right">Amallar</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {reportsQ.data.results.map((r) => {
                  const status = STATUS_LABELS[r.status];
                  return (
                    <tr key={r.id} className="hover:bg-gray-50">
                      <td className="px-3 py-2 text-gray-500">#{r.id}</td>
                      <td className="px-3 py-2 font-medium">{r.site_name}</td>
                      <td className="px-3 py-2 text-gray-600">
                        {r.date_from} → {r.date_to}
                      </td>
                      <td className="px-3 py-2">
                        <span className="inline-flex items-center gap-1">
                          {r.format === 'pdf' ? <FileText size={14} /> : <FileSpreadsheet size={14} />}
                          {r.format.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-3 py-2">
                        <span className={`inline-block px-2 py-0.5 rounded text-xs ${status.color}`}>
                          {(r.status === 'pending' || r.status === 'processing') && (
                            <RefreshCw size={10} className="inline mr-1 animate-spin" />
                          )}
                          {status.text}
                        </span>
                      </td>
                      <td className="px-3 py-2 text-gray-500 text-xs">
                        {new Date(r.created_at).toLocaleString('uz-UZ')}
                      </td>
                      <td className="px-3 py-2 text-right">
                        {r.status === 'done' ? (
                          <button
                            onClick={() => handleDownload(r.id, r.format)}
                            className="inline-flex items-center gap-1 text-brand-600 hover:text-brand-700 text-sm font-medium"
                          >
                            <Download size={14} /> Yuklab olish
                          </button>
                        ) : (
                          <span className="text-xs text-gray-400">—</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal open={createOpen} onClose={() => setCreateOpen(false)} title="Yangi hisobot">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Sayt</label>
            <select
              value={form.site}
              onChange={(e) => setForm({ ...form, site: Number(e.target.value) })}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
              required
            >
              <option value={0}>— tanlang —</option>
              {sites.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.domain})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Format</label>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setForm({ ...form, format: 'pdf' })}
                className={`flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg border text-sm ${
                  form.format === 'pdf'
                    ? 'border-brand-500 bg-brand-50 text-brand-700'
                    : 'border-gray-300 text-gray-700'
                }`}
              >
                <FileText size={14} /> PDF
              </button>
              <button
                type="button"
                onClick={() => setForm({ ...form, format: 'csv' })}
                className={`flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg border text-sm ${
                  form.format === 'csv'
                    ? 'border-brand-500 bg-brand-50 text-brand-700'
                    : 'border-gray-300 text-gray-700'
                }`}
              >
                <FileSpreadsheet size={14} /> CSV
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Input
              type="date"
              label="Boshi"
              value={form.date_from}
              onChange={(e) => setForm({ ...form, date_from: e.target.value })}
              required
            />
            <Input
              type="date"
              label="Oxiri"
              value={form.date_to}
              onChange={(e) => setForm({ ...form, date_to: e.target.value })}
              required
            />
          </div>

          <div className="flex gap-2 justify-end pt-2">
            <Button type="button" variant="secondary" onClick={() => setCreateOpen(false)}>
              Bekor qilish
            </Button>
            <Button type="submit" loading={createMut.isPending}>
              Yaratish
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
