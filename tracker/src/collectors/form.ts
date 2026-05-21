/** Form yuborish hodisalarini yig'ish (qiymatlar tarqatilmaydi). */

import { selectorOf } from './click';

export function attachFormListener(handler: (target: string, fieldCount: number) => void) {
  const onSubmit = (e: Event) => {
    const form = e.target as HTMLFormElement | null;
    if (!form || form.tagName !== 'FORM') return;
    const fields = form.querySelectorAll('input, textarea, select').length;
    handler(selectorOf(form), fields);
  };
  document.addEventListener('submit', onSubmit, { capture: true, passive: true });
  return () => document.removeEventListener('submit', onSubmit, true);
}
