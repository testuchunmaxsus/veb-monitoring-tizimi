import fs from 'node:fs';
import path from 'node:path';
import { gzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distFile = path.join(__dirname, '..', 'dist', 'tracker.min.js');

if (!fs.existsSync(distFile)) {
  console.error('Build natijasi topilmadi:', distFile);
  process.exit(1);
}

const raw = fs.readFileSync(distFile);
const gz = gzipSync(raw);
const kb = (n) => (n / 1024).toFixed(2) + ' KB';

console.log('\n=== Tracker hajmi ===');
console.log(`Raw:     ${kb(raw.length)}`);
console.log(`Gzipped: ${kb(gz.length)}`);
console.log('Maqsad:  < 5 KB (gzipped)');
if (gz.length > 5 * 1024) {
  console.warn('OGOHLANTIRISH: 5 KB chegarasidan oshib ketdi!');
}
