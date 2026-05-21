import { uuid } from '../utils/uuid';

const STORAGE_KEY = 'vmt_sid';
const TIMEOUT_KEY = 'vmt_sid_t';
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 daqiqa

export function getSessionId(): string {
  try {
    const now = Date.now();
    const lastTouch = parseInt(sessionStorage.getItem(TIMEOUT_KEY) || '0', 10);
    let id = sessionStorage.getItem(STORAGE_KEY);
    if (!id || now - lastTouch > SESSION_TIMEOUT_MS) {
      id = uuid();
      sessionStorage.setItem(STORAGE_KEY, id);
    }
    sessionStorage.setItem(TIMEOUT_KEY, String(now));
    return id;
  } catch {
    return uuid();
  }
}

export function getSessionStart(): number {
  try {
    const k = 'vmt_sid_start';
    let v = sessionStorage.getItem(k);
    if (!v) {
      v = String(Date.now());
      sessionStorage.setItem(k, v);
    }
    return parseInt(v, 10);
  } catch {
    return Date.now();
  }
}
