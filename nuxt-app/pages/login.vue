<template>
 <div class="bg-layer">
    <div class="noise"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
  </div>

  <div class="layout">

    <div class="panel-left">
      <a href="/" id="homelink">
      <div class="brand">
        <span class="brand-icon">✦</span>
        <span class="brand-name">Manueli's <em>Clubes</em></span>
      </div>
      </a>

      <div class="panel-copy">
        <h1 class="panel-title">Entre no seu<br /><span class="gold-italic">universo</span></h1>
        <p class="panel-sub">Clubes exclusivos, conexões reais e experiências inesquecíveis esperam por si.</p>
      </div>
    </div>

    <div class="panel-right">
      <div class="form-card">

        <div class="form-header">
          <div class="form-badge">Acesso à plataforma</div>
          <h2 class="form-title">Iniciar Sessão</h2>
          <p class="form-sub">Preencha os seus dados para continuar</p>
        </div>

        <form class="form-body" id="loginForm" @submit.prevent="fazerLogin">

          <div class="field" id="field-username">
            <label class="field-label" for="username">Username</label>
            <div class="input-wrap">
              <input id="username" name="username" type="text" class="field-input" placeholder="O seu username" v-model="username" />
            </div>
          </div>

          <div class="field" id="field-password">
            <label class="field-label" for="password">Password</label>
            <div class="input-wrap">
              <input id="password" name="password" type="password" class="field-input" placeholder="Password" v-model="password"/>
              <button type="button" class="input-toggle" id="togglePassword" tabindex="-1" aria-label="Mostrar password">
              </button>
            </div>
          </div>
          <div class="field" id="field-tpUser">
            <label class="field-label" for="tpUser">Tipo de Utilizador</label>
            <div class="input-wrap">
              <span class="input-icon">
              </span>
              <select id="tpUser" name="tpUser" class="field-select" v-model="tpUser">
                <option value="-1">Escolha uma opção</option>
              </select>
            </div>
            <span class="field-error">Selecione o tipo de utilizador.</span>
          </div>


          <button @click="fazerLogin" class="btn-submit" id="btnSubmit">
            <span class="loader"></span>
            <span class="btn-text">Entrar</span>
          </button>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const router = useRouter()
const username = ref('')
const password = ref('')
const tpUser = ref('-1')

async function fazerLogin() {
  if (!username.value || !password.value || tpUser.value === '-1') {
      return Swal.fire({
      title: 'warning',
      text: 'Preenche todos os campos obrigatórios.',
      icon: 'warning',
      confirmButtonText: 'Ok'
    })
  }
  

  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)
    formData.append('tipo_id', Number(tpUser.value))

    const response = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
            return Swal.fire({
      title: 'Erro!',
      text: 'Credenciais inválidas.',
      icon: 'error',
      confirmButtonText: 'Ok'
    })
    }

    const data = await response.json()
    localStorage.setItem('access_token', data.access_token)

    router.push('/dashboard')
  } catch (err) {
    console.error(err)
    alert('Erro ao comunicar com a API')
  }
}
async function listarTipoUser() {
  const url = `http://localhost:8000/tipouser`;

  try {
    const response = await fetch(url, { method: "GET" });

    if (!response.ok) {
      throw new Error("Erro ao obter tipoUser: " + response.statusText);
    }

    const dados = await response.json();
    const select = document.querySelector("#tpUser");
    select.innerHTML = '<option value="-1">Escolha uma opção</option>';

    if (!Array.isArray(dados)) {
      alert("Resposta inesperada da API.");
      return;
    }

    dados.forEach(c => {
      const option = `<option value="${c.id}">${c.descricao}</option>`;
      select.innerHTML += option;
    });

  } catch (error) {
    console.error(error);
    alert("Erro ao carregar tipos de utilizador.");
  }
}
onMounted(() => {
  listarTipoUser();
});
</script>
<style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --gold: #c9a96e;
      --gold-light: #e8c97e;
      --bg: #0a0a0f;
      --text: #e8e4d8;
      --muted: #6e6b5e;
      --faint: #4a4840;
      --dimmer: #3d3b35;
      --error: #c96e6e;
    }

    body {
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      font-weight: 300;
      overflow-x: hidden;
    }
    #homelink
    {
      text-decoration: none;
      color: inherit;
    }
    .bg-layer {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
    }
    .orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(100px);
    }
    .orb-1 { width: 600px; height: 600px; background: var(--gold);  opacity: 0.1;  top: -200px; left: -150px; }
    .orb-2 { width: 400px; height: 400px; background: #6e8fc9;      opacity: 0.08; bottom: -100px; right: 30%; }
    .orb-3 { width: 350px; height: 350px; background: #c96e8f;      opacity: 0.07; top: 20%; right: -100px; }

    .layout {
      position: relative;
      z-index: 1;
      min-height: 100vh;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }

    .panel-left {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 3rem 4rem;
      border-right: 1px solid rgba(201, 169, 110, 0.1);
      animation: fadeUp 0.5s ease both;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.3rem;
    }
    .brand-icon { color: var(--gold); }
    .brand-name em { font-style: italic; color: var(--gold); }

    .panel-copy {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 1.2rem;
    }
    .panel-title {
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(2.8rem, 4.5vw, 4.5rem);
      font-weight: 300;
      line-height: 1.1;
      letter-spacing: -0.01em;
    }
    .gold-italic { font-style: italic; color: var(--gold); }
    .panel-sub {
      font-size: 0.95rem;
      line-height: 1.7;
      color: var(--muted);
      max-width: 380px;
    }

    .panel-stats {
      display: flex;
      align-items: center;
      gap: 2rem;
      padding: 1.5rem 0;
      border-top: 1px solid rgba(201, 169, 110, 0.12);
    }
    .pstat { text-align: left; }
    .pstat-num {
      display: block;
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.8rem;
      font-weight: 600;
      color: var(--gold);
    }
    .pstat-label {
      font-size: 0.7rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--faint);
    }
    .pstat-sep {
      width: 1px;
      height: 36px;
      background: rgba(201, 169, 110, 0.15);
    }

    .panel-right {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3rem 4rem;
      animation: fadeUp 0.5s 0.15s ease both;
    }

    .form-card {
      width: 100%;
      max-width: 420px;
    }

    .form-header {
      margin-bottom: 2.2rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }
    .form-badge {
      display: inline-block;
      border: 1px solid rgba(201, 169, 110, 0.35);
      color: var(--gold);
      font-size: 0.7rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.3rem 0.9rem;
      border-radius: 100px;
      width: fit-content;
    }
    .form-title {
      font-family: 'Cormorant Garamond', serif;
      font-size: 2.2rem;
      font-weight: 300;
    }
    .form-sub {
      font-size: 0.85rem;
      color: var(--muted);
    }

    .form-body {
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }
    .field-label {
      font-size: 0.78rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #9d9a8e;
    }

    .input-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }
    .input-icon {
      position: absolute;
      left: 0.9rem;
      color: var(--faint);
      display: flex;
      align-items: center;
      pointer-events: none;
    }
    .field-input,
    .field-select {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(232, 228, 216, 0.1);
      border-radius: 10px;
      padding: 0.85rem 1rem 0.85rem 1rem;
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      font-size: 0.9rem;
      font-weight: 300;
      outline: none;
      transition: border-color 0.2s, background 0.2s;
      appearance: none;
      -webkit-appearance: none;
    }
    .field-input::placeholder { color: var(--dimmer); }
    .field-input:focus,
    .field-select:focus {
      border-color: rgba(201, 169, 110, 0.5);
      background: rgba(201, 169, 110, 0.04);
    }
    .field-select { cursor: pointer; }
    .field-select option { background: #1a1a1f; color: var(--text); }

    .input-toggle {
      position: absolute;
      background: none;
      border: none;
      color: var(--faint);
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 0;
      transition: color 0.2s;
    }
    .input-toggle:hover { color: var(--gold); }

    .select-arrow {
      position: absolute;
      right: 0.9rem;
      color: var(--faint);
      pointer-events: none;
      display: flex;
      align-items: center;
    }

    .field.has-error .field-input,
    .field.has-error .field-select {
      border-color: rgba(201, 90, 90, 0.5);
    }
    .field-error {
      font-size: 0.75rem;
      color: var(--error);
      padding-left: 0.2rem;
      display: none;
    }
    .field.has-error .field-error { display: block; }

    .api-error {
      display: none;
      align-items: center;
      gap: 0.5rem;
      background: rgba(201, 110, 110, 0.08);
      border: 1px solid rgba(201, 110, 110, 0.25);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      font-size: 0.85rem;
      color: var(--error);
    }
    .api-error.visible { display: flex; }

    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, var(--gold), var(--gold-light));
      color: var(--bg);
      border: none;
      padding: 1rem;
      border-radius: 10px;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      transition: opacity 0.2s, transform 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 50px;
      letter-spacing: 0.03em;
      margin-top: 0.4rem;
      position: relative;
    }
    .btn-submit:hover { opacity: 0.9; transform: translateY(-1px); }
    .btn-submit:active { transform: translateY(0); }
    .btn-submit:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    .btn-submit .loader {
      display: none;
      width: 18px;
      height: 18px;
      border: 2px solid rgba(10, 10, 15, 0.3);
      border-top-color: var(--bg);
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
    }
    .btn-submit.loading .loader { display: block; }
    .btn-submit.loading .btn-text { display: none; }

    .form-footer {
      margin-top: 1.5rem;
      text-align: center;
      font-size: 0.85rem;
      color: var(--faint);
      display: flex;
      gap: 0.4rem;
      justify-content: center;
    }
    .form-link {
      color: var(--gold);
      text-decoration: none;
      transition: opacity 0.2s;
    }
    .form-link:hover { opacity: 0.8; }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(18px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; }
      .panel-left {
        padding: 2.5rem 2rem 2rem;
        border-right: none;
        border-bottom: 1px solid rgba(201, 169, 110, 0.1);
      }
      .panel-copy { padding: 2rem 0; }
      .panel-right { padding: 2.5rem 2rem; }
    }
  </style>