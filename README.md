# Cantinho da Alegria

Landing page local em React e Vite. O conteúdo, a navegação, os cartões e os botões são componentes HTML reais; as ilustrações são PNGs individuais em `public/assets/elementos`.

## Executar

```bash
npm install
npm run dev
```

O servidor de desenvolvimento abre em `http://127.0.0.1:5173/`. Para conferir a versão compilada:

```bash
npm run build
npm run preview
```

A prévia compilada abre em `http://127.0.0.1:4173/`.

## Arquivos principais

- `src/App.jsx`: componentes e conteúdo da página.
- `src/styles.css`: layout responsivo, decoração e interações.
- `public/assets/elementos`: ilustrações separadas em PNG.
- `scripts/usar-imagens-originais.py`: recupera as ilustrações incorporadas no SVG de referência e monta `elementos-png.zip`.
- `scripts/gerar-detalhes.py`: gera o céu atrás do menu e a curva amarela do hero em PNG.

Nenhum SVG é servido pela página. O botão rosa mantém seu efeito de hover.
