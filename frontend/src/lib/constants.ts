export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
export const STORAGE_KEYS = {
  ACCESS: 'vmt_access',
  REFRESH: 'vmt_refresh',
} as const;
