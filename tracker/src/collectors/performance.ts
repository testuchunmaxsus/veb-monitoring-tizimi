/** Performance metrikalari yig'ish (LCP, FCP, TTFB, load time). */

export interface PerfMetrics {
  load_time_ms?: number;
  lcp_ms?: number;
  fcp_ms?: number;
  ttfb_ms?: number;
}

export function collectPerf(): Promise<PerfMetrics> {
  return new Promise((resolve) => {
    const metrics: PerfMetrics = {};

    // Navigation timing (TTFB, load time)
    const nav = (performance.getEntriesByType('navigation')[0] || null) as PerformanceNavigationTiming | null;
    if (nav) {
      metrics.ttfb_ms = Math.round(nav.responseStart);
      if (nav.loadEventEnd > 0) {
        metrics.load_time_ms = Math.round(nav.loadEventEnd);
      }
    }

    // Paint metrics (FCP)
    try {
      const paints = performance.getEntriesByType('paint');
      paints.forEach((p) => {
        if (p.name === 'first-contentful-paint') {
          metrics.fcp_ms = Math.round(p.startTime);
        }
      });
    } catch { /* ignore */ }

    // LCP (PerformanceObserver)
    try {
      if ('PerformanceObserver' in window) {
        const obs = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const last = entries[entries.length - 1];
          if (last) metrics.lcp_ms = Math.round(last.startTime);
        });
        obs.observe({ type: 'largest-contentful-paint', buffered: true });

        // 3 soniyadan keyin yakunlaymiz
        setTimeout(() => {
          try { obs.disconnect(); } catch {}
          resolve(metrics);
        }, 3000);
        return;
      }
    } catch { /* ignore */ }

    resolve(metrics);
  });
}
