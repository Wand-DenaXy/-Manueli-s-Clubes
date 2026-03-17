<template>
      <NuxtLink v-if="isAdmin" to="/dashboard" class="nav-item" :class="{ active: route.path === '/dashboard' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </NuxtLink>
      <NuxtLink to="/clubes" class="nav-item" :class="{ active: route.path === '/clubes' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Clubes
      </NuxtLink>
      <NuxtLink to="/mapas" class="nav-item" :class="{ active: route.path === '/mapas' }">
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
      <NuxtLink to="/planos" class="nav-item" :class="{ active: route.path === '/planos' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5z"/>
          <path d="M2 17l10 5 10-5"/>
          <path d="M2 12l10 5 10-5"/>
        </svg>
        Planos
      </NuxtLink>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'

const route = useRoute()

const isAdmin = computed(() => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) return false
    return Number(jwtDecode(token).tipo_id) === 1
  } catch {
    return false
  }
})
</script>

<style scoped>
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
</style>