import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Activity, Users, Globe, Smartphone, Monitor } from 'lucide-react';
import clsx from 'clsx';
import { sitesApi } from '@/api/sites';
import { useSocket, SocketMessage } from '@/hooks/useSocket';

interface FeedItem {
  id: number;
  type: string;
  url?: string;
  title?: string;
  country?: string;
  browser?: string;
  is_mobile?: boolean;
  target?: string;
  timestamp: string;
}

const MAX_FEED = 50;

export default function RealtimePage() {
  const sitesQ = useQuery({ queryKey: ['sites'], queryFn: () => sitesApi.list() });
  const sites = sitesQ.data?.results || [];
  const [siteId, setSiteId] = useState<number | null>(null);
  const [online, setOnline] = useState(0);
  const [feed, setFeed] = useState<FeedItem[]>([]);
  const idCounter = useMemo(() => ({ v: 0 }), []);

  // Default selectsiya
  if (sites.length > 0 && siteId === null) {
    setSiteId(sites[0].id);
  }

  const { connected } = useSocket({
    siteId,
    onMessage: (msg: SocketMessage) => {
      if (msg.type === 'presence') {
        setOnline((msg.data as { online: number }).online);
      } else if (msg.type === 'pageview' || msg.type === 'event') {
        idCounter.v += 1;
        const item: FeedItem = {
          id: idCounter.v,
          type: msg.type,
          ...(msg.data as Record<string, unknown>),
        } as FeedItem;
        setFeed((prev) => [item, ...prev].slice(0, MAX_FEED));
      }
    },
  });

  const onSiteChange = (id: number) => {
    setSiteId(id);
    setFeed([]);
    setOnline(0);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <span
              className={clsx('inline-block w-2.5 h-2.5 rounded-full', connected ? 'bg-green-500 animate-pulse' : 'bg-gray-300')}
            />
            Real-time
          </h1>
          <p className="text-sm text-gray-500">Saytdagi jonli oqim</p>
        </div>
        {sites.length > 0 && (
          <select
            value={siteId ?? ''}
            onChange={(e) => onSiteChange(Number(e.target.value))}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            {sites.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.domain})
              </option>
            ))}
          </select>
        )}
      </div>

      {sites.length === 0 && (
        <div className="card text-center py-12">
          <Activity className="mx-auto text-gray-300 mb-3" size={40} />
          <p className="text-gray-500">Saytlar yo'q. Avval sayt qo'shing.</p>
        </div>
      )}

      {sites.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="card text-center">
            <div className="flex items-center justify-center gap-2 text-gray-500 text-sm mb-2">
              <Users size={16} /> Hozir onlayn
            </div>
            <div className="text-5xl font-bold text-brand-600">{online}</div>
            <div className="text-xs text-gray-400 mt-2">
              {connected ? 'Ulangan' : 'Ulanish kutilmoqda...'}
            </div>
          </div>

          <div className="card lg:col-span-2">
            <h2 className="font-semibold mb-3 flex items-center gap-2">
              <Activity size={16} /> Voqealar oqimi
              <span className="text-xs text-gray-400 font-normal">(oxirgi {MAX_FEED} ta)</span>
            </h2>
            {feed.length === 0 ? (
              <div className="text-sm text-gray-400 text-center py-12">
                Hodisalarni kutish... Saytingizga kimdir kirsa shu yerda ko'rinadi.
              </div>
            ) : (
              <div className="divide-y max-h-[500px] overflow-y-auto">
                {feed.map((item) => (
                  <div key={item.id} className="flex items-start gap-3 py-2 text-sm">
                    <div
                      className={clsx(
                        'mt-1 w-2 h-2 rounded-full flex-shrink-0',
                        item.type === 'pageview' ? 'bg-brand-500' : 'bg-green-500'
                      )}
                    />
                    <div className="flex-1 min-w-0">
                      {item.type === 'pageview' && (
                        <>
                          <div className="font-medium truncate">{item.title || item.url}</div>
                          <div className="text-xs text-gray-500 truncate">{item.url}</div>
                        </>
                      )}
                      {item.type === 'event' && (
                        <div className="font-medium">
                          Hodisa: <span className="text-gray-600">{item.target}</span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-2 text-xs text-gray-400 flex-shrink-0">
                      {item.country && (
                        <span className="inline-flex items-center gap-1">
                          <Globe size={10} /> {item.country}
                        </span>
                      )}
                      {item.is_mobile !== undefined && (
                        item.is_mobile ? <Smartphone size={10} /> : <Monitor size={10} />
                      )}
                      {item.browser && <span>{item.browser}</span>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
