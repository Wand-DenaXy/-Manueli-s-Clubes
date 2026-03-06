<template>
  <div class="layout">
    <div class="bg-layer">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
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
      <NuxtLink to="/chat" class="nav-item" :class="{ active: route.path === '/chat' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Assistente
      </NuxtLink>
    </aside>

    <!-- Main -->
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
            <h1>Assistente</h1>
            <p>Pergunte o que quiser sobre os seus clubes ✦</p>
          </div>
        </div>
        <div class="topbar-right">
          <span class="status-pill">
            <span class="status-dot-live"></span>
            Online
          </span>
        </div>
      </header>

      <!-- Chat area -->
      <div class="chat-shell">

        <!-- Empty state -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-orb">✦</div>
          <p class="empty-title">Como posso ajudar?</p>
          <p class="empty-sub">Faça uma pergunta sobre os seus clubes, membros ou eventos.</p>
          <div class="suggestions">
            <button v-for="s in suggestions" :key="s" class="suggestion-chip" @click="useSuggestion(s)">{{ s }}</button>
          </div>
        </div>

        <!-- Messages -->
        <div v-else ref="scrollEl" class="messages">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="msg-row"
            :class="msg.role"
          >
            <div v-if="msg.role === 'ai'" class="avatar ai-avatar">✦</div>
            <div class="bubble" :class="msg.role">
              <span v-if="msg.typing" class="typing-dots">
                <span></span><span></span><span></span>
              </span>
              <template v-else>{{ msg.text }}</template>
            </div>
            <div v-if="msg.role === 'user'" class="avatar user-avatar">
              {{ initials }}
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="input-bar">
          <div class="input-wrap" :class="{ focused: inputFocused }">
            <textarea
              ref="textareaEl"
              v-model="userMessage"
              class="chat-input"
              placeholder="Escreva uma mensagem…"
              rows="1"
              @focus="inputFocused = true"
              @blur="inputFocused = false"
              @keydown.enter.exact.prevent="sendMessage"
              @input="autoResize"
            ></textarea>
            <button class="send-btn" :class="{ active: userMessage.trim() }" @click="sendMessage" :disabled="loading || !userMessage.trim()">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </div>
          <p class="input-hint">Enter para enviar &nbsp;·&nbsp; Shift+Enter para nova linha</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'

const route      = useRoute()
const sidebarOpen = ref(false)
const userMessage = ref('')
const messages    = ref([])
const loading     = ref(false)
const inputFocused = ref(false)
const scrollEl    = ref(null)
const textareaEl  = ref(null)

// Initials from token
const initials = (() => {
  try {
    const d = jwtDecode(localStorage.getItem('access_token') || '')
    return (d.nome || 'U').split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
  } catch { return 'U' }
})()

const suggestions = [
  'Quantos membros ativos existem?',
  'Mostra os clubes pendentes',
  'Qual o clube com mais membros?',
  'Resumo dos eventos deste mês',
]

function useSuggestion(text) {
  userMessage.value = text
  sendMessage()
}

function autoResize() {
  const el = textareaEl.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 160) + 'px'
}

async function scrollToBottom() {
  await nextTick()
  if (scrollEl.value) scrollEl.value.scrollTop = scrollEl.value.scrollHeight
}

async function sendMessage() {
  const text = userMessage.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', text })
  userMessage.value = ''
  if (textareaEl.value) textareaEl.value.style.height = 'auto'
  loading.value = true

  // Typing indicator
  messages.value.push({ role: 'ai', text: '', typing: true })
  await scrollToBottom()

  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ message: text }),
  })

  // Remove typing indicator
  messages.value.pop()

  if (!res.ok) {
    messages.value.push({ role: 'ai', text: 'Ocorreu um erro. Por favor tente novamente.' })
  } else {
    const data = await res.json()
    messages.value.push({ role: 'ai', text: data.response })
  }

  loading.value = false
  await scrollToBottom()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --gold:      #c9a96e;
  --gold-l:    #e8c97e;
  --gold-dim:  rgba(201,169,110,0.12);
  --bg:        #0a0a0f;
  --surface:   rgba(255,255,255,0.03);
  --surface-2: rgba(255,255,255,0.06);
  --border:    rgba(232,228,216,0.08);
  --border-g:  rgba(201,169,110,0.18);
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
  overflow: hidden; /* chat nunca deve ter scroll externo */
}

/* ── Orbs ── */
.bg-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(120px); }
.orb-1 { width: 500px; height: 500px; background: var(--gold); opacity: .06; top: -150px; left: 60px; }
.orb-2 { width: 350px; height: 350px; background: #6e8fc9; opacity: .05; bottom: 80px; right: 8%; }
.orb-3 { width: 260px; height: 260px; background: #c96e8f; opacity: .04; top: 45%; right: -40px; }

/* ── Overlay ── */
.sidebar-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.55);
  z-index: 99; backdrop-filter: blur(2px);
}

/* ── Sidebar ── */
.sidebar {
  position: fixed; top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: rgba(10,10,15,0.94);
  border-right: 1px solid var(--border-g);
  backdrop-filter: blur(16px);
  display: flex; flex-direction: column;
  z-index: 100; padding: 0 0 2rem;
  transition: transform 0.3s ease;
}
.sidebar-logo {
  display: flex; align-items: center; gap: .5rem;
  font-family: 'Cormorant Garamond', serif; font-size: 1.15rem;
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
  padding: .65rem 1.5rem; font-size: .875rem; color: var(--muted);
  text-decoration: none; transition: color .2s, background .2s; position: relative;
}
.nav-item:hover { color: var(--text); background: rgba(255,255,255,.03); }
.nav-item.active { color: var(--gold); background: var(--gold-dim); }
.nav-item.active::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(to bottom, var(--gold), var(--gold-l));
}
.nav-item svg { flex-shrink: 0; opacity: .7; }
.nav-item.active svg { opacity: 1; }

/* ── Main ── */
.main {
  margin-left: var(--sidebar-w);
  width: calc(100% - var(--sidebar-w));
  min-width: 0; flex: 1; position: relative; z-index: 1;
  display: flex; flex-direction: column;
  height: 100vh; overflow: hidden;
}

/* ── Topbar ── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.4rem 2.5rem;
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px);
  background: rgba(10,10,15,.6);
  flex-shrink: 0; gap: 1rem; width: 100%;
}
.topbar-left { display: flex; align-items: center; gap: 1rem; min-width: 0; flex: 1; }
.topbar-left h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.6rem; font-weight: 300; white-space: nowrap;
}
.topbar-left p { font-size: .8rem; color: var(--muted); margin-top: .1rem; }
.topbar-right { flex-shrink: 0; }

.btn-menu {
  display: none;
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  align-items: center; justify-content: center;
  cursor: pointer; color: var(--muted); flex-shrink: 0;
  transition: color .2s, border-color .2s;
}
.btn-menu:hover { color: var(--gold); border-color: var(--border-g); }

.status-pill {
  display: inline-flex; align-items: center; gap: .45rem;
  font-size: .72rem; color: var(--muted);
  border: 1px solid var(--border-g);
  padding: .3rem .85rem; border-radius: 100px;
}
.status-dot-live {
  width: 6px; height: 6px; border-radius: 50%;
  background: #6ec97e;
  box-shadow: 0 0 6px #6ec97e;
  animation: pulse-dot 2s ease infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: .4; }
}

/* ── Chat shell ── */
.chat-shell {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* ── Empty state ── */
.empty-state {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 1rem; padding: 2rem;
  animation: fadeUp .5s ease;
}
.empty-orb {
  width: 72px; height: 72px; border-radius: 50%;
  border: 1px solid var(--border-g);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; color: var(--gold);
  background: var(--gold-dim);
  box-shadow: 0 0 32px rgba(201,169,110,.08);
  margin-bottom: .5rem;
}
.empty-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.7rem; font-weight: 300; color: var(--text);
}
.empty-sub { font-size: .85rem; color: var(--muted); text-align: center; max-width: 380px; }
.suggestions {
  display: flex; flex-wrap: wrap; gap: .6rem;
  justify-content: center; margin-top: .5rem; max-width: 540px;
}
.suggestion-chip {
  padding: .45rem 1rem; border-radius: 100px;
  border: 1px solid var(--border-g);
  background: var(--surface); color: var(--muted);
  font-family: 'DM Sans', sans-serif; font-size: .78rem; font-weight: 300;
  cursor: pointer; transition: color .2s, border-color .2s, background .2s;
}
.suggestion-chip:hover {
  color: var(--gold); border-color: var(--gold);
  background: var(--gold-dim);
}

/* ── Messages ── */
.messages {
  flex: 1; overflow-y: auto;
  padding: 2rem clamp(1rem, 5vw, 3rem);
  display: flex; flex-direction: column; gap: 1.2rem;
  scroll-behavior: smooth;
}
.messages::-webkit-scrollbar { width: 4px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: var(--border-g); border-radius: 2px; }

.msg-row {
  display: flex; align-items: flex-end; gap: .75rem;
  animation: fadeUp .3s ease;
  max-width: 780px; width: 100%;
}
.msg-row.user { flex-direction: row-reverse; align-self: flex-end; }
.msg-row.ai   { align-self: flex-start; }

/* ── Avatars ── */
.avatar {
  width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: .7rem; font-weight: 500; letter-spacing: .02em;
}
.ai-avatar {
  background: var(--gold-dim); border: 1px solid var(--border-g);
  color: var(--gold); font-size: .9rem;
}
.user-avatar {
  background: rgba(110,143,201,.15); border: 1px solid rgba(110,143,201,.25);
  color: #6e8fc9; font-size: .68rem;
}

/* ── Bubbles ── */
.bubble {
  padding: .85rem 1.2rem;
  border-radius: 18px;
  font-size: .9rem; line-height: 1.65; font-weight: 300;
  max-width: min(520px, 75vw);
  word-break: break-word;
}
.bubble.user {
  background: var(--gold-dim);
  border: 1px solid var(--border-g);
  color: var(--text);
  border-bottom-right-radius: 4px;
}
.bubble.ai {
  background: var(--surface-2);
  border: 1px solid var(--border);
  color: var(--text);
  border-bottom-left-radius: 4px;
}

/* ── Typing dots ── */
.typing-dots {
  display: inline-flex; align-items: center; gap: 4px; height: 18px;
}
.typing-dots span {
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--muted);
  animation: bounce-dot .9s ease infinite;
}
.typing-dots span:nth-child(2) { animation-delay: .15s; }
.typing-dots span:nth-child(3) { animation-delay: .30s; }
@keyframes bounce-dot {
  0%, 80%, 100% { transform: translateY(0); opacity: .4; }
  40%            { transform: translateY(-5px); opacity: 1; }
}

/* ── Input bar ── */
.input-bar {
  flex-shrink: 0;
  padding: 1rem clamp(1rem, 5vw, 3rem) 1.5rem;
  border-top: 1px solid var(--border);
  background: rgba(10,10,15,.7);
  backdrop-filter: blur(12px);
  display: flex; flex-direction: column; gap: .5rem;
}
.input-wrap {
  display: flex; align-items: flex-end; gap: .75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px; padding: .75rem 1rem;
  transition: border-color .2s, box-shadow .2s;
}
.input-wrap.focused {
  border-color: var(--border-g);
  box-shadow: 0 0 0 3px rgba(201,169,110,.06);
}
.chat-input {
  flex: 1; background: none; border: none; outline: none; resize: none;
  font-family: 'DM Sans', sans-serif; font-size: .9rem;
  font-weight: 300; color: var(--text);
  line-height: 1.6; max-height: 160px; overflow-y: auto;
}
.chat-input::placeholder { color: var(--faint); }
.chat-input::-webkit-scrollbar { width: 3px; }
.chat-input::-webkit-scrollbar-thumb { background: var(--border-g); border-radius: 2px; }

.send-btn {
  width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
  background: var(--surface); border: 1px solid var(--border);
  color: var(--faint); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all .2s;
}
.send-btn.active {
  background: var(--gold-dim); border-color: var(--gold);
  color: var(--gold);
}
.send-btn.active:hover {
  background: rgba(201,169,110,.22);
  box-shadow: 0 0 12px rgba(201,169,110,.2);
}
.send-btn:disabled { cursor: not-allowed; }

.input-hint {
  font-size: .68rem; color: var(--faint);
  padding-left: .2rem; letter-spacing: .02em;
}

/* ── Animations ── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

/* ══ RESPONSIVE ══ */
@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; width: 100%; }
  .btn-menu { display: flex; }
  .topbar { padding: 1rem 1.2rem; }
  .topbar-left p { display: none; }
  .messages { padding: 1rem; }
  .input-bar { padding: .75rem 1rem 1rem; }
  .bubble { max-width: 85vw; }
}
</style>