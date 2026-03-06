<template>
  <div class="page">
    <div class="bg-layer">
      <div class="noise"></div>
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <header class="header">
      <div class="logo">
        <a href="/" style="text-decoration:none;color:inherit;">
        <span class="logo-icon">✦</span>
        <span class="logo-text">Manueli's <em>Clubes</em></span>
        </a>
      </div>
      <nav class="nav">
        <NuxtLink to="/" class="nav-link">Início</NuxtLink>
        <NuxtLink to="/aboutus" class="nav-link active">Sobre nós</NuxtLink>
        <NuxtLink to="/login" class="nav-link"><button class="btn-primary">Entrar</button></NuxtLink>
      </nav>
    </header>
    <section class="hero">
      <div class="hero-badge">A nossa história</div>
      <h1 class="hero-title">
        Feito com <span class="gradient-text">paixão</span><br />por a comunidade
      </h1>
      <p class="hero-subtitle">
        Nascemos da vontade de aproximar pessoas com interesses comuns,<br />
        num espaço onde cada clube tem uma história para contar.
      </p>
    </section>

    <!-- Mission + Vision -->
    <section class="section two-col">
      <div class="text-block" style="animation-delay: 0.05s">
        <span class="block-tag">Missão</span>
        <h2 class="block-title">Conectar pessoas<br /><em>através de clubes</em></h2>
        <p class="block-body">
          A nossa missão é simples: criar uma plataforma onde qualquer pessoa possa
          encontrar ou criar um clube que reflita os seus interesses. Acreditamos que
          as comunidades tornam a vida mais rica, mais divertida e mais significativa.
        </p>
        <p class="block-body">
          Desde clubes de leitura a grupos de escalada, de enthusiastas de tecnologia
          a apreciadores de gastronomia — há um espaço para todos aqui.
        </p>
      </div>
      <div class="visual-block" style="animation-delay: 0.15s">
        <div class="visual-card vc-1">
          <span class="vc-num">{{ clubes }}</span>
          <span class="vc-label">Clubes Ativos</span>
        </div>
        <div class="visual-card vc-2">
          <span class="vc-num">{{ utilizadores }}</span>
          <span class="vc-label">Membros</span>
        </div>
        <div class="visual-card vc-3">
          <span class="vc-num">{{ tipousers }}</span>
          <span class="vc-label">Categorias</span>
        </div>
        <div class="visual-card vc-4">
          <span class="vc-num">2026</span>
          <span class="vc-label">Fundado em</span>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-label">Os nossos valores</div>
      <h2 class="section-title">O que nos <em>guia</em></h2>
      <div class="values-grid">
        <div v-for="(val, i) in values" :key="i" class="value-card" :style="`animation-delay: ${0.05 * i}s`">
          <div class="value-icon">{{ val.icon }}</div>
          <h3 class="value-title">{{ val.title }}</h3>
          <p class="value-desc">{{ val.desc }}</p>
        </div>
      </div>
    </section>


    <section class="section">
      <div class="section-label">A equipa</div>
      <h2 class="section-title">As pessoas por <em>detrás</em></h2>
      <div class="team-grid">
        <div class="team-card" :style="`animation-delay: ${0.08}s`">
          <div class="team-avatar">
            <img src="assets/images/96d16583-263e-498d-aff1-389601c601de.jpg" alt="Manueli Silvestre" />
          </div>
          <div class="team-info">
            <span class="team-name">Manueli Silvestre</span>
            <span class="team-role">Fundador & CEO</span>
          </div>
          <p class="team-bio">Apaixonado por comunidades e tecnologia. Criou esta plataforma depois de não encontrar um lugar simples para gerir o seu clube de leitura</p>
          <div class="team-links">
            <a :href="`mailto:manueli@clubes.pt`" class="team-link">✉</a>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="cta-inner">
        <div class="hero-badge">Junta-te a nós</div>
        <h2 class="cta-title">Pronto para encontrar<br /><em>o teu clube?</em></h2>
        <p class="cta-sub">Cria a tua conta hoje e descobre comunidades que partilham a tua paixão.</p>
        <div class="cta-actions">
          <NuxtLink to="/login"><button class="btn-primary btn-lg">Começar agora</button></NuxtLink>
        </div>
      </div>
    </section>

    <footer class="footer">
      <span class="logo-text small">✦ Manueli's <em>Clubes</em></span>
      <span class="footer-copy">© 2025 — Todos os direitos reservados</span>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'

const clubes = ref(0)
const utilizadores = ref(0)
const tipousers = ref(0)

async function buscarStats() {
  try {
    const response = await fetch('http://192.168.1.83:8000/stats')

    if (!response.ok) {
      throw new Error("Erro ao buscar estatísticas")
    }

    const data = await response.json()
    clubes.value = data.clubes
    utilizadores.value = data.utilizadores
    tipousers.value = data.tipousers

  } catch (error) {
    console.error(error)
  }
}

const values = [
  {
    icon: '🤝',
    title: 'Comunidade',
    desc: 'Acreditamos que as melhores experiências acontecem quando estamos rodeados de pessoas com os mesmos interesses.',
  },
  {
    icon: '✦',
    title: 'Autenticidade',
    desc: 'Cada clube tem a sua identidade única. Aqui não há moldes — só espaço para seres quem és.',
  },
  {
    icon: '🔓',
    title: 'Abertura',
    desc: 'Todos são bem-vindos. A diversidade de perspetivas é o que torna as comunidades verdadeiramente ricas.',
  },
  {
    icon: '⚡',
    title: 'Movimento',
    desc: 'Não ficamos parados. Evoluímos constantemente para servir melhor os nossos membros e clubes.',
  },
]

onMounted(() => {
  buscarStats()
})
</script>

<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  min-height: 100vh;
  background: #0a0a0f;
  color: #e8e4d8;
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  overflow-x: hidden;
  position: relative;
}

.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.noise {
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  opacity: 0.4;
}
.orb { position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.12; }
.orb-1 { width: 600px; height: 600px; background: #c9a96e; top: -200px; left: -200px; }
.orb-2 { width: 400px; height: 400px; background: #6e8fc9; bottom: 20%; right: -100px; }
.orb-3 { width: 300px; height: 300px; background: #c96e8f; bottom: -100px; left: 30%; }

.header {
  position: sticky; top: 0; z-index: 10;
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.5rem 4rem;
  border-bottom: 1px solid rgba(201,169,110,0.15);
  backdrop-filter: blur(12px);
  background: rgba(10,10,15,0.6);
}
.logo {
  display: flex; align-items: center; gap: 0.5rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.4rem; letter-spacing: 0.02em;
}
.logo-icon { color: #c9a96e; }
.logo-text em { font-style: italic; color: #c9a96e; }
.nav { display: flex; align-items: center; gap: 2rem; }
.nav-link {
  color: #9d9a8e; text-decoration: none;
  font-size: 0.875rem; letter-spacing: 0.04em;
  transition: color 0.2s;
}
.nav-link:hover, .nav-link.active { color: #e8e4d8; }

.btn-primary {
  background: linear-gradient(135deg, #c9a96e, #e8c97e);
  color: #0a0a0f; border: none;
  padding: 0.6rem 1.4rem; border-radius: 100px;
  font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 500;
  cursor: pointer; transition: opacity 0.2s, transform 0.2s;
}
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-primary.btn-lg { padding: 0.85rem 2rem; font-size: 1rem; }

.btn-ghost {
  background: transparent; color: #e8e4d8;
  border: 1px solid rgba(232,228,216,0.2);
  padding: 0.6rem 1.4rem; border-radius: 100px;
  font-family: 'DM Sans', sans-serif; font-size: 0.875rem; font-weight: 300;
  cursor: pointer; transition: border-color 0.2s, background 0.2s;
}
.btn-ghost:hover { border-color: rgba(201,169,110,0.4); background: rgba(201,169,110,0.06); }
.btn-ghost.btn-lg { padding: 0.85rem 2rem; font-size: 1rem; }

.hero {
  position: relative; z-index: 1;
  text-align: center;
  padding: 7rem 2rem 5rem;
  display: flex; flex-direction: column; align-items: center; gap: 1.4rem;
}
.hero-badge {
  display: inline-block;
  border: 1px solid rgba(201,169,110,0.4);
  color: #c9a96e;
  font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
  padding: 0.32rem 1rem; border-radius: 100px;
  animation: fadeUp 0.5s ease both;
}
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3rem, 7vw, 5.5rem);
  font-weight: 300; line-height: 1.1;
  animation: fadeUp 0.5s 0.08s ease both;
}
.gradient-text {
  background: linear-gradient(135deg, #c9a96e, #e8c97e, #c96e8f);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; font-style: italic;
}
.hero-subtitle {
  color: #6e6b5e; font-size: 1.05rem; line-height: 1.75; max-width: 520px;
  animation: fadeUp 0.5s 0.16s ease both;
}

.section {
  position: relative; z-index: 1;
  max-width: 1100px; margin: 0 auto;
  padding: 5rem 4rem;
}
.section-label {
  font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: #c9a96e; margin-bottom: 0.7rem;
}
.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 4vw, 3rem); font-weight: 300;
  line-height: 1.2; margin-bottom: 3rem;
}
.section-title em { font-style: italic; color: #c9a96e; }

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  align-items: center;
}

.text-block { animation: fadeUp 0.6s ease both; }
.block-tag {
  font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: #c9a96e; display: block; margin-bottom: 0.8rem;
}
.block-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.4rem; font-weight: 300; line-height: 1.2;
  margin-bottom: 1.5rem;
}
.block-title em { font-style: italic; color: #c9a96e; }
.block-body {
  color: #6e6b5e; font-size: 0.95rem; line-height: 1.8;
  margin-bottom: 1rem;
}

.visual-block {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  animation: fadeUp 0.6s ease both;
}
.visual-card {
  border-radius: 18px;
  padding: 2rem 1.5rem;
  display: flex; flex-direction: column; gap: 0.4rem;
  border: 1px solid rgba(232,228,216,0.08);
  transition: border-color 0.2s, transform 0.2s;
}
.visual-card:hover { border-color: rgba(201,169,110,0.2); transform: translateY(-3px); }
.vc-1 { background: rgba(201,169,110,0.06); }
.vc-2 { background: rgba(110,143,201,0.06); }
.vc-3 { background: rgba(201,110,143,0.06); }
.vc-4 { background: rgba(110,201,126,0.06); }
.vc-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.6rem; font-weight: 600; color: #c9a96e; line-height: 1;
}
.vc-label { font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: #6e6b5e; }

.values-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1.4rem;
}
.value-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(232,228,216,0.08);
  border-radius: 18px; padding: 2rem 1.6rem;
  transition: border-color 0.2s, transform 0.2s;
  animation: fadeUp 0.5s ease both;
}
.value-card:hover { border-color: rgba(201,169,110,0.2); transform: translateY(-4px); }
.value-icon { font-size: 1.8rem; margin-bottom: 1rem; }
.value-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.3rem; font-weight: 400; margin-bottom: 0.6rem; color: #e8e4d8;
}
.value-desc { font-size: 0.85rem; color: #6e6b5e; line-height: 1.75; }


.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 320px));
  justify-content: center;
  gap: 1.6rem;
}
.team-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(232,228,216,0.08);
  border-radius: 20px; padding: 2.2rem 2rem;
  display: flex; flex-direction: column; gap: 0.8rem;
  transition: border-color 0.2s, transform 0.2s;
  animation: fadeUp 0.5s ease both;
}
.team-card:hover { border-color: rgba(201,169,110,0.2); transform: translateY(-4px); }
.team-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; font-weight: 500; color: #0a0a0f;
   overflow: hidden;
  margin-bottom: 0.4rem;
}
.team-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.team-info { display: flex; flex-direction: column; gap: 0.2rem; }
.team-name { font-size: 1rem; font-weight: 500; color: #e8e4d8; }
.team-role { font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: #c9a96e; }
.team-bio { font-size: 0.875rem; color: #6e6b5e; line-height: 1.75; flex: 1; }
.team-links { display: flex; gap: 0.6rem; margin-top: 0.4rem; }
.team-link {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(232,228,216,0.1);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.78rem; color: #9d9a8e; text-decoration: none;
  transition: border-color 0.2s, color 0.2s;
}
.team-link:hover { border-color: rgba(201,169,110,0.4); color: #c9a96e; }

/* ── Timeline ── */
.timeline { display: flex; flex-direction: column; }
.timeline-item {
  display: grid; grid-template-columns: 80px 1px 1fr;
  gap: 0 2rem;
  align-items: start;
  padding-bottom: 2.5rem;
  animation: fadeUp 0.5s ease both;
}
.timeline-item:last-child { padding-bottom: 0; }

.tl-year {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.3rem; color: #c9a96e; font-weight: 600;
  text-align: right; padding-top: 0.1rem;
}
.tl-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: #c9a96e;
  border: 2px solid #0a0a0f;
  box-shadow: 0 0 0 1px #c9a96e;
  margin: 0.25rem auto 0;
  position: relative;
}
.tl-dot::after {
  content: '';
  position: absolute; top: 12px; left: 50%;
  transform: translateX(-50%);
  width: 1px; height: calc(100% + 2.5rem - 10px);
  background: rgba(201,169,110,0.2);
}
.timeline-item:last-child .tl-dot::after { display: none; }

.tl-content { padding-bottom: 0.5rem; }
.tl-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.3rem; font-weight: 400; margin-bottom: 0.4rem; color: #e8e4d8;
}
.tl-desc { font-size: 0.875rem; color: #6e6b5e; line-height: 1.75; }


.cta-section {
  position: relative; z-index: 1;
  padding: 5rem 2rem 6rem;
  text-align: center;
}
.cta-inner {
  max-width: 580px; margin: 0 auto;
  display: flex; flex-direction: column; align-items: center; gap: 1.2rem;
}
.cta-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 300; line-height: 1.2;
}
.cta-title em { font-style: italic; color: #c9a96e; }
.cta-sub { color: #6e6b5e; font-size: 1rem; line-height: 1.7; }
.cta-actions { display: flex; gap: 1rem; margin-top: 0.5rem; }

.footer {
  position: relative; z-index: 1;
  display: flex; justify-content: space-between; align-items: center;
  padding: 1.5rem 4rem;
  border-top: 1px solid rgba(201,169,110,0.1);
}
.logo-text.small { font-family: 'Cormorant Garamond', serif; font-size: 1rem; }
.footer-copy { font-size: 0.75rem; color: #3d3b35; }


@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (max-width: 960px) {
  .two-col { grid-template-columns: 1fr; gap: 3rem; }
  .values-grid { grid-template-columns: 1fr 1fr; }
  .team-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 768px) {
  .header { padding: 1.2rem 1.5rem; }
  .nav .nav-link:not(:last-child) { display: none; }
  .section { padding: 4rem 1.5rem; }
  .values-grid, .team-grid { grid-template-columns: 1fr; }
  .timeline-item { grid-template-columns: 60px 1px 1fr; }
  .footer { padding: 1.2rem 1.5rem; flex-direction: column; gap: 0.5rem; text-align: center; }
}
</style>