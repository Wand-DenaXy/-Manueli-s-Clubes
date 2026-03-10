<template>
  <div class="page">
    <div class="bg-layer">
      <div class="noise"></div>
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

      <Header />

    <section class="hero">
      <h1 class="hero-title">
        Bem-vindo ao mundo<br />
        <span class="gradient-text">dos Clubes</span>
      </h1>
      <p class="hero-subtitle">
        Descubra comunidades únicas, conecte-se com pessoas extraordinárias<br />
        e viva experiências que ficam para sempre.
      </p>
      <div class="hero-actions">
        <a href="mapas"><button class="btn-primary btn-lg">Descobrir Localização</button></a>
        <a href="clubes"><button class="btn-ghost btn-lg">Criar meu Clube</button></a>
      </div>
      <div class="hero-stats">
        <div class="stat">
          <span class="stat-num">{{ clubes }}</span>
          <span class="stat-label">Clubes Ativos</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat">
          <span class="stat-num">{{ utilizadores }}</span>
          <span class="stat-label">Membros</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat">
          <span class="stat-num">{{ mapas }}</span>
          <span class="stat-label">Localizações</span>
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
import Header from '/components/Header.vue'
import { onMounted } from 'vue'
import { ref } from 'vue'

const clubes = ref(0)
const utilizadores = ref(0)
const mapas = ref(0)

async function buscarStats() {
  try {
    const response = await fetch('http://localhost:8000/stats')

    if (!response.ok) {
      throw new Error("Erro ao buscar estatísticas")
    }

    const data = await response.json()
    clubes.value = data.clubes
    utilizadores.value = data.utilizadores
    mapas.value = data.mapas

  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  buscarStats()
})
</script>
<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  min-height: 100vh;
  background: #0a0a0f;
  color: #e8e4d8;
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  overflow-x: hidden;
  position: relative;
}

.bg-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.noise {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  opacity: 0.4;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.12;
}
.orb-1 { width: 600px; height: 600px; background: #c9a96e; top: -200px; left: -200px; }
.orb-2 { width: 400px; height: 400px; background: #6e8fc9; bottom: 20%; right: -100px; }
.orb-3 { width: 300px; height: 300px; background: #c96e8f; bottom: -100px; left: 30%; }

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.4rem;
  letter-spacing: 0.02em;
}
.logo-icon { color: #c9a96e; }
.logo-text em { font-style: italic; color: #c9a96e; }

.nav { display: flex; align-items: center; gap: 2rem; }
.nav-link {
  color: #9d9a8e;
  text-decoration: none;
  font-size: 0.875rem;
  letter-spacing: 0.04em;
  transition: color 0.2s;
}
.nav-link:hover { color: #e8e4d8; }

.btn-primary {
  background: linear-gradient(135deg, #c9a96e, #e8c97e);
  color: #0a0a0f;
  border: none;
  padding: 0.6rem 1.4rem;
  border-radius: 100px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-primary.btn-lg { padding: 0.85rem 2rem; font-size: 1rem; }

.btn-ghost {
  background: transparent;
  color: #e8e4d8;
  border: 1px solid rgba(232, 228, 216, 0.25);
  padding: 0.6rem 1.4rem;
  border-radius: 100px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 400;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.btn-ghost:hover { border-color: rgba(201, 169, 110, 0.5); background: rgba(201, 169, 110, 0.06); }
.btn-ghost.btn-lg { padding: 0.85rem 2rem; font-size: 1rem; }

.hero {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 8rem 2rem 6rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}
.hero-badge {
  display: inline-block;
  border: 1px solid rgba(201, 169, 110, 0.4);
  color: #c9a96e;
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0.35rem 1rem;
  border-radius: 100px;
  animation: fadeUp 0.6s ease both;
}
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3rem, 7vw, 6rem);
  font-weight: 300;
  line-height: 1.1;
  letter-spacing: -0.01em;
  animation: fadeUp 0.6s 0.1s ease both;
}
.gradient-text {
  background: linear-gradient(135deg, #c9a96e, #e8c97e, #c96e8f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-style: italic;
}
.hero-subtitle {
  color: #6e6b5e;
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 520px;
  animation: fadeUp 0.6s 0.2s ease both;
}
.hero-actions {
  display: flex;
  gap: 1rem;
  animation: fadeUp 0.6s 0.3s ease both;
}
.hero-stats {
  display: flex;
  align-items: center;
  gap: 2.5rem;
  margin-top: 2rem;
  padding: 1.5rem 3rem;
  border: 1px solid rgba(201, 169, 110, 0.15);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(8px);
  animation: fadeUp 0.6s 0.4s ease both;
}
.stat { text-align: center; }
.stat-num {
  display: block;
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: #c9a96e;
}
.stat-label { font-size: 0.75rem; letter-spacing: 0.06em; color: #6e6b5e; text-transform: uppercase; }
.stat-divider { width: 1px; height: 40px; background: rgba(201, 169, 110, 0.2); }

.section {
  position: relative;
  z-index: 1;
  padding: 5rem 4rem;
  max-width: 1300px;
  margin: 0 auto;
}
.section-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 2.5rem;
}
.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.4rem;
  font-weight: 300;
}
.highlight { font-style: italic; color: #c9a96e; }
.see-all { font-size: 0.875rem; color: #6e6b5e; text-decoration: none; transition: color 0.2s; }
.see-all:hover { color: #c9a96e; }


.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
.club-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(232, 228, 216, 0.08);
  border-radius: 20px;
  padding: 2rem;
  overflow: hidden;
  transition: transform 0.3s, border-color 0.3s, background 0.3s;
}
.club-card:hover {
  transform: translateY(-4px);
  border-color: rgba(201, 169, 110, 0.25);
  background: rgba(255, 255, 255, 0.05);
}
.card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0.8;
}
.card-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.card-tag {
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6e6b5e;
  margin-bottom: 0.5rem;
}
.card-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 0.6rem;
}
.card-desc {
  font-size: 0.875rem;
  color: #6e6b5e;
  line-height: 1.65;
  margin-bottom: 1.5rem;
}
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.members-preview { display: flex; align-items: center; gap: 0.5rem; }
.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #0a0a0f;
  margin-left: -6px;
  display: inline-block;
}
.avatar:first-child { margin-left: 0; }
.member-count { font-size: 0.75rem; color: #6e6b5e; margin-left: 0.25rem; }
.btn-join {
  background: transparent;
  color: #c9a96e;
  border: 1px solid rgba(201, 169, 110, 0.4);
  padding: 0.4rem 1rem;
  border-radius: 100px;
  font-size: 0.8rem;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.btn-join:hover { background: #c9a96e; color: #0a0a0f; }

.cta-section {
  position: relative;
  z-index: 1;
  padding: 5rem 2rem;
  text-align: center;
}
.cta-inner {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
}
.cta-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 300;
  line-height: 1.2;
}
.cta-sub { color: #6e6b5e; font-size: 1rem; }

.footer {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 4rem;
  border-top: 1px solid rgba(201, 169, 110, 0.1);
}
.logo-text.small { font-family: 'Cormorant Garamond', serif; font-size: 1rem; }
.footer-copy { font-size: 0.75rem; color: #3d3b35; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .header { padding: 1.2rem 1.5rem; }
  .nav { gap: 1rem; }
  .nav-link { display: none; }
  .section { padding: 4rem 1.5rem; }
  .footer { padding: 1.2rem 1.5rem; flex-direction: column; gap: 0.5rem; text-align: center; }
  .hero-stats { flex-direction: column; gap: 1rem; }
  .stat-divider { width: 60px; height: 1px; }
}
</style>