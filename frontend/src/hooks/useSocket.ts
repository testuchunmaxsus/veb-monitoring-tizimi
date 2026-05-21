import { useEffect, useRef, useState } from 'react';
import { WS_URL, STORAGE_KEYS } from '@/lib/constants';

export interface SocketMessage<T = unknown> {
  type: string;
  data: T;
}

interface UseSocketOptions {
  siteId: number | null;
  onMessage?: (msg: SocketMessage) => void;
  enabled?: boolean;
}

export function useSocket({ siteId, onMessage, enabled = true }: UseSocketOptions) {
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const handlerRef = useRef(onMessage);

  useEffect(() => {
    handlerRef.current = onMessage;
  }, [onMessage]);

  useEffect(() => {
    if (!enabled || !siteId) return;

    const access = localStorage.getItem(STORAGE_KEYS.ACCESS);
    if (!access) return;

    const url = `${WS_URL}/site/${siteId}/?token=${encodeURIComponent(access)}`;
    let reconnectTimer: number | null = null;
    let stopped = false;

    const connect = () => {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => setConnected(true);
      ws.onclose = () => {
        setConnected(false);
        if (!stopped) {
          reconnectTimer = window.setTimeout(connect, 3000);
        }
      };
      ws.onerror = () => {
        try { ws.close(); } catch { /* ignore */ }
      };
      ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data) as SocketMessage;
          handlerRef.current?.(msg);
        } catch { /* ignore */ }
      };
    };

    connect();

    return () => {
      stopped = true;
      if (reconnectTimer) window.clearTimeout(reconnectTimer);
      try { wsRef.current?.close(); } catch { /* ignore */ }
    };
  }, [siteId, enabled]);

  return { connected };
}
