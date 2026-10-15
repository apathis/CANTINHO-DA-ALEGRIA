import React, { useState } from 'react';

const instagram = 'https://www.instagram.com/cantinhodaalegria.tiadeia/';
const whatsapp = 'https://wa.me/5511948434543';
const asset = (name) => `${import.meta.env.BASE_URL}assets/elementos/${name}.png`;

const links = [
  ['Sobre', '#sobre'],
  ['Nossos cuidados', '#cuidados'],
  ['Atividades', '#atividades'],
  ['Contato', '#contato'],
];

function Drawing({ name, className = '', alt = '' }) {
  return <img className={className} src={asset(name)} alt={alt} aria-hidden={alt ? undefined : 'true'} />;
}

function Brand({ footer = false }) {
  return (
    <a className={`brand ${footer ? 'footer-brand' : ''}`} href="#inicio" aria-label={footer ? 'Voltar ao início' : 'Cantinho da Alegria, início'}>
      <Drawing name="logo-desenho" />
      <span className="brand-words"><strong>CANTINHO<br />DA ALEGRIA</strong><small>Recreação &amp; Cuidados Infantis</small></span>
    </a>
  );
}

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <header className="topbar">
      <Brand />
      <nav className="topnav" aria-label="Navegação principal">
        {links.map(([label, href]) => <a key={href} href={href}>{label}</a>)}
      </nav>
      <div className="mobile-menu">
        <button className="menu-toggle" type="button" aria-label={menuOpen ? 'Fechar menu' : 'Abrir menu'} aria-expanded={menuOpen} onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? '×' : '☰'}</button>
        {menuOpen && <nav aria-label="Menu mobile">{links.map(([label, href]) => <a key={href} href={href} onClick={() => setMenuOpen(false)}>{label}</a>)}</nav>}
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-title">
      <div className="header-backdrop" aria-hidden="true" />
      <Drawing name="grama-larga" className="decor decor-hero-left-grass" />
      <Drawing name="rabisco-amarelo" className="decor decor-hero-right-squiggle" />
      <Drawing name="tracos-amarelos-esquerda" className="decor decor-hero-rays-left" />
      <Drawing name="tracos-amarelos-direita" className="decor decor-hero-rays-middle" />
      <Drawing name="trilha-rosa" className="decor decor-hero-pink-trail" />
      <div className="hero-copy">
        <p className="eyebrow">RECREAÇÃO COM CARINHO,<br />DIVERSÃO E DESCOBERTAS <Drawing name="coracao-pequeno" /></p>
        <h1 id="hero-title">Um cantinho<br />para <span className="pink">brincar,</span><br /><span className="yellow">crescer</span> e ser feliz.</h1>
        <p className="hero-lead">Carinho em cada cuidado, espaço para imaginar<br className="desktop-break" /> e novas descobertas todos os dias.</p>
        <div className="hero-actions">
          <a className="button button-pink visit-button" href={whatsapp} aria-label="Agende uma visita pelo WhatsApp" target="_blank" rel="noopener noreferrer">Agende uma visita <span aria-hidden="true">↗</span></a>
        </div>
      </div>
      <div className="hero-visual" aria-hidden="true"><Drawing name="ilustracao-principal" className="hero-scene" /></div>
      <Drawing name="coracao-lateral" className="deco deco-hero-heart" />
      <Drawing name="grama-pequena" className="deco deco-hero-grass" />
      <div className="hero-edge" aria-hidden="true" />
    </section>
  );
}

const careCards = [
  { tone: 'pink', icon: 'icone-coracao', title: 'Carinho de verdade', lines: ['Cuidadoras carinhosas', 'e atenciosas em cada', 'momento.'] },
  { tone: 'blue', icon: 'icone-casinha', title: 'Um lugar seguro', lines: ['Ambiente seguro', 'e estimulante para', 'explorar o mundo.'] },
  { tone: 'yellow', icon: 'icone-paleta', title: 'Aprender brincando', lines: ['Atividades criativas e', 'educativas cheias', 'de imaginação.'] },
  { tone: 'green', icon: 'icone-prato', title: 'Comer bem também', lines: ['Refeições balanceadas', 'e saudáveis para cuidar', 'de dentro para fora.'] },
];

function Care() {
  return (
    <section className="care" id="sobre" aria-labelledby="care-title">
      <p className="section-kicker">O QUE FAZ NOSSO CANTINHO ESPECIAL</p>
      <h2 id="care-title">Cuidado que acolhe. <span>Diversão que ensina.</span></h2>
      <p className="care-lead">Um ambiente pensado para as crianças se sentirem seguras, livres para criar e cheias de vontade de descobrir.</p>
      <Drawing name="arco-iris-estrela" className="deco care-rainbow" />
      <Drawing name="trilha-lateral" className="decor decor-care-left-trail" />
      <Drawing name="nuvem-lateral" className="decor decor-care-right-cloud" />
      <Drawing name="trilha-grama-lateral" className="decor decor-care-right-trail" />
      <Drawing name="estrela-pequena" className="decor decor-care-left-star" />
      <Drawing name="coracao-pequeno" className="deco care-heart" />
      <div className="care-grid" id="cuidados">
        {careCards.map(({ tone, icon, title, lines }) => <article className={`care-card card-${tone}`} key={title}>
          <Drawing name={icon} /><h3>{title}</h3><p>{lines.map((line, i) => <React.Fragment key={line}>{i > 0 && <br />}{line}</React.Fragment>)}</p>
        </article>)}
      </div>
    </section>
  );
}

const activities = [
  ['icone-relogio', <>Integral, meio período<br />ou diária</>],
  ['icone-bale', 'Balé'],
  ['icone-cross-kids', 'Cross Kids'],
  ['icone-maca', 'Almoço incluso'],
];

function Activities() {
  return <section className="activities" id="atividades" aria-labelledby="activities-title">
    <Drawing name="arco-pontilhado" className="decor decor-activities-arc" />
    <Drawing name="linha-pontilhada-amarela" className="decor decor-activities-line" />
    <h2 id="activities-title" className="section-kicker">NOSSAS ATIVIDADES E MODALIDADES</h2>
    <ul>{activities.map(([icon, label]) => <li key={icon}><Drawing name={icon} className="activity-symbol" />{label}</li>)}</ul>
    <Drawing name="aviao-papel" className="deco activities-plane" />
  </section>;
}

function Closing() {
  return <section className="closing" id="contato" aria-labelledby="closing-title">
    <Drawing name="onda-azul" className="closing-wave" />
    <Drawing name="coracao-grande" className="decor decor-closing-heart" />
    <Drawing name="grama-larga" className="decor decor-closing-left-grass" />
    <Drawing name="nuvem-contorno" className="decor mobile-closing-cloud" />
    <Drawing name="coracao-pequeno" className="decor mobile-closing-heart" />
    <div className="closing-content">
      <h2 id="closing-title"><span className="word-intro">Quer conhecer</span> <span className="word-esse">esse</span> <span className="word-cantinho">cantinho</span> <span className="word-end">de perto?</span></h2>
      <p>Será um prazer te receber e mostrar tudo o que<br className="desktop-break" /> faz do Cantinho da Alegria um lugar tão especial!</p>
      <a className="button button-white" href={instagram} target="_blank" rel="noopener noreferrer"><Drawing name="icone-instagram" className="ig-icon" /><span>Vamos conversar<br />pelo Instagram</span><b aria-hidden="true">›</b></a>
    </div>
    <Drawing name="menina-sol-inteiro" className="closing-girl" alt="Menina ilustrada sorrindo e acenando sob o sol" />
    <Drawing name="grama-larga" className="closing-grass" />
    <Drawing name="grama-rodape" className="closing-grass-mobile" />
  </section>;
}

function MobileContact() {
  return <section className="mobile-contact mobile-only" aria-labelledby="mobile-contact-title">
    <Drawing name="coracao-pequeno" className="mobile-contact-heart" />
    <h2 id="mobile-contact-title"><span aria-hidden="true">☀</span> Entre em contato</h2>
    <p>Estamos prontos para receber<br />sua família!</p>
    <a className="button mobile-whatsapp" href={whatsapp} target="_blank" rel="noopener noreferrer"><Drawing name="icone-whatsapp-rodape" /> Chamar no WhatsApp <span aria-hidden="true">↗</span></a>
  </section>;
}

function Footer() {
  return <footer className="footer">
    <Brand footer />
    <nav aria-label="Navegação do rodapé">{links.map(([label, href]) => <a key={href} href={href}>{label}</a>)}</nav>
    <p>Recreação &amp; Cuidados Infantis<br />Cantinho da Alegria <span>♡</span></p>
  </footer>;
}

export default function App() {
  return <div className="site" id="inicio"><Header /><main><Hero /><Care /><Activities /><Closing /><MobileContact /></main><Footer /></div>;
}
