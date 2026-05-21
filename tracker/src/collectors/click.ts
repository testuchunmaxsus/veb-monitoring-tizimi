/** Klik hodisalarini avtomatik yig'ish. */

const CLICKABLE_TAGS = ['A', 'BUTTON'];

export function selectorOf(el: Element): string {
  if (!el) return '';
  const id = el.id ? `#${el.id}` : '';
  const cls = (el.className || '')
    .toString()
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 3)
    .map((c) => `.${c}`)
    .join('');
  const tag = el.tagName.toLowerCase();
  return `${tag}${id}${cls}`.slice(0, 200);
}

export function attachClickListener(handler: (target: string, x: number, y: number) => void) {
  const onClick = (e: MouseEvent) => {
    const target = e.target as Element | null;
    if (!target) return;
    // Faqat clickable elementlar yoki data-vmt-track="true" bo'lganlar
    let el: Element | null = target;
    while (el && el !== document.body) {
      if (
        CLICKABLE_TAGS.includes(el.tagName) ||
        el.getAttribute?.('data-vmt-track') === 'true' ||
        el.getAttribute?.('role') === 'button'
      ) {
        handler(selectorOf(el), e.clientX, e.clientY);
        return;
      }
      el = el.parentElement;
    }
  };
  document.addEventListener('click', onClick, { capture: true, passive: true });
  return () => document.removeEventListener('click', onClick, true);
}
