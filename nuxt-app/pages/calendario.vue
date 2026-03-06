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
      <NuxtLink to="/mapas" class="nav-item" exact-active-class="active">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
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
            <h1>Calendário de Clubes</h1>
            <p>Clique num clube para ingressar ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="badge-date">{{ currentMonthYear }}</span>
        </div>
      </header>

      <div class="content-wrap">
        <div class="content" :class="{ 'panel-open': selectedClub }">

          <div class="meta-bar">
            <div class="meta-chip">
              <span class="meta-num">{{ events.length }}</span>
              <span class="meta-label">Clubes no calendário</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-chip">
              <span class="meta-num">{{ inscritos.length }}</span>
              <span class="meta-label">Já inscritos por si</span>
            </div>
            <div class="meta-divider"></div>
            <p class="meta-hint">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              Cada clube aparece no mês em que foi criado
            </p>
          </div>

          <div class="cal-card">
            <ClientOnly>
              <FullCalendar :options="calendarOptions" />
              <template #fallback>
                <div class="cal-skeleton">
                  <div class="skel-toolbar">
                    <div class="skel-block w-24"></div>
                    <div class="skel-block w-40"></div>
                    <div class="skel-block w-32"></div>
                  </div>
                  <div class="skel-grid">
                    <div v-for="n in 35" :key="n" class="skel-cell"></div>
                  </div>
                </div>
              </template>
            </ClientOnly>
          </div>

        </div>

        <!-- Painel lateral de detalhe do clube -->
        <Transition name="panel">
          <div v-if="selectedClub" class="detail-panel">
            <div class="panel-accent" :style="{ background: selectedClub._color }"></div>

            <div class="panel-header">
              <div class="panel-icon" :style="{ borderColor: selectedClub._color + '40', color: selectedClub._color }">🏛️</div>
              <button class="panel-close" @click="closePanel">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <div class="panel-title-block">
              <h2 class="panel-name">{{ selectedClub.nome }}</h2>
              <p class="panel-loc">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/><circle cx="12" cy="9" r="2"/></svg>
                {{ selectedClub.localidade || 'Localidade não definida' }}
              </p>
            </div>

            <div class="panel-divider"></div>

            <div class="panel-fields">
              <div v-if="selectedClub.email" class="panel-field">
                <span class="field-label">Email</span>
                <span class="field-val">{{ selectedClub.email }}</span>
              </div>
              <div v-if="selectedClub.telefone" class="panel-field">
                <span class="field-label">Telefone</span>
                <span class="field-val">{{ selectedClub.telefone }}</span>
              </div>
              <div class="panel-field">
                <span class="field-label">Criado em</span>
                <span class="field-val">{{ formatDate(selectedClub.evento_at) }}</span>
              </div>
              <div v-if="isInscrito(selectedClub.id)" class="panel-field">
                <span class="field-label">Estado</span>
                <span class="status-pill">
                  <span class="status-dot"></span>
                  Já inscrito
                </span>
              </div>
            </div>

            <div class="panel-divider"></div>

            <div class="panel-question">
              {{ isInscrito(selectedClub.id)
                ? 'Já está inscrito neste clube.'
                : `Pretende ingressar no clube ${selectedClub.nome}?` }}
            </div>

            <Transition name="fade">
              <div v-if="joinFeedback" class="feedback-msg" :class="joinFeedback.type">
                {{ joinFeedback.msg }}
              </div>
            </Transition>

            <div class="panel-actions">
              <button class="btn-cancel" @click="closePanel">Fechar</button>
              <button
                v-if="!isInscrito(selectedClub.id)"
                class="btn-join"
                :class="{ done: joinFeedback?.type === 'success' }"
                :disabled="joining || joinFeedback?.type === 'success'"
                @click="ingressar"
              >
                <span v-if="joining" class="btn-spinner"></span>
                <svg v-else-if="joinFeedback?.type !== 'success'" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <line x1="19" y1="8" x2="19" y2="14"/>
                  <line x1="22" y1="11" x2="16" y2="11"/>
                </svg>
                <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                {{ joining ? 'A ingressar…' : joinFeedback?.type === 'success' ? 'Inscrito!' : 'Ingressar' }}
              </button>
            </div>
          </div>
        </Transition>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import ptLocale from '@fullcalendar/core/locales/pt'

const BASE_URL = 'http://192.168.1.83:8000'

const route        = useRoute()
const router       = useRouter()
const sidebarOpen  = ref(false)
const selectedClub = ref(null)
const joining      = ref(false)
const joinFeedback = ref(null)
const events       = ref([])
const inscritos    = ref([])
const clubesMap    = ref({})

const PALETTE = ['#c9a96e', '#6e8fc9', '#6ec97e', '#c96e6e', '#9b6ec9', '#c96e8f']

const currentMonthYear = computed(() =>
  new Date().toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
    .replace(/^\w/, c => c.toUpperCase())
)

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('pt-PT', { day: '2-digit', month: 'long', year: 'numeric' })
}

function isInscrito(id) {
  return inscritos.value.includes(id)
}

async function fetchClubes() {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/login'); return }
  try {
    const res = await fetch(`${BASE_URL}/clubes`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (!res.ok) throw new Error()
    const data = await res.json()

    const mapa = {}
    data.forEach((clube, i) => {
      mapa[String(clube.id)] = { ...clube, _color: PALETTE[i % PALETTE.length] }
    })
    clubesMap.value = mapa

    events.value = data
      .filter(clube => clube.evento_at)
      .map((clube, i) => ({
        id:              String(clube.id),
        title:           clube.nome,
        date:            clube.evento_at.split('T')[0],
        color:           PALETTE[i % PALETTE.length],
        backgroundColor: PALETTE[i % PALETTE.length],
      }))
  } catch (e) {
    console.error('Erro ao carregar clubes', e)
  }
}

function handleEventClick({ event }) {
  const clube = clubesMap.value[String(event.id)]
  if (!clube) return
  selectedClub.value = { ...clube }
  joinFeedback.value = null
  joining.value      = false
}

function styleEvent({ el, event }) {
  const c = event.backgroundColor
  el.style.cssText = `
    border-radius:6px;
    background:${c}22;
    border:none;
    border-left:3px solid ${c};
    color:${c};
    font-size:.78rem;
    font-weight:400;
    padding:2px 6px;
    cursor:pointer;
  `
}

async function ingressar() {
  if (!selectedClub.value || joining.value) return
  joining.value      = true
  joinFeedback.value = null
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(`${BASE_URL}/clubes/${selectedClub.value.id}/ingressar`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    })
    if (res.status === 409) {
      joinFeedback.value = { type: 'warning', msg: 'Já está inscrito neste clube.' }
      inscritos.value.push(selectedClub.value.id)
      sessionStorage.setItem('clubes_inscritos', JSON.stringify(inscritos.value))
      return
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail ?? 'Erro ao ingressar')
    }
    const data = await res.json()
    inscritos.value.push(selectedClub.value.id)
    sessionStorage.setItem('clubes_inscritos', JSON.stringify(inscritos.value))
    joinFeedback.value = { type: 'success', msg: data.mensagem ?? '✦ Inscrito com sucesso!' }
    setTimeout(closePanel, 1800)
  } catch (e) {
    joinFeedback.value = { type: 'error', msg: e.message || 'Não foi possível ingressar. Tente novamente.' }
  } finally {
    joining.value = false
  }
}

function closePanel() {
  selectedClub.value = null
  joinFeedback.value = null
  joining.value      = false
}

const calendarOptions = computed(() => ({
  plugins:       [dayGridPlugin, interactionPlugin],
  initialView:   'dayGridMonth',
  locale:        ptLocale,
  headerToolbar: { left: 'prev,next today', center: 'title', right: 'dayGridMonth,dayGridWeek' },
  events:        events.value,
  eventClick:    handleEventClick,
  eventDidMount: styleEvent,
  eventDisplay:  'block',
  dayMaxEvents:  3,
  height:        'auto',
}))

onMounted(() => {
  inscritos.value = JSON.parse(sessionStorage.getItem('clubes_inscritos') || '[]')
  fetchClubes()
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
  --border-g:  rgba(201,169,110,0.18);
  --text:      #e8e4d8;
  --muted:     #6e6b5e;
  --faint:     #4a4840;
  --sidebar-w: 240px;
  --panel-w:   320px;

  display: flex; min-height: 100vh; width: 100%;
  background: var(--bg); color: var(--text);
  font-family: 'DM Sans', sans-serif; font-weight: 300;
  overflow-x: hidden;
}

.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(110px); }
.orb-1 { width: 500px; height: 500px; background: var(--gold); opacity: .07; top: -180px; left: 40px; }
.orb-2 { width: 350px; height: 350px; background: #6e8fc9; opacity: .06; bottom: 0; right: 10%; }
.orb-3 { width: 280px; height: 280px; background: #c96e8f; opacity: .05; top: 40%; right: -60px; }

.sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.55); z-index: 99; backdrop-filter: blur(2px); }

.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0; width: var(--sidebar-w);
  background: rgba(10,10,15,0.92); border-right: 1px solid var(--border-g);
  backdrop-filter: blur(16px); display: flex; flex-direction: column;
  z-index: 100; padding: 0 0 2rem; transition: transform 0.3s ease;
}
.sidebar-logo { display: flex; align-items: center; gap: .5rem; font-family: 'Cormorant Garamond', serif; font-size: 1.15rem; padding: 1.8rem 1.5rem 1.5rem; border-bottom: 1px solid var(--border-g); }
.sidebar-logo .icon { color: var(--gold); }
.sidebar-logo em { font-style: italic; color: var(--gold); }
.sidebar-section { font-size: .65rem; letter-spacing: .12em; text-transform: uppercase; color: var(--faint); padding: 1.4rem 1.5rem .5rem; }
.nav-item { display: flex; align-items: center; gap: .75rem; padding: .65rem 1.5rem; font-size: .875rem; color: var(--muted); text-decoration: none; transition: color .2s, background .2s; position: relative; }
.nav-item:hover { color: var(--text); background: rgba(255,255,255,.03); }
.nav-item.active { color: var(--gold); background: var(--gold-dim); }
.nav-item.active::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, var(--gold), var(--gold-l)); }
.nav-item svg { flex-shrink: 0; opacity: .7; }
.nav-item.active svg { opacity: 1; }

.main {
  margin-left: var(--sidebar-w);
  width: calc(100% - var(--sidebar-w));
  min-width: 0; flex: 1; position: relative; z-index: 1;
  display: flex; flex-direction: column; min-height: 100vh;
}

.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.4rem 2rem; border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px); background: rgba(10,10,15,.5);
  position: sticky; top: 0; z-index: 50; gap: 1rem; width: 100%;
}
.topbar-left { display: flex; align-items: center; gap: 1rem; min-width: 0; flex: 1; }
.topbar-left h1 { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 300; white-space: nowrap; }
.topbar-left p { font-size: .8rem; color: var(--muted); margin-top: .1rem; }
.topbar-right { display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }
.btn-menu { display: none; width: 36px; height: 36px; border-radius: 50%; background: var(--surface); border: 1px solid var(--border); align-items: center; justify-content: center; cursor: pointer; color: var(--muted); flex-shrink: 0; transition: color .2s, border-color .2s; }
.btn-menu:hover { color: var(--gold); border-color: var(--border-g); }
.badge-date { font-size: .75rem; color: var(--muted); border: 1px solid var(--border-g); padding: .3rem .8rem; border-radius: 100px; text-transform: capitalize; white-space: nowrap; }

/* Layout principal com painel lateral */
.content-wrap {
  display: flex; flex: 1; min-height: 0; overflow: hidden;
  align-items: flex-start;
}

.content {
  flex: 1; min-width: 0; padding: 2rem;
  display: flex; flex-direction: column; gap: 1.5rem;
  transition: padding-right .35s ease;
  overflow-y: auto;
}

/* Meta bar */
.meta-bar { display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap; padding: .9rem 1.4rem; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; animation: fadeUp .4s ease; }
.meta-chip { display: flex; align-items: baseline; gap: .5rem; }
.meta-num { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: var(--gold); line-height: 1; }
.meta-label { font-size: .75rem; color: var(--muted); }
.meta-divider { width: 1px; height: 24px; background: var(--border); flex-shrink: 0; }
.meta-hint { display: flex; align-items: center; gap: .35rem; font-size: .72rem; color: var(--faint); margin-left: auto; }

/* Calendário card */
.cal-card { background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 1.5rem; overflow: hidden; animation: fadeUp .5s ease .1s both; min-height: 500px; }

/* Skeleton */
.cal-skeleton { display: flex; flex-direction: column; gap: 1rem; }
.skel-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: .5rem; }
.skel-block { height: 28px; border-radius: 8px; background: rgba(255,255,255,.04); animation: shimmer 1.5s ease infinite; }
.w-24 { width: 96px; } .w-32 { width: 128px; } .w-40 { width: 160px; }
.skel-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.skel-cell { height: 80px; border-radius: 6px; background: rgba(255,255,255,.02); animation: shimmer 1.5s ease infinite; }
.skel-cell:nth-child(odd) { animation-delay: .1s; }

@keyframes shimmer { 0%, 100% { opacity: .4; } 50% { opacity: .7; } }

/* FullCalendar overrides */
:deep(.fc) { font-family: 'DM Sans', sans-serif; font-weight: 300; color: var(--text); }
:deep(.fc-theme-standard td), :deep(.fc-theme-standard th), :deep(.fc-theme-standard .fc-scrollgrid) { border-color: var(--border) !important; }
:deep(.fc-col-header-cell-cushion) { color: var(--muted); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; font-weight: 400; text-decoration: none; padding: .6rem 0; }
:deep(.fc-daygrid-day-number) { color: var(--muted); font-size: .8rem; text-decoration: none; padding: .4rem .6rem; transition: color .2s; }
:deep(.fc-daygrid-day:hover .fc-daygrid-day-number) { color: var(--gold); }
:deep(.fc-day-today) { background: rgba(201,169,110,.04) !important; }
:deep(.fc-day-today .fc-daygrid-day-number) { color: var(--gold) !important; font-weight: 500; }
:deep(.fc-toolbar-title) { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 300; color: var(--text); }
:deep(.fc-button) { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--muted) !important; font-family: 'DM Sans', sans-serif !important; font-size: .75rem !important; font-weight: 400 !important; border-radius: 8px !important; padding: .35rem .85rem !important; transition: color .2s, border-color .2s !important; box-shadow: none !important; text-transform: capitalize !important; }
:deep(.fc-button:hover), :deep(.fc-button-active) { color: var(--gold) !important; border-color: var(--border-g) !important; background: var(--gold-dim) !important; }
:deep(.fc-button:focus) { box-shadow: none !important; }
:deep(.fc-event) { cursor: pointer !important; transition: transform .15s, opacity .15s !important; }
:deep(.fc-event:hover) { transform: translateY(-1px); opacity: .9 !important; }
:deep(.fc-more-link) { color: var(--muted) !important; font-size: .72rem !important; }
:deep(.fc-daygrid-day-frame) { min-height: 80px; }
:deep(.fc-scrollgrid-sync-inner) { background: transparent !important; }

/* ── Painel lateral de detalhe ── */
.detail-panel {
  width: var(--panel-w);
  flex-shrink: 0;
  height: calc(100vh - 73px); /* altura menos topbar */
  position: sticky;
  top: 0;
  background: rgba(12,12,20,0.97);
  border-left: 1px solid var(--border-g);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}
.detail-panel::-webkit-scrollbar { width: 3px; }
.detail-panel::-webkit-scrollbar-thumb { background: var(--border-g); border-radius: 2px; }

.panel-accent { height: 3px; width: 100%; flex-shrink: 0; }

.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 1.4rem .8rem;
}
.panel-icon {
  width: 44px; height: 44px; border-radius: 12px; border: 1px solid;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem; background: rgba(255,255,255,.03);
}
.panel-close {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  color: var(--muted); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: color .2s, border-color .2s;
}
.panel-close:hover { color: var(--text); border-color: var(--border-g); }

.panel-title-block { padding: 0 1.4rem 1.2rem; }
.panel-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.4rem; font-weight: 400; color: var(--text); line-height: 1.2;
}
.panel-loc {
  display: flex; align-items: center; gap: .3rem;
  font-size: .75rem; color: var(--muted); margin-top: .3rem;
}

.panel-divider { height: 1px; background: var(--border); margin: 0 1.4rem; }

.panel-fields {
  padding: 1rem 1.4rem;
  display: flex; flex-direction: column; gap: .75rem;
}
.panel-field { display: flex; flex-direction: column; gap: .2rem; }
.field-label { font-size: .62rem; letter-spacing: .1em; text-transform: uppercase; color: var(--faint); }
.field-val { font-size: .85rem; color: var(--text); word-break: break-all; }

.status-pill {
  display: inline-flex; align-items: center; gap: .3rem;
  padding: .2rem .65rem; border-radius: 100px; font-size: .7rem;
  background: rgba(110,201,126,.1); color: #6ec97e;
  width: fit-content;
}
.status-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }

.panel-question {
  padding: .8rem 1.4rem;
  font-size: .85rem; color: var(--muted); line-height: 1.6;
}

.feedback-msg {
  margin: 0 1.4rem .4rem;
  padding: .5rem .9rem; border-radius: 8px; font-size: .78rem;
}
.feedback-msg.success { background: rgba(110,201,126,.1); color: #6ec97e; border: 1px solid rgba(110,201,126,.2); }
.feedback-msg.warning { background: rgba(201,169,110,.1); color: var(--gold); border: 1px solid var(--border-g); }
.feedback-msg.error   { background: rgba(201,110,110,.1); color: #c96e6e; border: 1px solid rgba(201,110,110,.2); }

.panel-actions {
  display: flex; gap: .6rem;
  padding: .8rem 1.4rem 1.6rem;
  margin-top: auto;
}
.btn-cancel {
  flex: 1; padding: .7rem; border-radius: 10px;
  border: 1px solid var(--border); background: var(--surface);
  color: var(--muted); font-family: 'DM Sans', sans-serif;
  font-size: .82rem; font-weight: 300; cursor: pointer;
  transition: color .2s, border-color .2s;
}
.btn-cancel:hover { color: var(--text); border-color: var(--border-g); }
.btn-join {
  flex: 2; padding: .7rem .9rem; border-radius: 10px;
  border: 1px solid var(--border-g); background: var(--gold-dim);
  color: var(--gold); font-family: 'DM Sans', sans-serif;
  font-size: .82rem; font-weight: 400; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: .45rem;
  transition: background .2s, box-shadow .2s;
}
.btn-join:hover:not(:disabled) { background: rgba(201,169,110,.22); box-shadow: 0 0 18px rgba(201,169,110,.15); }
.btn-join.done { background: rgba(110,201,126,.1); border-color: rgba(110,201,126,.3); color: #6ec97e; }
.btn-join:disabled { cursor: not-allowed; opacity: .75; }
.btn-spinner {
  width: 13px; height: 13px; border-radius: 50%;
  border: 2px solid rgba(201,169,110,.3); border-top-color: var(--gold);
  animation: spin .6s linear infinite; flex-shrink: 0;
}

/* Transição do painel */
.panel-enter-active { transition: width .35s ease, opacity .3s ease; overflow: hidden; }
.panel-leave-active { transition: width .3s ease, opacity .25s ease; overflow: hidden; }
.panel-enter-from, .panel-leave-to { width: 0; opacity: 0; }
.panel-enter-to, .panel-leave-from { width: var(--panel-w); opacity: 1; }

.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }
.fade-enter-from,   .fade-leave-to     { opacity: 0; }

@keyframes spin   { to { transform: rotate(360deg); } }
@keyframes fadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }

@media (max-width: 1099px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; width: 100%; }
  .btn-menu { display: flex; }
  .topbar { padding: 1rem 1.5rem; }
  .content { padding: 1.5rem; }
}
@media (max-width: 768px) {
  .topbar { padding: 1rem 1.2rem; }
  .topbar-left p { display: none; }
  .badge-date { display: none; }
  .content { padding: 1rem; gap: 1rem; }
  .cal-card { padding: .75rem; }
  .meta-hint { display: none; }
  .content-wrap { flex-direction: column; }
  .detail-panel {
    width: 100% !important;
    height: auto;
    position: relative;
    border-left: none;
    border-top: 1px solid var(--border-g);
  }
  .panel-enter-from, .panel-leave-to { width: 100%; height: 0; opacity: 0; }
}
</style>