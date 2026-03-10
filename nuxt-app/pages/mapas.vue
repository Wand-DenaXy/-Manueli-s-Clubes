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
      <NuxtLink to="/dashboard" class="nav-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </NuxtLink>
      <NuxtLink to="/clubes" class="nav-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Clubes
      </NuxtLink>
      <NuxtLink to="/mapas" class="nav-item active">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>
        Mapas
      </NuxtLink>
      <NuxtLink to="/calendario" class="nav-item">
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
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <div>
            <h1>Mapas</h1>
            <p>Localização geográfica dos clubes registados ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="badge-date">{{ currentMonthYear }}</span>
          <button class="btn-toggle-panel" @click="panelOpen = !panelOpen" :class="{ active: panelOpen } " v-if="podeEditar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Novo ponto
          </button>
        </div>
      </header>

      <div class="map-layout">

        <aside class="clubs-panel">
          <div class="panel-tabs">
            <button class="panel-tab" :class="{ active: activeTab === 'clubes' }" @click="activeTab = 'clubes'">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
              Clubes
              <span class="tab-badge">{{ clubes.length }}</span>
            </button>
            <button class="panel-tab" :class="{ active: activeTab === 'pontos' }" @click="activeTab = 'pontos'">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/><circle cx="12" cy="9" r="2"/></svg>
              Pontos
              <span class="tab-badge">{{ pontos.length }}</span>
            </button>
          </div>
          <template v-if="activeTab === 'clubes'">

            <div class="clubs-list">
              <div
                v-for="clube in filteredClubes"
                :key="clube.id"
                class="club-item"
                :class="{ active: selectedClube?.id === clube.id }"
                @click="focusClube(clube)"
              >
                <div class="club-item-dot" :style="{ background: clube.color }"></div>
                <div class="club-item-info">
                  <span class="club-item-name">{{ clube.nome }}</span>
                  <span class="club-item-loc">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/><circle cx="12" cy="9" r="2"/></svg>
                    {{ clube.localidade }}
                  </span>
                </div>
                <div v-if="clube.lat && clube.lng" class="club-item-coords">
                  <span>{{ Number(clube.lat).toFixed(3) }}</span>
                  <span>{{ Number(clube.lng).toFixed(3) }}</span>
                </div>
                <div v-else class="club-item-no-coords">sem coords</div>
              </div>
              <div v-if="filteredClubes.length === 0" class="clubs-empty">
                Nenhum clube encontrado
              </div>
            </div>
          </template>

          <template v-else>


            <div v-if="loadingPontos" class="pontos-loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>
              A carregar…
            </div>

            <div v-else class="clubs-list">
              <div
                v-for="ponto in filteredPontos"
                :key="ponto.id"
                class="ponto-item"
                :class="{ active: selectedPonto?.id === ponto.id }"
                @click="focusPonto(ponto)"
              >
                <div class="ponto-item-icon" :style="{ color: getClubeColor(ponto.clube_id) }">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/></svg>
                </div>
                <div class="club-item-info">
                  <span class="club-item-name">{{ ponto.descricao }}</span>
                  <span class="club-item-loc ponto-clube-name">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                    {{ getClubeName(ponto.clube_id) }}
                  </span>
                </div>
                <div class="club-item-coords">
                  <span>{{ Number(ponto.latitude).toFixed(3) }}</span>
                  <span>{{ Number(ponto.longitude).toFixed(3) }}</span>
                </div>
              </div>

              <div v-if="filteredPontos.length === 0 && !loadingPontos" class="clubs-empty">
                Nenhum ponto encontrado
              </div>
            </div>

            <div v-if="filteredPontos.length > 0" class="pontos-footer">
              <span>{{ filteredPontos.length }} ponto{{ filteredPontos.length !== 1 ? 's' : '' }}</span>
              <button class="btn-refresh" @click="carregarPontos" title="Atualizar">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>
                Atualizar
              </button>
            </div>
          </template>
        </aside>
        <div class="map-container">
          <div id="leaflet-map" ref="mapRef"></div>

          <div v-if="addingPoint" class="map-hint">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Clica no mapa para colocar o ponto
          </div>
        </div>
        <transition name="panel-slide">
          <div v-if="panelOpen" class="add-panel">
            <div class="add-panel-header">
              <div>
                <span class="panel-chip">Novo ponto</span>
                <h3 class="add-panel-title">Registar <em>localização</em></h3>
              </div>
              <button class="btn-close-panel" @click="panelOpen = false">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="add-panel-divider"></div>

            <div class="add-field">
              <label class="add-label">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                Clube associado <span class="req">*</span>
              </label>
              <select v-model.number="newPoint.clube_id" class="add-select">
                <option value="" disabled>Seleciona um clube…</option>
                <option v-for="c in clubes" :key="c.id" :value="c.id">{{ c.nome }}</option>
              </select>
            </div>

            <div class="add-field">
              <label class="add-label">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/><circle cx="12" cy="9" r="2"/></svg>
                Nome / descrição
              </label>
              <input v-model="newPoint.descricao" type="text" placeholder="Ex: Sede principal" class="add-input" />
            </div>

            <div class="add-coords-row">
              <div class="add-field">
                <label class="add-label">Latitude <span class="req">*</span></label>
                <input v-model="newPoint.lat" type="number" step="0.000001" placeholder="38.7169" class="add-input" />
              </div>
              <div class="add-field">
                <label class="add-label">Longitude <span class="req">*</span></label>
                <input v-model="newPoint.lng" type="number" step="0.000001" placeholder="-9.1399" class="add-input" />
              </div>
            </div>

            <button class="btn-pick" :class="{ active: addingPoint }" @click="togglePickMode">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
              {{ addingPoint ? 'A aguardar clique no mapa…' : 'Escolher no mapa' }}
            </button>

            <div class="add-panel-divider"></div>

            <button class="btn-save-point" @click="guardarPonto" :disabled="savingPoint">
              <svg v-if="!savingPoint" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
              <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>
              {{ savingPoint ? 'A guardar…' : 'Guardar Ponto' }}
            </button>

            <p class="add-note">O ponto ficará associado ao clube seleccionado e visível no mapa imediatamente.</p>
          </div>
        </transition>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import Swal from 'sweetalert2'

const router = useRouter()
const sidebarOpen = ref(false)
const panelOpen = ref(false)
const addingPoint = ref(false)
const savingPoint = ref(false)
const searchQuery = ref('')
const filterClubeId = ref('')
const tipo_id = ref(null)
const clubes = ref([])
const isAdmin = computed(() => tipo_id.value === 1)
const isGestor = computed(() => tipo_id.value === 2)
const podeEditar = computed(() => isAdmin.value || isGestor.value)
const pontos = ref([])
const selectedClube = ref(null)
const selectedPonto = ref(null)
const activeTab = ref('clubes')
const loadingPontos = ref(false)

const BASE_URL = 'http://localhost:8000'

const PALETTE = ['#c9a96e','#6e8fc9','#6ec97e','#c96e8f','#9b6ec9','#c96e6e','#6ec9c9','#c9b96e']

const newPoint = ref({ clube_id: '', descricao: '', lat: '', lng: '' })

const currentMonthYear = computed(() =>
  new Date().toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
    .replace(/^\w/, c => c.toUpperCase())
)

const filteredClubes = computed(() =>
  clubes.value.filter(c =>
    c.nome.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (c.localidade || '').toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const filteredPontos = computed(() => {
  let list = pontos.value
  if (filterClubeId.value) {
    list = list.filter(p => p.clube_id === filterClubeId.value)
  }
  return list
})

function getClubeName(clube_id) {
  return clubes.value.find(c => String(c.id) === String(clube_id))?.nome || '—'
}

function getClubeColor(clube_id) {
  return clubes.value.find(c => String(c.id) === String(clube_id))?.color || '#c9a96e'
}

let pickStyleEl = null
let L = null
let map = null
let markersLayer = null
let pontosLayer = null
let tempMarker = null

async function initMap() {
  if (map) return
  L = (await import('leaflet')).default
  await import('leaflet/dist/leaflet.css')

  delete L.Icon.Default.prototype._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  })

  map = L.map('leaflet-map', {
    center: [38.570578, -7.917666],
    zoom: 7,
    zoomControl: false,
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors © CARTO',
    maxZoom: 19,
  }).addTo(map)

  L.control.zoom({ position: 'bottomright' }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
  pontosLayer = L.layerGroup().addTo(map)

  map.on('click', (e) => {
    if (!addingPoint.value) return
    const { lat, lng } = e.latlng
    newPoint.value.lat = lat.toFixed(6)
    newPoint.value.lng = lng.toFixed(6)
    addingPoint.value = false
    removePick()

    if (tempMarker) map.removeLayer(tempMarker)
    tempMarker = L.circleMarker([lat, lng], {
      radius: 8, color: '#c9a96e', fillColor: '#c9a96e',
      fillOpacity: 0.9, weight: 2,
    }).addTo(map).bindPopup('Ponto seleccionado').openPopup()
  })
}

function makeIcon(color) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="38" viewBox="0 0 28 38">
    <path d="M14 0C6.27 0 0 6.27 0 14c0 9.33 14 24 14 24s14-14.67 14-24C28 6.27 21.73 0 14 0z" fill="${color}" opacity="0.92"/>
    <circle cx="14" cy="14" r="6" fill="#0a0a0f" opacity="0.6"/>
    <circle cx="14" cy="14" r="3" fill="${color}"/>
  </svg>`
  return L.divIcon({
    html: svg,
    iconSize: [28, 38],
    iconAnchor: [14, 38],
    popupAnchor: [0, -38],
    className: '',
  })
}

function makePontoIcon(color) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="30" viewBox="0 0 22 30">
    <path d="M11 0C4.93 0 0 4.93 0 11c0 7.33 11 19 11 19s11-11.67 11-19C22 4.93 17.07 0 11 0z" fill="${color}" opacity="0.75"/>
    <circle cx="11" cy="11" r="4" fill="#0a0a0f" opacity="0.5"/>
    <circle cx="11" cy="11" r="2" fill="${color}"/>
  </svg>`
  return L.divIcon({
    html: svg,
    iconSize: [22, 30],
    iconAnchor: [11, 30],
    popupAnchor: [0, -30],
    className: '',
  })
}

function renderMarkers() {
  if (!map || !markersLayer) return
  markersLayer.clearLayers()

  clubes.value.forEach(clube => {
    if (!clube.lat || !clube.lng) return
    const lat = parseFloat(clube.lat)
    const lng = parseFloat(clube.lng)
    if (isNaN(lat) || isNaN(lng)) return

    const marker = L.marker([lat, lng], { icon: makeIcon(clube.color) })
    marker.bindPopup(`
      <div style="font-family:'DM Sans',sans-serif;min-width:160px;padding:4px 0">
        <div style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#6e6b5e;margin-bottom:.3rem">Clube</div>
        <div style="font-size:1rem;font-family:'Cormorant Garamond',serif;color:#e8e4d8;margin-bottom:.4rem">${clube.nome}</div>
        <div style="display:flex;align-items:center;gap:.3rem;font-size:.75rem;color:#9d9a8e">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7z"/><circle cx="12" cy="9" r="2"/></svg>
          ${clube.localidade || '—'}
        </div>
        <div style="margin-top:.5rem;font-size:.7rem;color:#4a4840">${lat.toFixed(5)}, ${lng.toFixed(5)}</div>
      </div>
    `, { className: 'leaflet-popup-dark', maxWidth: 220 })
    markersLayer.addLayer(marker)
  })
}

function renderPontos() {
  if (!map || !pontosLayer) return
  pontosLayer.clearLayers()

  pontos.value.forEach(ponto => {
    const lat = parseFloat(ponto.latitude)
    const lng = parseFloat(ponto.longitude) 
    if (isNaN(lat) || isNaN(lng)) return

    const color = getClubeColor(ponto.clube_id)
    const clubeNome = getClubeName(ponto.clube_id)

    const marker = L.marker([lat, lng], { icon: makePontoIcon(color) })
    marker.bindPopup(`
      <div style="font-family:'DM Sans',sans-serif;min-width:160px;padding:4px 0">
        <div style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#6e6b5e;margin-bottom:.3rem">Ponto</div>
        <div style="font-size:1rem;font-family:'Cormorant Garamond',serif;color:#e8e4d8;margin-bottom:.4rem">${ponto.descricao || 'Sem nome'}</div>
        <div style="display:flex;align-items:center;gap:.3rem;font-size:.75rem;color:#9d9a8e;margin-bottom:.25rem">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          ${clubeNome}
        </div>
        <div style="font-size:.7rem;color:#4a4840">${lat.toFixed(5)}, ${lng.toFixed(5)}</div>
      </div>
    `, { className: 'leaflet-popup-dark', maxWidth: 220 })
    pontosLayer.addLayer(marker)
  })
}

function focusPonto(ponto) {
  selectedPonto.value = ponto
  const lat = parseFloat(ponto.latitude)
  const lng = parseFloat(ponto.longitude)
  if (!map || isNaN(lat) || isNaN(lng)) return
  map.flyTo([lat, lng], 15, { duration: 1.2 })

  pontosLayer.eachLayer(layer => {
    const pos = layer.getLatLng()
    if (Math.abs(pos.lat - lat) < 0.0001 && Math.abs(pos.lng - lng) < 0.0001) {
      layer.openPopup()
    }
  })
}

function togglePickMode() {
  addingPoint.value = !addingPoint.value

  if (addingPoint.value) {
    pickStyleEl = document.createElement('style')
    pickStyleEl.id = 'pick-mode-style'
    pickStyleEl.textContent = `
      #leaflet-map,
      #leaflet-map *,
      #leaflet-map .leaflet-grab,
      #leaflet-map .leaflet-interactive,
      #leaflet-map .leaflet-container {
        cursor: crosshair !important;
      }
    `
    document.head.appendChild(pickStyleEl)
  } else {
    removePick()
  }
}

function removePick() {
  const el = document.getElementById('pick-mode-style')
  if (el) el.remove()
  pickStyleEl = null
}

async function carregarClubes() {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(`${BASE_URL}/clubes`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) return
    const dados = await res.json()
    if (!Array.isArray(dados)) return
    clubes.value = dados.map((c, i) => ({
      ...c,
      color: PALETTE[i % PALETTE.length],
    }))
    renderMarkers()
    if (pontos.value.length) renderPontos()
  } catch (e) {
    console.error(e)
  }
}

async function carregarPontos() {
  const token = localStorage.getItem('access_token')
  loadingPontos.value = true
  try {
    const res = await fetch(`${BASE_URL}/mapas`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) return
    const dados = await res.json()
    if (!Array.isArray(dados)) return
    pontos.value = dados
    renderPontos()
  } catch (e) {
    console.error(e)
  } finally {
    loadingPontos.value = false
  }
}

async function guardarPonto() {
  if (!newPoint.value.clube_id) {
    return Swal.fire({ title: 'Erro', text: 'Seleciona um clube.', icon: 'error', confirmButtonText: 'Ok' })
  }
  if (!newPoint.value.lat || !newPoint.value.lng) {
    return Swal.fire({ title: 'Erro', text: 'Define as coordenadas (clica no mapa ou preenche manualmente).', icon: 'error', confirmButtonText: 'Ok' })
  }

  savingPoint.value = true
  const token = localStorage.getItem('access_token')

  try {
    const res = await fetch(`${BASE_URL}/mapas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ clube_id: Number(newPoint.value.clube_id), descricao: newPoint.value.descricao, latitude: parseFloat(newPoint.value.lat),longitude: parseFloat(newPoint.value.lng),
      
      })
    })
    if (res.ok) {
      await Swal.fire({ title: 'Guardado!', text: 'Ponto adicionado com sucesso.', icon: 'success', confirmButtonText: 'Ok' })
      newPoint.value = {clube_id: '',descricao: '',lat: '',lng: ''}
      if (tempMarker) { map.removeLayer(tempMarker); tempMarker = null }
      panelOpen.value = false
      await carregarPontos()
      activeTab.value = 'pontos'
    } else {
      Swal.fire({ title: 'Erro', text: 'Erro ao guardar ponto: ' + res.statusText, icon: 'error', confirmButtonText: 'Ok' })
    }
  } catch (e) {
    Swal.fire({ title: 'Erro', text: e.message, icon: 'error' })
  } finally {
    savingPoint.value = false
  }
}

watch(panelOpen, () => {
  nextTick(() => { if (map) map.invalidateSize() })
})

watch(activeTab, (val) => {
  if (val === 'pontos' && pontos.value.length === 0) {
    carregarPontos()
  }
})

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/login'); return }


    try {
    const decoded = jwtDecode(token)
    tipo_id.value = Number(decoded.tipo_id)
  } catch (e) {
    router.push('/login'); return
  }
  
  await nextTick()
  await initMap()
  await carregarClubes()
  await carregarPontos()
})

onBeforeUnmount(() => {
  removePick()
  if (map) { map.remove(); map = null }
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
  overflow: hidden;
}
.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(120px); }
.orb-1 { width: 500px; height: 500px; background: var(--gold); opacity: .05; top: -200px; left: 20px; }
.orb-2 { width: 360px; height: 360px; background: #6e8fc9; opacity: .04; bottom: 0; right: 8%; }
.orb-3 { width: 280px; height: 280px; background: #c96e8f; opacity: .03; top: 45%; right: -50px; }

.sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99; backdrop-filter: blur(3px); }

.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: rgba(10,10,15,0.96);
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
.nav-item { display: flex; align-items: center; gap: .75rem; padding: .65rem 1.5rem; font-size: .875rem; color: var(--muted); text-decoration: none; transition: color .2s, background .2s; position: relative; }
.nav-item:hover { color: var(--text); background: rgba(255,255,255,.02); }
.nav-item.active { color: var(--gold); background: var(--gold-dim); }
.nav-item.active::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, var(--gold), var(--gold-l)); }
.nav-item svg { flex-shrink: 0; opacity: .65; }
.nav-item.active svg { opacity: 1; }

.main {
  margin-left: var(--sidebar-w);
  width: calc(100% - var(--sidebar-w));
  min-width: 0; flex: 1;
  position: relative; z-index: 1;
  display: flex; flex-direction: column;
  height: 100vh; overflow: hidden;
}

.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.1rem 1.8rem;
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
  background: rgba(10,10,15,.75);
  z-index: 50; gap: 1rem; flex-shrink: 0;
}
.topbar-left { display: flex; align-items: center; gap: 1rem; min-width: 0; flex: 1; }
.topbar-left h1 { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 300; white-space: nowrap; }
.topbar-left p { font-size: .76rem; color: var(--muted); margin-top: .1rem; white-space: nowrap; }
.topbar-right { display: flex; align-items: center; gap: .9rem; flex-shrink: 0; }
.btn-menu { display: none; width: 34px; height: 34px; border-radius: 50%; background: var(--surface); border: 1px solid var(--border); align-items: center; justify-content: center; cursor: pointer; color: var(--muted); flex-shrink: 0; transition: color .2s, border-color .2s; }
.btn-menu:hover { color: var(--gold); border-color: var(--border-g); }
.badge-date { font-size: .72rem; color: var(--muted); border: 1px solid var(--border-g); padding: .28rem .8rem; border-radius: 100px; white-space: nowrap; }
.btn-toggle-panel {
  display: inline-flex; align-items: center; gap: .45rem;
  background: var(--gold-dim); color: var(--gold);
  border: 1px solid var(--border-g);
  padding: .42rem 1rem; border-radius: 100px;
  font-family: 'DM Sans', sans-serif; font-size: .8rem; font-weight: 400;
  cursor: pointer; transition: background .2s, border-color .2s, color .2s; white-space: nowrap;
}
.btn-toggle-panel:hover, .btn-toggle-panel.active {
  background: rgba(201,169,110,0.18); border-color: rgba(201,169,110,0.38); color: var(--gold-l);
}

.map-layout { display: flex; flex: 1; min-height: 0; overflow: hidden; }

.clubs-panel {
  width: 270px; flex-shrink: 0;
  background: rgba(10,10,15,0.85);
  border-right: 1px solid var(--border-g);
  backdrop-filter: blur(16px);
  display: flex; flex-direction: column;
  overflow: hidden; z-index: 10;
}

.panel-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.panel-tab {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: .4rem;
  padding: .85rem .5rem;
  background: transparent; border: none;
  font-family: 'DM Sans', sans-serif; font-size: .75rem; font-weight: 400;
  color: var(--muted); cursor: pointer;
  transition: color .2s, background .2s, border-bottom .2s;
  border-bottom: 2px solid transparent;
  position: relative;
}
.panel-tab:hover { color: var(--text); background: rgba(255,255,255,.02); }
.panel-tab.active { color: var(--gold); border-bottom-color: var(--gold); background: var(--gold-dim); }

.tab-badge {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 18px; height: 16px; padding: 0 .35rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 100px; font-size: .6rem; color: var(--faint);
}
.panel-tab.active .tab-badge {
  background: var(--gold-dim); border-color: var(--border-g); color: var(--gold);
}

.clubs-search {
  display: flex; align-items: center; gap: .5rem;
  padding: .75rem 1.2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.clubs-search svg { color: var(--muted); flex-shrink: 0; }
.search-input { flex: 1; background: transparent; border: none; outline: none; color: var(--text); font-family: 'DM Sans', sans-serif; font-size: .82rem; font-weight: 300; }
.search-input::placeholder { color: var(--faint); }

.pontos-filter {
  padding: .6rem 1.2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.filter-select {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: .45rem .75rem;
  color: var(--text);
  font-family: 'DM Sans', sans-serif; font-size: .78rem; font-weight: 300;
  outline: none;
  cursor: pointer;
  transition: border-color .2s;
}
.filter-select option { background: #13131e; color: var(--text); }
.filter-select:focus { border-color: var(--border-g); }

/* Loading */
.pontos-loading {
  display: flex; align-items: center; justify-content: center; gap: .5rem;
  padding: 2rem; font-size: .8rem; color: var(--muted);
}

.clubs-list { flex: 1; overflow-y: auto; padding: .4rem 0; }
.clubs-list::-webkit-scrollbar { width: 3px; }
.clubs-list::-webkit-scrollbar-track { background: transparent; }
.clubs-list::-webkit-scrollbar-thumb { background: var(--border-g); border-radius: 2px; }

.club-item {
  display: flex; align-items: center; gap: .75rem;
  padding: .7rem 1.2rem; cursor: pointer;
  transition: background .15s;
  border-left: 2px solid transparent;
}
.club-item:hover { background: rgba(255,255,255,0.025); }
.club-item.active { background: var(--gold-dim); border-left-color: var(--gold); }

/* Ponto item */
.ponto-item {
  display: flex; align-items: center; gap: .75rem;
  padding: .7rem 1.2rem; cursor: pointer;
  transition: background .15s;
  border-left: 2px solid transparent;
}
.ponto-item:hover { background: rgba(255,255,255,0.025); }
.ponto-item.active { background: var(--gold-dim); border-left-color: var(--gold); }

.ponto-item-icon { flex-shrink: 0; display: flex; align-items: center; }
.ponto-clube-name { font-style: italic; }

.club-item-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.club-item-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: .15rem; }
.club-item-name { font-size: .82rem; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.club-item-loc { display: flex; align-items: center; gap: .25rem; font-size: .7rem; color: var(--muted); }
.club-item-coords { display: flex; flex-direction: column; align-items: flex-end; gap: .1rem; flex-shrink: 0; }
.club-item-coords span { font-size: .62rem; color: var(--faint); font-variant-numeric: tabular-nums; }
.club-item-no-coords { font-size: .62rem; color: var(--faint); font-style: italic; flex-shrink: 0; }
.clubs-empty { padding: 2rem 1.2rem; text-align: center; font-size: .8rem; color: var(--faint); }

/* Rodapé pontos */
.pontos-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: .65rem 1.2rem;
  border-top: 1px solid var(--border);
  flex-shrink: 0;
}
.pontos-footer span { font-size: .7rem; color: var(--faint); }
.btn-refresh {
  display: flex; align-items: center; gap: .35rem;
  background: transparent; border: 1px solid var(--border);
  border-radius: 6px; padding: .28rem .6rem;
  color: var(--muted); font-family: 'DM Sans', sans-serif; font-size: .68rem;
  cursor: pointer; transition: color .2s, border-color .2s, background .2s;
}
.btn-refresh:hover { color: var(--gold); border-color: var(--border-g); background: var(--gold-dim); }

.map-container { flex: 1; position: relative; min-width: 0; }
#leaflet-map { width: 100%; height: 100%; }

.map-hint {
  position: absolute; bottom: 3.5rem; left: 50%; transform: translateX(-50%);
  display: flex; align-items: center; gap: .5rem;
  background: rgba(10,10,15,0.88); border: 1px solid var(--border-g);
  padding: .55rem 1.2rem; border-radius: 100px;
  font-size: .78rem; color: var(--gold);
  backdrop-filter: blur(8px); z-index: 400; white-space: nowrap;
  animation: fadeUp .3s ease both;
}

.add-panel {
  width: 300px; flex-shrink: 0;
  background: rgba(10,10,15,0.9); border-left: 1px solid var(--border-g);
  backdrop-filter: blur(20px);
  display: flex; flex-direction: column;
  padding: 1.4rem 1.5rem; gap: 1rem;
  overflow-y: auto; z-index: 10;
}
.add-panel::-webkit-scrollbar { width: 3px; }
.add-panel::-webkit-scrollbar-thumb { background: var(--border-g); border-radius: 2px; }

.add-panel-header { display: flex; align-items: flex-start; justify-content: space-between; gap: .5rem; }
.add-panel-title { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 300; line-height: 1.2; margin-top: .35rem; }
.add-panel-title em { font-style: italic; color: var(--gold); }
.panel-chip { font-size: .62rem; letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }

.btn-close-panel {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--muted); flex-shrink: 0;
  transition: color .2s, border-color .2s;
}
.btn-close-panel:hover { color: var(--text); border-color: rgba(232,228,216,0.2); }

.add-panel-divider { height: 1px; background: var(--border); }

.add-field { display: flex; flex-direction: column; gap: .4rem; }
.add-label { display: flex; align-items: center; gap: .35rem; font-size: .62rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); transition: color .2s; }
.add-field:focus-within .add-label { color: var(--gold); }
.req { color: var(--gold); }

.add-select, .add-input {
  width: 100%; background: var(--surface2); border: 1px solid var(--border); border-radius: 9px;
  padding: .72rem .9rem; color: var(--text);
  font-family: 'DM Sans', sans-serif; font-size: .84rem; font-weight: 300;
  outline: none; transition: border-color .2s, background .2s, box-shadow .2s;
}
.add-select option { background: #13131e; color: var(--text); }
.add-select:focus, .add-input:focus {
  border-color: rgba(201,169,110,0.4); background: rgba(201,169,110,0.03); box-shadow: 0 0 0 3px rgba(201,169,110,0.06);
}
.add-input::placeholder { color: var(--faint); }
.add-coords-row { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }

.btn-pick {
  display: flex; align-items: center; justify-content: center; gap: .5rem;
  width: 100%; background: transparent; border: 1px dashed var(--border-g); border-radius: 9px;
  padding: .65rem; color: var(--muted);
  font-family: 'DM Sans', sans-serif; font-size: .8rem;
  cursor: pointer; transition: border-color .2s, color .2s, background .2s;
}
.btn-pick:hover { border-color: var(--gold); color: var(--gold); background: var(--gold-dim); }
.btn-pick.active { border-color: var(--gold); color: var(--gold); background: var(--gold-dim); border-style: solid; }

.btn-save-point {
  display: flex; align-items: center; justify-content: center; gap: .5rem;
  width: 100%; background: linear-gradient(135deg, #c9a96e, #e2c278);
  color: #0a0a0f; border: none; padding: .8rem; border-radius: 10px;
  font-family: 'DM Sans', sans-serif; font-size: .875rem; font-weight: 500;
  cursor: pointer; transition: opacity .2s, transform .2s, box-shadow .2s;
  box-shadow: 0 4px 18px rgba(201,169,110,0.3);
}
.btn-save-point:hover:not(:disabled) { opacity: .88; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(201,169,110,0.38); }
.btn-save-point:disabled { opacity: .55; cursor: not-allowed; }
.add-note { font-size: .7rem; color: var(--faint); line-height: 1.6; text-align: center; }

.panel-slide-enter-active,
.panel-slide-leave-active { transition: width .3s ease, opacity .3s ease; overflow: hidden; }
.panel-slide-enter-from,
.panel-slide-leave-to { width: 0; opacity: 0; }
.panel-slide-enter-to,
.panel-slide-leave-from { width: 300px; opacity: 1; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeUp { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }

@media (max-width: 1099px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; width: 100%; }
  .btn-menu { display: flex; }
}
@media (max-width: 768px) {
  .topbar { padding: .9rem 1rem; }
  .topbar-left p { display: none; }
  .badge-date { display: none; }
  .clubs-panel { width: 210px; }
  .add-panel { width: 260px; padding: 1rem; }
}
@media (max-width: 560px) {
  .clubs-panel { display: none; }
  .add-panel { width: 100%; position: absolute; right: 0; top: 0; bottom: 0; z-index: 20; }
}
</style>

<style>
.pick-mode,
.pick-mode .leaflet-grab,
.pick-mode .leaflet-interactive {
  cursor: crosshair !important;
}

.leaflet-popup-dark .leaflet-popup-content-wrapper {
  background: #13131e !important; border: 1px solid rgba(201,169,110,0.18) !important;
  border-radius: 12px !important; box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
  color: #e8e4d8 !important; padding: 0 !important;
}
.leaflet-popup-dark .leaflet-popup-content { margin: 12px 16px !important; }
.leaflet-popup-dark .leaflet-popup-tip { background: #13131e !important; }
.leaflet-popup-dark .leaflet-popup-close-button { color: #6e6b5e !important; font-size: 16px !important; }
.leaflet-popup-dark .leaflet-popup-close-button:hover { color: #c9a96e !important; }
.leaflet-control-zoom a { background: rgba(13,13,20,0.92) !important; border-color: rgba(201,169,110,0.2) !important; color: #c9a96e !important; backdrop-filter: blur(8px); }
.leaflet-control-zoom a:hover { background: rgba(201,169,110,0.12) !important; color: #e8c97e !important; }
.leaflet-control-attribution { background: rgba(10,10,15,0.75) !important; color: #3e3c35 !important; font-size: 10px !important; backdrop-filter: blur(4px); }
.leaflet-control-attribution a { color: #4a4840 !important; }
</style>