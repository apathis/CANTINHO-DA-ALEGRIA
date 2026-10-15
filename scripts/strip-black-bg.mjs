import sharp from 'sharp';
import { copyFile, access, unlink, rename } from 'node:fs/promises';
import { join } from 'node:path';

const assets = join(process.cwd(), 'dist', 'assets');
const files = [
  'post-it-alegria.png',
  'doodles-grupo.png',
  'sol.png',
  'nuvem.png',
  'coracao.png',
  'estrela.png',
  'menina-convite.png',
  'ilustracao-cantinho.png',
];

const threshold = 42;

for (const file of files) {
  const input = join(assets, file);
  try {
    await access(input);
  } catch {
    console.warn('skip missing', file);
    continue;
  }

  const backup = `${input}.bak`;
  try {
    await access(backup);
  } catch {
    await copyFile(input, backup);
  }

  const { data, info } = await sharp(input).ensureAlpha().raw().toBuffer({ resolveWithObject: true });

  for (let i = 0; i < data.length; i += 4) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    if (r <= threshold && g <= threshold && b <= threshold) {
      data[i + 3] = 0;
    }
  }

  const output = join(assets, file.replace(/\.(png|jpg|jpeg)$/i, '-alpha.png'));
  await sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } })
    .png()
    .toFile(output);
  console.log('ok', file, '->', output.split(/[/\\]/).pop(), `${info.width}x${info.height}`);
}
