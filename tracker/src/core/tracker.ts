/** Tracker asosiy klassi. */
import { attachClickListener } from '../collectors/click';
import { attachFormListener } from '../collectors/form';
import { collectPerf } from '../collectors/performance';
import { getSessionId, getSessionStart } from './session';
import { sendBeaconJson, sendFetch } from './transport';

export interface TrackerConfig {
  apiKey: string;
  endpoint: string; // bazaviy URL: http://host/api/v1/track
}

export class Tracker {
  private cfg: TrackerConfig;
  private detachers: Array<() => void> = [];
  private currentUrl: string;

  constructor(cfg: TrackerConfig) {
    this.cfg = cfg;
    this.currentUrl = location.href;
  }

  start() {
    this.sendPageView();
    this.detachers.push(
      attachClickListener((target, x, y) => this.sendEvent('click', target, { x, y })),
    );
    this.detachers.push(
      attachFormListener((target, fields) => this.sendEvent('form', target, { fields })),
    );
    this.attachUrlChangeListener();
    this.attachUnloadListener();
  }

  /** SPA navigatsiyasini kuzatish (history API). */
  private attachUrlChangeListener() {
    const fire = () => {
      if (location.href !== this.currentUrl) {
        this.currentUrl = location.href;
        this.sendPageView();
      }
    };
    const origPush = history.pushState;
    const origReplace = history.replaceState;
    history.pushState = function (...args) {
      const r = origPush.apply(this, args);
      window.dispatchEvent(new Event('vmt:locationchange'));
      return r;
    };
    history.replaceState = function (...args) {
      const r = origReplace.apply(this, args);
      window.dispatchEvent(new Event('vmt:locationchange'));
      return r;
    };
    window.addEventListener('vmt:locationchange', fire);
    window.addEventListener('popstate', fire);
  }

  /** Sahifa yopilganda sessiyani yakunlash. */
  private attachUnloadListener() {
    const onLeave = () => {
      const duration = Math.round((Date.now() - getSessionStart()) / 1000);
      sendBeaconJson(this.url('session/end/'), {
        api_key: this.cfg.apiKey,
        session_uid: getSessionId(),
        duration_sec: duration,
      });
    };
    window.addEventListener('pagehide', onLeave);
    window.addEventListener('beforeunload', onLeave);
  }

  private url(path: string) {
    return `${this.cfg.endpoint}/${path.replace(/^\//, '')}`;
  }

  private async sendPageView() {
    const perf = await collectPerf();
    sendFetch(this.url('pageview/'), {
      api_key: this.cfg.apiKey,
      session_uid: getSessionId(),
      url: location.href,
      title: document.title.slice(0, 500),
      referrer: document.referrer.slice(0, 500),
      ...perf,
    });
  }

  private sendEvent(type: string, target: string, metadata: Record<string, unknown>) {
    sendFetch(this.url('event/'), {
      api_key: this.cfg.apiKey,
      session_uid: getSessionId(),
      type,
      target,
      metadata,
    });
  }

  stop() {
    this.detachers.forEach((d) => d());
    this.detachers = [];
  }
}
