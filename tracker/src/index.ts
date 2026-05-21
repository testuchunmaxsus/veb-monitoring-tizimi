/**
 * Veb-Monitoring Tracker
 *
 * Foydalanish:
 *   <script async src="/tracker.min.js"
 *           data-api-key="vmt_xxx"
 *           data-endpoint="http://localhost:8000/api/v1/track"></script>
 */
import { Tracker } from './core/tracker';

declare global {
  interface Window {
    __vmtTracker?: Tracker;
  }
}

function readConfig() {
  // currentScript ba'zan null bo'ladi (eski brauzer / async chain)
  let script = document.currentScript as HTMLScriptElement | null;
  if (!script) {
    const scripts = document.getElementsByTagName('script');
    for (let i = scripts.length - 1; i >= 0; i--) {
      if (scripts[i].dataset.apiKey) {
        script = scripts[i];
        break;
      }
    }
  }
  if (!script) return null;
  const apiKey = script.dataset.apiKey;
  const endpoint = (script.dataset.endpoint || '').replace(/\/$/, '');
  if (!apiKey || !endpoint) return null;
  return { apiKey, endpoint };
}

function init() {
  if (window.__vmtTracker) return;
  const cfg = readConfig();
  if (!cfg) {
    if (typeof console !== 'undefined') console.warn('[VMT] data-api-key/data-endpoint kerak');
    return;
  }
  const tracker = new Tracker(cfg);
  window.__vmtTracker = tracker;
  tracker.start();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}
