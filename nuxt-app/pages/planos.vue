<template>
  <div class="layout">
    <div class="bg-layer">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <a href="/" style="text-decoration:none;color:inherit;">
        <div class="sidebar-logo">
          <span class="icon">✦</span>
          <span>Manueli's <em>Clubes</em></span>
        </div>
      </a>
      <span class="sidebar-section">Principal</span>
      <NavBar />
    </aside>

    <div class="main">
      <header class="topbar">
        <div class="topbar-left">
          <button class="btn-menu" @click="sidebarOpen = !sidebarOpen">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <div>
            <h1>Planos</h1>
            <p>Escolhe o plano ideal para a tua organização ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="badge-date">{{ currentMonthYear }}</span>
        </div>
      </header>

      <div class="content">
        <div v-if="successMsg" class="alert alert-success">✦ {{ successMsg }}</div>
        <div v-if="cancelMsg" class="alert alert-cancel">{{ cancelMsg }}</div>

        <div class="plans-header">
          <span class="section-chip">✦ Subscrição</span>
          <h2 class="section-title">Encontra o plano <em>perfeito</em></h2>
          <p class="section-desc">Começa gratuitamente e faz upgrade conforme a tua necessidade.</p>
        </div>

        <div class="plans-grid">
          <div class="plan-card">
            <div class="plan-badge">Starter</div>
            <div class="plan-price">
              <span class="price-value">{{ planos[0]?.preco  || "0"}}€</span>
              <span class="price-period">/mês</span>
            </div>
            <p class="plan-desc">Ideal para experimentar a plataforma sem compromisso.</p>
            <div class="plan-divider"></div>
            <ul class="plan-features">
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Até <strong>3 clubes</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Até <strong>1 mapa</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Calendário de eventos
              </li>
            </ul>
            <button class="plan-btn" disabled>Plano Atual</button>
          </div>

          <div class="plan-card featured">
            <div class="plan-badge">Pro</div>
            <div class="popular-tag">Mais popular</div>
            <div class="plan-price">
              <span class="price-value">{{ planos[1]?.preco  || ""}}€</span>
              <span class="price-period">/mês</span>
            </div>
            <p class="plan-desc">Para equipas em crescimento que precisam de mais recursos.</p>
            <div class="plan-divider"></div>
            <ul class="plan-features">
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Até <strong>15 clubes</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Até <strong>20 mapas</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Calendário de eventos
              </li>
            </ul>
            <button class="plan-btn gold" :disabled="loadingPlano === 2" @click="escolherPlano(2)">
              {{ loadingPlano === 2 ? 'A redirecionar...' : 'Escolher Pro' }}
            </button>
          </div>

          <div class="plan-card">
            <div class="plan-badge">Enterprise</div>
            <div class="plan-price">
              <span class="price-value">{{ planos[2]?.preco  || ""}}€</span>
              <span class="price-period">/mês</span>
            </div>
            <p class="plan-desc">Sem limites. Tudo incluído para grandes organizações.</p>
            <div class="plan-divider"></div>
            <ul class="plan-features">
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Clubes <strong>ilimitados</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Mapas <strong>ilimitados</strong>
              </li>
              <li class="feature-item included">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                Calendário de eventos
              </li>
            </ul>
            <button class="plan-btn" :disabled="loadingPlano === 3" @click="escolherPlano(3)">
              {{ loadingPlano === 3 ? 'A redirecionar...' : 'Escolher Enterprise' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavBar from '~/components/Navbar.vue'

const router = useRouter()
const route = useRoute()
const planos = ref([])
const sidebarOpen = ref(false)
const token = ref(null)
const loadingPlano = ref(null)
const successMsg = ref('')
const cancelMsg = ref('')

async function buscarPrecoPlanos() {
  try {
    const response = await fetch('http://localhost:8000/planos', {
      headers: { Authorization: `Bearer ${token.value}` }
    })

    if (!response.ok) {
      throw new Error("Erro ao buscar preços dos planos")
    }

    planos.value = await response.json()

  } catch (error) {
    console.error(error)
  }
}

async function escolherPlano(planoId) {
  loadingPlano.value = planoId
  try {
    const response = await fetch('http://localhost:8000/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`
      },
      body: JSON.stringify({ plano_id: planoId })
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Erro ao criar sessão de pagamento')
    }

    const { url } = await response.json()
    window.location.href = url

  } catch (error) {
    console.error(error)
    cancelMsg.value = error.message
  } finally {
    loadingPlano.value = null
  }
}

async function confirmarPlanoAposStripe(planoId) {
  try {
    const response = await fetch(`http://localhost:8000/me/plano/${planoId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Erro ao ativar plano')
    }

    const planoNomes = { 1: 'Free', 2: 'Pro', 3: 'Enterprise' }
    successMsg.value = `✦ Plano ${planoNomes[planoId] ?? ''} ativado com sucesso!`

  } catch (error) {
    console.error(error)
    cancelMsg.value = `Pagamento efetuado mas erro ao ativar plano: ${error.message}`
  }
}

const currentMonthYear = computed(() =>
  new Date().toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
    .replace(/^\w/, c => c.toUpperCase())
)

onMounted( () => {
  token.value = localStorage.getItem('access_token')
  if (!token.value) { router.push('/login') }
  buscarPrecoPlanos()

  if (route.query.success === 'true' && route.query.plano_id) {
    confirmarPlanoAposStripe(Number(route.query.plano_id))
    router.replace({ path: route.path })
  }
  if (route.query.canceled === 'true') {
    cancelMsg.value = 'Pagamento cancelado. Podes tentar novamente quando quiseres.'
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.layout {
  --gold:      #c9a96e;
  --gold-l:    #e8c97e;
  --gold-dim:  rgba(201,169,110,0.09);
  --bg:        #0a0a0f;
  --surface:   rgba(255,255,255,0.025);
  --surface2:  rgba(255,255,255,0.04);
  --border:    rgba(232,228,216,0.07);
  --border-g:  rgba(201,169,110,0.14);
  --text:      #e8e4d8;
  --muted:     #6e6b5e;
  --faint:     #3e3c35;
  --sidebar-w: 240px;
  --radius:    14px;

  display: flex;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  overflow-x: hidden;
}

.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(120px); }
.orb-1 { width: 520px; height: 520px; background: var(--gold); opacity: .06; top: -200px; left: 20px; }
.orb-2 { width: 360px; height: 360px; background: #6e8fc9; opacity: .05; bottom: 0; right: 8%; }
.orb-3 { width: 280px; height: 280px; background: #c96e8f; opacity: .04; top: 45%; right: -50px; }

.sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99; backdrop-filter: blur(3px); }

.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: rgba(10,10,15,0.94);
  border-right: 1px solid var(--border-g);
  backdrop-filter: blur(20px);
  display: flex; flex-direction: column;
  z-index: 100; padding: 0 0 2rem;
  transition: transform .3s ease;
}
.sidebar-logo { display: flex; align-items: center; gap: .5rem; font-family: 'Cormorant Garamond', serif; font-size: 1.15rem; padding: 1.8rem 1.5rem 1.5rem; border-bottom: 1px solid var(--border-g); }
.sidebar-logo .icon { color: var(--gold); }
.sidebar-logo em { font-style: italic; color: var(--gold); }
.sidebar-section { font-size: .62rem; letter-spacing: .14em; text-transform: uppercase; color: var(--faint); padding: 1.4rem 1.5rem .5rem; }

.main { margin-left: var(--sidebar-w); width: calc(100% - var(--sidebar-w)); min-width: 0; flex: 1; position: relative; z-index: 1; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }

.topbar { display: flex; align-items: center; justify-content: space-between; padding: 1.3rem 2rem; border-bottom: 1px solid var(--border); backdrop-filter: blur(12px); background: rgba(10,10,15,.6); position: sticky; top: 0; z-index: 50; gap: 1rem; }
.topbar-left { display: flex; align-items: center; gap: 1rem; min-width: 0; flex: 1; }
.topbar-left h1 { font-family: 'Cormorant Garamond', serif; font-size: 1.55rem; font-weight: 300; white-space: nowrap; }
.topbar-left p { font-size: .78rem; color: var(--muted); margin-top: .1rem; white-space: nowrap; }
.topbar-right { display: flex; align-items: center; gap: .9rem; flex-shrink: 0; }
.btn-menu { display: none; width: 34px; height: 34px; border-radius: 50%; background: var(--surface); border: 1px solid var(--border); align-items: center; justify-content: center; cursor: pointer; color: var(--muted); flex-shrink: 0; transition: color .2s, border-color .2s; }
.btn-menu:hover { color: var(--gold); border-color: var(--border-g); }
.badge-date { font-size: .72rem; color: var(--muted); border: 1px solid var(--border-g); padding: .28rem .8rem; border-radius: 100px; white-space: nowrap; }

.content { padding: 2rem; display: flex; flex-direction: column; gap: 2rem; width: 100%; min-width: 0; align-items: center; }

.plans-header { text-align: center; animation: fadeUp .45s ease both; }
.section-chip {
  display: inline-flex; align-items: center; gap: .4rem;
  font-size: .62rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--gold); border: 1px solid var(--border-g);
  padding: .22rem .75rem; border-radius: 100px;
  background: var(--gold-dim);
}
.section-title { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; line-height: 1.2; margin-top: .6rem; }
.section-title em { font-style: italic; color: var(--gold); }
.section-desc { font-size: .85rem; color: var(--muted); margin-top: .4rem; }

.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  width: 100%;
  max-width: 960px;
  animation: fadeUp .5s ease .1s both;
}

.plan-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem 1.8rem;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: border-color .3s, transform .3s;
}
.plan-card:hover { border-color: var(--border-g); transform: translateY(-4px); }
.plan-card.featured {
  border-color: rgba(201,169,110,0.35);
  background: rgba(201,169,110,0.03);
}
.plan-card.featured::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--gold), var(--gold-l));
}

.plan-badge {
  font-size: .65rem; letter-spacing: .14em; text-transform: uppercase;
  color: var(--muted); margin-bottom: .8rem;
}
.featured .plan-badge { color: var(--gold); }

.popular-tag {
  position: absolute; top: 1.2rem; right: 1.2rem;
  font-size: .6rem; letter-spacing: .1em; text-transform: uppercase;
  color: var(--gold); background: var(--gold-dim);
  border: 1px solid var(--border-g);
  padding: .2rem .6rem; border-radius: 100px;
}

.plan-price { display: flex; align-items: baseline; gap: .2rem; margin-bottom: .6rem; }
.price-value { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 600; line-height: 1; }
.price-period { font-size: .8rem; color: var(--muted); }

.plan-desc { font-size: .8rem; color: var(--muted); line-height: 1.5; }

.plan-divider { height: 1px; background: var(--border); margin: 1.4rem 0; }

.plan-features { list-style: none; display: flex; flex-direction: column; gap: .7rem; flex: 1; }

.feature-item {
  display: flex; align-items: center; gap: .6rem;
  font-size: .82rem; color: var(--text);
}
.feature-item strong { font-weight: 500; }
.feature-item.included svg { color: var(--gold); }
.feature-item.excluded { color: var(--faint); }
.feature-item.excluded svg { color: var(--faint); }

.plan-btn {
  margin-top: 1.8rem;
  width: 100%;
  padding: .8rem 1.2rem;
  border-radius: 100px;
  font-family: 'DM Sans', sans-serif;
  font-size: .85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all .25s;
  background: var(--surface2);
  border: 1px solid var(--border-g);
  color: var(--text);
}
.plan-btn:hover { background: rgba(201,169,110,0.08); border-color: var(--gold); color: var(--gold); }
.plan-btn.gold {
  background: linear-gradient(135deg, var(--gold), var(--gold-l));
  color: #0a0a0f;
  border: none;
  font-weight: 600;
}
.plan-btn.gold:hover { opacity: .9; transform: translateY(-1px); }

@keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }

.alert {
  width: 100%; max-width: 960px; padding: 1rem 1.4rem;
  border-radius: var(--radius); font-size: .88rem; text-align: center;
  animation: fadeUp .4s ease both;
}
.alert-success {
  background: rgba(76,175,80,0.08); border: 1px solid rgba(76,175,80,0.3); color: #81c784;
}
.alert-cancel {
  background: rgba(255,152,0,0.08); border: 1px solid rgba(255,152,0,0.3); color: #ffb74d;
}

@media (max-width: 1099px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; width: 100%; }
  .btn-menu { display: flex; }
  .plans-grid { grid-template-columns: repeat(3, 1fr); gap: 1rem; }
}

@media (max-width: 768px) {
  .topbar { padding: 1rem 1.2rem; }
  .topbar-left p { display: none; }
  .badge-date { display: none; }
  .content { padding: 1.5rem 1rem; }
  .plans-grid { grid-template-columns: 1fr; max-width: 380px; }
  .section-title { font-size: 1.6rem; }
}

@media (max-width: 480px) {
  .topbar-left h1 { font-size: 1.25rem; }
  .content { padding: 1rem .75rem; }
  .plan-card { padding: 1.5rem 1.3rem; }
  .price-value { font-size: 2.2rem; }
}
</style>
