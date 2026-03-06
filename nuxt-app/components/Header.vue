<template>
  <header class="header">
    <div class="logo">
      <span class="logo-icon">✦</span>
      <span class="logo-text">Manueli's <em>Clubes</em></span>
    </div>
    <nav class="nav">
      <a href="aboutus" class="nav-link">Sobre nós</a>
      <a href="login" class="nav-link">
        <button class="btn-primary">Entrar</button>
      </a>
    </nav>
  </header>
</template>

<script setup>
// Nenhuma lógica extra por enquanto
</script>

<style scoped>
.header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 4rem;
  border-bottom: 1px solid rgba(201, 169, 110, 0.15);
  backdrop-filter: blur(12px);
  background: rgba(10, 10, 15, 0.6);
  position: sticky;
  top: 0;
}

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
</style>