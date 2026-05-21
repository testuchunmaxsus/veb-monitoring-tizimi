/** Transport: navigator.sendBeacon + fetch fallback. */

export function sendBeaconJson(url: string, payload: unknown): boolean {
  try {
    const data = JSON.stringify(payload);
    if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
      // Blob bilan jo'natamiz, server text/plain ham qabul qilishi kerak
      const blob = new Blob([data], { type: 'application/json' });
      const ok = navigator.sendBeacon(url, blob);
      if (ok) return true;
    }
  } catch { /* fallback */ }
  return sendFetch(url, payload);
}

export function sendFetch(url: string, payload: unknown): boolean {
  try {
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      keepalive: true,
      credentials: 'omit',
      mode: 'cors',
    }).catch(() => {});
    return true;
  } catch {
    return false;
  }
}
