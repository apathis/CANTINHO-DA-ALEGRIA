import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
const root = join(process.cwd(), 'dist');
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.svg':'image/svg+xml', '.png':'image/png' };
createServer(async (req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  const path = normalize(join(root, pathname === '/' ? 'index.html' : pathname));
  if (!path.startsWith(root)) { res.writeHead(403); res.end(); return; }
  try { const data = await readFile(path); res.writeHead(200, { 'Content-Type': types[extname(path)] || 'application/octet-stream' }); res.end(data); }
  catch { res.writeHead(404); res.end(); }
}).listen(4173, '127.0.0.1', () => process.stdout.write('http://127.0.0.1:4173\n'));
