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
      <NuxtLink to="/dashboard" class="nav-item" :class="{ active: route.path === '/dashboard' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </NuxtLink>
      <NuxtLink to="/clubes" class="nav-item" :class="{ active: route.path === '/clubes' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Clubes
      </NuxtLink>
      <NuxtLink to="/mapas" class="nav-item"exact-active-class="active">
        <svg  width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"stroke-linecap="round"stroke-linejoin="round">
          <path d="M1 6l7-3 8 3 7-3v15l-7 3-8-3-7 3V6z"/>
          <line x1="8" y1="3" x2="8" y2="18"/>
          <line x1="16" y1="6" x2="16" y2="21"/>
        </svg>
        Mapas
      </NuxtLink>
      <NuxtLink to="/calendario" class="nav-item" :class="{ active: route.path === '/calendario' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        Calendário
      </NuxtLink>
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
            <h1>Dashboard</h1>
            <p>Bem-vindo de volta, {{ firstName }} ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="badge-date">{{ currentMonthYear }}</span>
        </div>
      </header>

      <div class="content">

        <div class="kpi-grid">
          <div v-for="(kpi, i) in kpis" :key="i" class="kpi-card" :class="`k${i+1}`">
            <div class="kpi-label">{{ kpi.label }}</div>
            <div class="kpi-value">{{ kpi.value }}<span class="kpi-unit">{{ kpi.unit }}</span></div>
            <div class="kpi-footer">
            </div>
            <div class="kpi-icon">{{ kpi.icon }}</div>
          </div>
        </div>

        <div class="chart-row">
          <div class="chart-card">
            <div class="chart-header">
              <div>
                <div class="chart-title">Crescimento de Utilizadores</div>
                <div class="chart-sub">Ao longo do ano</div>
              </div>
              <div class="chart-legend">
                <div class="legend-item"><span class="legend-dot" style="background:#c9a96e"></span> Utilizadores</div>
              </div>
            </div>
            <div class="chart-wrap">
              <canvas ref="lineChartRef"></canvas>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-header">
              <div>
                <div class="chart-title">Categorias</div>
                <div class="chart-sub">Distribuição por tipo</div>
              </div>
            </div>
            <div class="chart-wrap doughnut-wrap">
              <canvas ref="doughnutChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'

//Graficos
const { Chart, registerables } = await import('chart.js')
Chart.register(...registerables)
Chart.defaults.color = MUTED
Chart.defaults.font.family = "'DM Sans', sans-serif"
Chart.defaults.font.size = 11

//Cores Graficos
const GOLD = '#c9a96e', BLUE = '#6e8fc9'
const GREEN = '#6ec97e', PINK = '#c96e8f', PURPLE = '#9b6ec9', RED = '#c96e6e'
const TEXT = '#e8e4d8', MUTED = '#6e6b5e', GRID = 'rgba(232,228,216,0.05)'


const kpis = ref([])
const route = useRoute()
const sidebarOpen = ref(false)
const firstName = ref('Manueli')


const currentMonthYear = computed(() => {
  return new Date().toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
    .replace(/^\w/, c => c.toUpperCase())
})

async function kpiCards() {
  const token = localStorage.getItem('access_token')
  if (!token) { return router.push('/') }
  try {
    const response = await fetch('http://192.168.1.83:8000/stats')

    if (!response.ok) {
      throw new Error("Erro ao buscar estatísticas")
    }

    const data = await response.json()

    kpis.value = [
      { label: 'Total de Clubes',  value: data.clubes,icon: '🏛️' },
      { label: 'Membros Ativos',   value: data.utilizadores,icon: '👥' },
      { label: 'Tipos de Utilizadores',   value: data.tipousers,icon: '✨' }
    ]
  } catch (error) {
    console.error(error)
  }
}
async function CategoriasGrafic() {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/')
    return
  }

  try {
    const response = await fetch(`http://192.168.1.83:8000/statstpuser`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error("Erro ao buscar estatísticas")
    }

    const data = await response.json()

    const labels = []
    const valores = []

    for (const key in data) {
      labels.push(key)
      valores.push(data[key])
    }

    if (doughnutChart) doughnutChart.destroy()

    doughnutChart = new Chart(doughnutChartRef.value, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: valores,
          backgroundColor: [GOLD, BLUE, RED, GREEN, PURPLE, PINK],
          borderColor: '#0a0a0f',
          borderWidth: 3,
          hoverOffset: 6
        }],
      },
      options: {
        responsive: true,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: MUTED,
              padding: 14,
              usePointStyle: true,
              pointStyleWidth: 8,
              font: { size: 11 }
            }
          },
          tooltip: {
            backgroundColor: '#13131a',
            borderColor: 'rgba(201,169,110,0.2)',
            borderWidth: 1,
            padding: 10,
            titleColor: TEXT,
            bodyColor: MUTED,
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.parsed}`
            }
          }
        }
      }
    })

  } catch (error) {
    console.error(error)
  }
}
async function UtilizadoresGrafic() {
  const token = localStorage.getItem('access_token')
  if (!token) return router.push('/login')

  const response = await fetch('http://192.168.1.83:8000/registrations', {
    headers: { Authorization: `Bearer ${token}` }
  })

  const data = await response.json()

  const labels = data.map(item => item.month)
  const valores = data.map(item => item.count)

  if (lineChart) lineChart.destroy()

  lineChart = new Chart(lineChartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Novos Registos',
        data: valores,
        borderColor: GOLD,
        backgroundColor: 'rgba(201,169,110,0.1)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: GRID } },
        y: { grid: { color: GRID } }
      }
    }
  })
}

const lineChartRef     = ref(null)
const doughnutChartRef = ref(null)
let lineChart = null, doughnutChart = null



onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) { await router.push('/login'); return }

  kpiCards();
  CategoriasGrafic();
  UtilizadoresGrafic();

})

onBeforeUnmount(() => {
  lineChart?.destroy()
  doughnutChart?.destroy()
})
onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/login'); return }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.layout {
  --gold:      #c9a96e;
  --gold-l:    #e8c97e;
  --gold-dim:  rgba(201,169,110,0.12);
  --bg:        #0a0a0f;
  --surface:   rgba(255,255,255,0.03);
  --border:    rgba(232,228,216,0.08);
  --border-g:  rgba(201,169,110,0.15);
  --text:      #e8e4d8;
  --muted:     #6e6b5e;
  --faint:     #4a4840;
  --sidebar-w: 240px;
}

.layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  overflow-x: hidden;
}

.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(110px); }
.orb-1 { width: 500px; height: 500px; background: var(--gold); opacity: .07; top: -180px; left: 40px; }
.orb-2 { width: 350px; height: 350px; background: #6e8fc9;     opacity: .06; bottom: 0;   right: 10%; }
.orb-3 { width: 280px; height: 280px; background: #c96e8f;     opacity: .05; top: 40%;    right: -60px; }

.sidebar-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.55);
  z-index: 99;
  backdrop-filter: blur(2px);
}

.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: rgba(10,10,15,0.92);
  border-right: 1px solid var(--border-g);
  backdrop-filter: blur(16px);
  display: flex; flex-direction: column;
  z-index: 100;
  padding: 0 0 2rem;
  transition: transform 0.3s ease;
}
.sidebar-logo {
  display: flex; align-items: center; gap: .5rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  padding: 1.8rem 1.5rem 1.5rem;
  border-bottom: 1px solid var(--border-g);
}
.sidebar-logo .icon { color: var(--gold); }
.sidebar-logo em { font-style: italic; color: var(--gold); }
.sidebar-section {
  font-size: .65rem; letter-spacing: .12em;
  text-transform: uppercase; color: var(--faint);
  padding: 1.4rem 1.5rem .5rem;
}
.nav-item {
  display: flex; align-items: center; gap: .75rem;
  padding: .65rem 1.5rem;
  font-size: .875rem; color: var(--muted);
  text-decoration: none;
  transition: color .2s, background .2s;
  position: relative;
}
.nav-item:hover { color: var(--text); background: rgba(255,255,255,.03); }
.nav-item.active { color: var(--gold); background: var(--gold-dim); }
.nav-item.active::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(to bottom, var(--gold), var(--gold-l));
}
.nav-item svg { flex-shrink: 0; opacity: .7; }
.nav-item.active svg { opacity: 1; }

.main {
  margin-left: var(--sidebar-w);
  width: calc(100% - var(--sidebar-w));
  min-width: 0;
  flex: 1;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: hidden;
}

.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.4rem 2rem;
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px);
  background: rgba(10,10,15,.5);
  position: sticky; top: 0; z-index: 50;
  gap: 1rem;
  width: 100%;
}
.topbar-left {
  display: flex; align-items: center; gap: 1rem;
  min-width: 0; flex: 1;
}
.topbar-left h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.6rem; font-weight: 300; white-space: nowrap;
}
.topbar-left p { font-size: .8rem; color: var(--muted); margin-top: .1rem; white-space: nowrap; }
.topbar-right { display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }

.btn-menu {
  display: none;
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  align-items: center; justify-content: center;
  cursor: pointer; color: var(--muted); flex-shrink: 0;
  transition: color .2s, border-color .2s;
}
.btn-menu:hover { color: var(--gold); border-color: var(--border-g); }

.badge-date {
  font-size: .75rem; color: var(--muted);
  border: 1px solid var(--border-g);
  padding: .3rem .8rem; border-radius: 100px;
  text-transform: capitalize; white-space: nowrap;
}

.content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  min-width: 0;
  max-width: 1600px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.2rem;
  width: 100%;
}
.kpi-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 1.4rem 1.6rem;
  position: relative; overflow: hidden;
  transition: border-color .25s, transform .25s;
  animation: fadeUp .5s ease both;
  min-width: 0;
}
.kpi-card:nth-child(1) { animation-delay:.05s; }
.kpi-card:nth-child(2) { animation-delay:.10s; }
.kpi-card:nth-child(3) { animation-delay:.15s; }
.kpi-card:hover { border-color: var(--border-g); transform: translateY(-2px); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.kpi-card.k1::before { background: linear-gradient(90deg,#c9a96e,#e8c97e); }
.kpi-card.k2::before { background: linear-gradient(90deg,#6e8fc9,#7eaee8); }
.kpi-card.k3::before { background: linear-gradient(90deg,#6ec97e,#7ee89a); }
.kpi-card.k4::before { background: linear-gradient(90deg,#c96e8f,#e87ea0); }
.kpi-label { font-size:.7rem; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:.6rem; }
.kpi-value { font-family:'Cormorant Garamond',serif; font-size:2.6rem; font-weight:600; line-height:1; }
.kpi-unit { font-size:1.2rem; font-weight:300; color:var(--muted); }
.kpi-footer { display:flex; align-items:center; gap:.4rem; margin-top:.7rem; }
.kpi-delta { display:inline-flex; align-items:center; padding:.15rem .5rem; border-radius:100px; font-size:.7rem; font-weight:500; }
.kpi-delta.up   { background:rgba(110,201,126,.12); color:#6ec97e; }
.kpi-delta.down { background:rgba(201,110,110,.12); color:#c96e6e; }
.kpi-icon { position:absolute; bottom:1rem; right:1.2rem; font-size:2.2rem; opacity:.08; }

.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.2rem;
  width: 100%;
  min-width: 0;
}
.chart-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:16px; padding:1.5rem;
  transition:border-color .25s;
  min-width: 0;
  overflow: hidden;
}
.chart-card:hover { border-color:var(--border-g); }
.chart-header { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:1.4rem; flex-wrap:wrap; gap:.5rem; }
.chart-title { font-family:'Cormorant Garamond',serif; font-size:1.2rem; font-weight:400; }
.chart-sub { font-size:.75rem; color:var(--muted); margin-top:.1rem; }
.chart-legend { display:flex; gap:.8rem; flex-wrap:wrap; }
.legend-item { display:flex; align-items:center; gap:.35rem; font-size:.72rem; color:var(--muted); }
.legend-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.chart-wrap { position:relative; width:100%; }
.chart-wrap canvas { max-width:100%; display:block; }
.doughnut-wrap { max-width: 260px; margin: 0 auto; }

@keyframes fadeUp   { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:none; } }
@keyframes slideIn  { from { opacity:0; transform:translateX(-16px); } to { opacity:1; transform:none; } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:none; } }

@media (max-width: 1099px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.open {
    transform: translateX(0);
  }

  .main {
    margin-left: 0;
    width: 100%;
  }

  .btn-menu { display: flex; }

  .topbar { padding: 1rem 1.5rem; }

  .content { padding: 1.5rem; gap: 1.2rem; }

  .kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
  }

  .chart-row { grid-template-columns: 1fr; }
  .doughnut-wrap { max-width: 280px; }
}

@media (max-width: 768px) {
  .topbar { padding: 1rem 1.2rem; }
  .topbar-left p { display: none; }
  .badge-date { display: none; }

  .content { padding: 1rem; gap: 1rem; }

  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .8rem;
  }
  .kpi-value { font-size: 2rem; }
  .kpi-icon  { font-size: 1.6rem; }

  .chart-row { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .topbar-left h1 { font-size: 1.25rem; }

  .content { padding: .75rem; gap: .75rem; }

  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .6rem;
  }
  .kpi-card  { padding: 1rem 1.1rem; }
  .kpi-value { font-size: 1.7rem; }
  .kpi-label { font-size: .62rem; }
  .kpi-icon  { font-size: 1.4rem; }

  .chart-card { padding: 1rem; }
  .doughnut-wrap { max-width: 220px; }
}
</style>