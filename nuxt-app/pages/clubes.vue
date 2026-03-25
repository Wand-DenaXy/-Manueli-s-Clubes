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
<<<<<<< Updated upstream
      <NavBar />
=======
      ${isAdmin
      <NuxtLink to="/dashboard" class="nav-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </NuxtLink>
        : ''
        }
      <NuxtLink to="/clubes" class="nav-item active">
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
    <NuxtLink to="/calendario" class="nav-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        Calendário
    </NuxtLink>
>>>>>>> Stashed changes
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
            <h1>Clubes</h1>
            <p>Crie, edite e gira todos os clubes da plataforma ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="badge-date">{{ currentMonthYear }}</span>
        </div>
      </header>

      <div class="content">

        <div class="create-card">
          <div class="create-card-header">
            <div class="create-card-header-left">
              <span class="section-chip">✦ Novo clube</span>
              <h2 class="section-title">Adicionar <em>um clube</em></h2>
            </div>
            <p class="section-desc">Preenche os campos abaixo para registar um novo clube na plataforma.</p>
          </div>

          <div class="form-divider"></div>

          <div class="form-grid">
            <div class="input-group">
              <label class="input-label" for="nome">
                <svg width="12" height="12" viewBox="0 0 20 20" fill="none"><path d="M10 2a4 4 0 100 8 4 4 0 000-8zM4 14s-2 0-2 2v1h16v-1c0-2-2-2-2-2s-1.5 2-6 2-6-2-6-2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                Nome do Clube
              </label>
              <div class="input-wrapper">
                <input type="text" id="nome" placeholder="Ex: Clube Desportivo do Porto" class="input-field" />
                <span class="input-focus-line"></span>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label" for="email">
                <svg width="12" height="12" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="12" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M2 7l8 5 8-5" stroke="currentColor" stroke-width="1.5"/></svg>
                Email
              </label>
              <div class="input-wrapper">
                <input type="email" id="email" placeholder="email@clube.pt" class="input-field" />
                <span class="input-focus-line"></span>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label" for="telefone">
                <svg width="12" height="12" viewBox="0 0 20 20" fill="none"><path d="M3 4a1 1 0 011-1h2.5a1 1 0 011 .75l.75 3a1 1 0 01-.29.97l-1.2 1.2a11 11 0 004.3 4.3l1.2-1.2a1 1 0 01.97-.29l3 .75a1 1 0 01.75 1V16a1 1 0 01-1 1C7.16 17 3 12.84 3 5a1 1 0 010-.01V4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                Telefone
              </label>
              <div class="input-wrapper">
                <input type="text" id="telefone" placeholder="+351 912 345 678" class="input-field" />
                <span class="input-focus-line"></span>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label" for="localidade">
                <svg width="12" height="12" viewBox="0 0 20 20" fill="none"><path d="M10 2a6 6 0 016 6c0 4-6 10-6 10S4 12 4 8a6 6 0 016-6z" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/></svg>
                Localidade
              </label>
              <div class="input-wrapper">
                <input type="text" id="localidade" placeholder="Lisboa, Porto, Braga…" class="input-field" />
                <span class="input-focus-line"></span>
              </div>
            </div>
          </div>

          <div class="form-footer">
            <div class="form-tips">
              <span class="tip-item"><span class="tip-dot"></span>Nome único</span>
              <span class="tip-item"><span class="tip-dot"></span>Email válido</span>
              <span class="tip-item"><span class="tip-dot"></span>Todos os campos obrigatórios</span>
            </div>
            <button class="btn-create" @click="registaClube()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              Criar Clube
            </button>
          </div>
        </div>

        <div class="table-card">
          <div class="table-card-header">
            <div class="table-card-header-left">
              <h3 class="table-card-title">Clubes Registados</h3>
              <p class="table-card-sub">Edita os campos diretamente na linha e guarda as alterações.</p>
            </div>
            <div class="table-count" id="tableCount">— clubes</div>
          </div>

          <div class="table-wrapper">
            <table id="tabelaClubes">
              <thead>
                <tr>
                  <th class="th-id">ID</th>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Localidade</th>
                  <th>Proximo Evento</th>
                  <th class="th-actions">Ações</th>
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { jwtDecode } from 'jwt-decode'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import NavBar from "~/components/Navbar.vue";

const router = useRouter()
const sidebarOpen = ref(false)
const isAdmin = computed(() => Number(getTipoFromToken()) === 1)

const currentMonthYear = computed(() =>
  new Date().toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
    .replace(/^\w/, c => c.toUpperCase())
)

const BASE_URL = 'http://localhost:8000'
const getBaseUrl = () => BASE_URL

function getTipoFromToken() {
  const token = localStorage.getItem('access_token')
  if (!token) return null
  try { return jwtDecode(token).tipo_id } catch { return null }
}

async function listarClubes() {
  const tipo_id = getTipoFromToken()
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(`${getBaseUrl()}/clubes`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) { router.push('/'); return }

    const dados = await res.json()

    const tbody = document.querySelector('#tabelaClubes tbody')
    tbody.innerHTML = ''

    dados.forEach((c, i) => {
      const isAdmin = Number(tipo_id) === 1
      tbody.innerHTML += `
        <tr style="animation: fadeUp .3s ease ${i * 0.04}s both">
          <td><span class="cell-id">${c.id}</span></td>
          <td><input id="nome_${c.id}" value="${c.nome || ''}" class="cell-input" /></td>
          <td><input id="email_${c.id}" value="${c.email || ''}" class="cell-input" /></td>
          <td><input id="tel_${c.id}" value="${c.telefone || ''}" class="cell-input" /></td>
          <td><input id="localidade_${c.id}" value="${c.localidade || ''}" class="cell-input" /></td>
          <td><input id="evento_at_${c.id}" value="${c.evento_at || ''}" class="cell-input" /></td>
          <td class="td-actions">
            ${isAdmin
              ?
              `
              <button class="btn-save" onclick="atualizarClube(${c.id})">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              Guardar
            </button> 
              <button class="btn-del" onclick="apagarClube(${c.id})">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6l-1 14H6L5 6"/>
                    <path d="M10 11v6M14 11v6"/>
                    <path d="M9 6V4h6v2"/>
                  </svg>
                  Apagar
                </button>`
              : `<span class="no-perm">Apenas admins</span>`
            }
          </td>
        </tr>`
    })
  } catch (e) { handleAjaxError(e) }
}

async function registaClube() {
  const token = localStorage.getItem('access_token')
  const nome = document.getElementById('nome').value.trim()
  const email = document.getElementById('email').value.trim()
  const telefone = document.getElementById('telefone').value.trim()
  const localidade = document.getElementById('localidade').value.trim()

  if (!nome || !email || !telefone || !localidade) {
    return Swal.fire({ title: 'Erro', text: 'Preenche todos os campos obrigatórios.', icon: 'error', confirmButtonText: 'Ok' })
  }
  try {
    const res = await fetch(`${getBaseUrl()}/clubes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ nome, email, telefone, localidade })
    })
    if (res.ok) {
      await Swal.fire({ title: 'Sucesso', text: 'Clube criado com sucesso!', icon: 'success', confirmButtonText: 'Ok' })
      ;['nome', 'email', 'telefone', 'localidade'].forEach(id => { document.getElementById(id).value = '' })
      listarClubes()
    } else {
      Swal.fire({ title: 'Erro', text: 'Erro a criar clube: ' + res.statusText, icon: 'error', confirmButtonText: 'Ok' })
    }
  } catch (e) { handleAjaxError(e) }
}

async function atualizarClube(id) {
  const token = localStorage.getItem('access_token')
  let evento = document.getElementById(`evento_at_${id}`).value

  const dados = {
    nome: document.getElementById(`nome_${id}`).value,
    email: document.getElementById(`email_${id}`).value,
    telefone: document.getElementById(`tel_${id}`).value,
    localidade: document.getElementById(`localidade_${id}`).value,
    evento_at: evento === '' ? null : evento
  }
  try {
    const res = await fetch(`${getBaseUrl()}/clubes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify(dados)
    })
    if (res.ok) {
      await Swal.fire({ title: 'Sucesso', text: 'Clube atualizado!', icon: 'success', confirmButtonText: 'Ok' })
      listarClubes()
    } else {
      Swal.fire({ title: 'Erro', text: 'Erro ao atualizar clube.', icon: 'error', confirmButtonText: 'Ok' })
    }
  } catch (e) { handleAjaxError(e) }
}

async function apagarClube(id) {
  const token = localStorage.getItem('access_token')
  const confirm = await Swal.fire({
    title: 'Tens a certeza?',
    text: 'Esta ação não pode ser revertida.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Apagar',
    cancelButtonText: 'Cancelar',
  })
  if (!confirm.isConfirmed) return
  try {
    const res = await fetch(`${getBaseUrl()}/clubes/${id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      await Swal.fire({ title: 'Apagado!', text: 'Clube removido com sucesso.', icon: 'success', confirmButtonText: 'Ok' })
      listarClubes()
    }
  } catch (e) { handleAjaxError(e) }
}

function handleAjaxError(e) {
  Swal.fire({ title: 'Erro de ligação', text: 'Erro ao comunicar com a API: ' + (e.message || 'desconhecido'), icon: 'error' })
}

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/login'); return }
  listarClubes()
  window.atualizarClube = atualizarClube
  window.apagarClube = apagarClube
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
.btn-notif { width: 34px; height: 34px; border-radius: 50%; background: var(--surface); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; cursor: pointer; position: relative; color: var(--muted); flex-shrink: 0; transition: color .2s, border-color .2s; }
.btn-notif:hover { color: var(--gold); border-color: var(--border-g); }
.notif-dot { position: absolute; top: 7px; right: 7px; width: 5px; height: 5px; border-radius: 50%; background: var(--gold); }


.content { padding: 2rem; display: flex; flex-direction: column; gap: 1.8rem; width: 100%; min-width: 0; }


.create-card {
  background: var(--surface);
  border: 1px solid var(--border-g);
  border-radius: var(--radius);
  padding: 1.8rem 2rem;
  animation: fadeUp .45s ease both;
  position: relative;
  overflow: hidden;
}
.create-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), rgba(201,169,110,0.2), transparent);
}

.create-card-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.create-card-header-left { display: flex; flex-direction: column; gap: .5rem; }
.section-chip {
  display: inline-flex; align-items: center; gap: .4rem;
  font-size: .62rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--gold); border: 1px solid var(--border-g);
  padding: .22rem .75rem; border-radius: 100px;
  width: fit-content; background: var(--gold-dim);
}
.section-title { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 300; line-height: 1.15; }
.section-title em { font-style: italic; color: var(--gold); }
.section-desc { font-size: .78rem; color: var(--muted); line-height: 1.65; max-width: 320px; text-align: right; }

.form-divider { height: 1px; background: var(--border); margin: 1.4rem 0; }

.form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }

.input-group { display: flex; flex-direction: column; gap: .5rem; }
.input-label {
  display: flex; align-items: center; gap: .4rem;
  font-size: .62rem; letter-spacing: .1em; text-transform: uppercase;
  color: var(--muted); transition: color .2s;
}
.input-group:focus-within .input-label { color: var(--gold); }

.input-wrapper { position: relative; }
.input-field {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: .85rem 1rem;
  color: var(--text);
  font-family: 'DM Sans', sans-serif; font-size: .875rem; font-weight: 300;
  outline: none;
  transition: border-color .25s, background .25s, box-shadow .25s;
}
.input-field::placeholder { color: var(--faint); }
.input-field:hover { border-color: rgba(232,228,216,0.14); }
.input-field:focus {
  border-color: rgba(201,169,110,0.4);
  background: rgba(201,169,110,0.03);
  box-shadow: 0 0 0 3px rgba(201,169,110,0.06);
}

.input-focus-line {
  position: absolute; bottom: 1px; left: 12%; right: 12%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  transform: scaleX(0);
  transition: transform .3s ease;
  border-radius: 1px;
  pointer-events: none;
}
.input-field:focus ~ .input-focus-line { transform: scaleX(1); }

.form-footer {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: 1.4rem; gap: 1rem; flex-wrap: wrap;
}
.form-tips { display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap; }
.tip-item { display: flex; align-items: center; gap: .4rem; font-size: .72rem; color: var(--faint); }
.tip-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--gold); flex-shrink: 0; opacity: .55; }

.btn-create {
  display: inline-flex; align-items: center; gap: .55rem;
  background: linear-gradient(135deg, #c9a96e 0%, #e2c278 100%);
  color: #0a0a0f; border: none;
  padding: .78rem 1.9rem; border-radius: 100px;
  font-family: 'DM Sans', sans-serif; font-size: .875rem; font-weight: 500;
  cursor: pointer; white-space: nowrap;
  transition: opacity .2s, transform .2s, box-shadow .2s;
  box-shadow: 0 4px 18px rgba(201,169,110,0.3);
}
.btn-create:hover { opacity: .9; transform: translateY(-2px); box-shadow: 0 8px 28px rgba(201,169,110,0.4); }
.btn-create:active { transform: translateY(0); }

.table-card {
  background: var(--surface);
  border: 1px solid var(--border-g);
  border-radius: var(--radius);
  overflow: hidden;
  animation: fadeUp .45s .12s ease both;
  position: relative;
}
.table-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,169,110,0.25), transparent);
}

.table-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.3rem 1.8rem;
  border-bottom: 1px solid var(--border);
  gap: 1rem;
}
.table-card-title { font-family: 'Cormorant Garamond', serif; font-size: 1.15rem; font-weight: 400; }
.table-card-sub { font-size: .72rem; color: var(--muted); margin-top: .2rem; }
.table-count {
  font-size: .7rem; color: var(--gold);
  border: 1px solid var(--border-g);
  padding: .22rem .85rem; border-radius: 100px;
  white-space: nowrap; background: var(--gold-dim); flex-shrink: 0;
}

.table-wrapper { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; font-size: .84rem; }
thead tr { background: rgba(255,255,255,0.012); }
th {
  padding: .8rem 1.4rem; text-align: left;
  font-size: .6rem; letter-spacing: .1em; text-transform: uppercase;
  color: var(--muted); font-weight: 400;
  border-bottom: 1px solid var(--border); white-space: nowrap;
}
.th-id { width: 60px; }
.th-actions { width: 190px; }

tbody tr { border-bottom: 1px solid var(--border); transition: background .15s; }
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: rgba(201,169,110,0.025); }

td { padding: .65rem 1.4rem; color: var(--text); vertical-align: middle; }

.cell-id {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 28px; height: 22px; padding: 0 .4rem;
  background: rgba(201,169,110,0.07);
  border: 1px solid var(--border-g);
  border-radius: 6px;
  font-size: .7rem; color: var(--gold);
}

.td-actions { white-space: nowrap; }

@keyframes fadeUp   { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
@keyframes slideIn  { from { opacity:0; transform:translateX(-12px); } to { opacity:1; transform:none; } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:none; } }


@media (max-width: 1299px) {
  .form-grid { grid-template-columns: repeat(2, 1fr); }
  .section-desc { text-align: left; max-width: 100%; }
  .create-card-header { flex-direction: column; align-items: flex-start; }
}

@media (max-width: 1099px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; width: 100%; }
  .btn-menu { display: flex; }
  .topbar { padding: 1rem 1.5rem; }
  .content { padding: 1.5rem; gap: 1.5rem; }
}


@media (max-width: 768px) {
  .topbar { padding: 1rem 1.2rem; }
  .topbar-left p { display: none; }
  .badge-date { display: none; }
  .content { padding: 1rem; gap: 1rem; }
  .create-card { padding: 1.3rem; }
  .form-grid { grid-template-columns: 1fr; gap: .85rem; }
  .form-footer { flex-direction: column; align-items: flex-start; }
  .btn-create { width: 100%; justify-content: center; }
  th, td { padding: .6rem .9rem; }
}


@media (max-width: 480px) {
  .topbar-left h1 { font-size: 1.2rem; }
  .content { padding: .75rem; gap: .75rem; }
  .create-card { padding: 1rem; }
  .table-card-header { flex-direction: column; align-items: flex-start; }
  .form-tips { display: none; }
}
</style>

<style>

.cell-input {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 7px;
  padding: .38rem .6rem;
  color: #e8e4d8;
  font-family: 'DM Sans', sans-serif;
  font-size: .84rem;
  font-weight: 300;
  width: 100%;
  min-width: 100px;
  outline: none;
  transition: border-color .2s, background .2s;
}
.cell-input:hover {
  border-color: rgba(232,228,216,0.07);
  background: rgba(255,255,255,0.025);
}
.cell-input:focus {
  border-color: rgba(201,169,110,0.3);
  background: rgba(201,169,110,0.03);
}

.btn-save {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  background: rgba(201,169,110,0.09);
  color: #c9a96e;
  border: 1px solid rgba(201,169,110,0.14);
  padding: .33rem .85rem;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: .74rem;
  font-weight: 400;
  cursor: pointer;
  margin-right: .4rem;
  transition: background .2s, border-color .2s, transform .15s;
}
.btn-save:hover {
  background: rgba(201,169,110,0.18);
  border-color: rgba(201,169,110,0.38);
  transform: translateY(-1px);
}
.btn-save svg { flex-shrink: 0; }

.btn-del {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  background: transparent;
  color: #9a5060;
  border: 1px solid rgba(160,70,90,0.2);
  padding: .33rem .85rem;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: .74rem;
  font-weight: 400;
  cursor: pointer;
  transition: background .2s, border-color .2s, color .2s, transform .15s;
}
.btn-del:hover {
  background: rgba(160,70,90,0.1);
  border-color: rgba(160,70,90,0.38);
  color: #c07080;
  transform: translateY(-1px);
}
.btn-del svg { flex-shrink: 0; }

.no-perm {
  font-size: .72rem;
  color: #3e3c35;
  font-style: italic;
  font-family: 'DM Sans', sans-serif;
}

@media (max-width: 768px) {
  .cell-input { min-width: 80px; font-size: .8rem; }
}
</style>