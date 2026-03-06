# Documentação - index.vue (Gestão de Clubes)

## Visão Geral

Este arquivo implementa uma aplicação web para **gestão de clubes** usando **Vue 3 + Nuxt.js**. Permite criar, listar, atualizar e apagar clubes através de uma API REST.

---

## Estrutura do Código

### 1. Template (Interface do Utilizador)

```vue
<template>
  <div>
    <h1>Gestão de Clubes</h1>
    <!-- Configuração da Base URL -->
    <label>Base URL:
      <input type="text" id="baseUrl" value="http://192.168.1.83:8000" size="40" />
    </label>
    <button @click="guardarBase()">Guardar</button>

    <!-- Formulário de Criação -->
    <h3>Novo Clube</h3>
    <input type="text" id="nome" placeholder="Nome" />
    <input type="email" id="email" placeholder="Email" />
    <input type="text" id="telefone" placeholder="Telefone" />
    <input type="text" id="localidade" placeholder="localidade" />
    <button class="primary" @click="registaClube()">Criar</button>

    <!-- Tabela de Clubes -->
    <table id="tabelaClubes">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Email</th>
          <th>Telefone</th>
          <th>Localidade</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
</template>
```

**Componentes:**
- **Base URL Input**: Campo para guardar a URL da API
- **Formulário**: Campos para criar novos clubes
- **Tabela**: Exibe os clubes com inputs para edição e botões de ação

---

### 2. Script Setup (Lógica)

#### **getBaseUrl()**
```javascript
function getBaseUrl() {
  return localStorage.getItem('baseUrl') || 'http://192.168.1.83:8000';
}
```
- Retorna a URL guardada no `localStorage`
- Se não existir, usa a URL padrão

---

#### **guardarBase()**
```javascript
function guardarBase() {
  const baseUrl = document.getElementById('baseUrl').value.trim();
  localStorage.setItem('baseUrl', baseUrl);
  alert('Base URL guardada!');
}
```
- Guarda a URL da API no browser (`localStorage`)
- Permite trocar de servidor sem alterar o código

---

#### **listarClubes()**
```javascript
async function listarClubes() {
  const base = getBaseUrl();
  const url = `${base}/clubes`;

  fetch(url)
    .then(response => response.json())
    .then(dados => {
      const tbody = document.querySelector("#tabelaClubes tbody");
      tbody.innerHTML = '';

      dados.forEach(function(c) {
        const tr = `
          <tr>
            <td>${c.id}</td>
            <td><input id="nome_${c.id}" value="${c.nome || ""}" /></td>
            <td><input id="email_${c.id}" value="${c.email || ""}" /></td>
            <td><input id="tel_${c.id}" value="${c.telefone || ""}" /></td>
            <td><input id="localidade_${c.id}" value="${c.localidade || ""}" /></td>
            <td>
              <button onclick="atualizarClube(${c.id})">Guardar</button>
              <button onclick="apagarClube(${c.id})">Apagar</button>
            </td>
          </tr>
        `;
        tbody.innerHTML += tr;
      });
    })
    .catch(handleAjaxError);
}
```

**O que faz:**
1. Obtém a base URL
2. Faz `fetch` para `GET /clubes`
3. Converte a resposta em JSON
4. Limpa a tabela (`tbody.innerHTML = ''`)
5. Para cada clube, cria uma linha com:
   - ID (apenas leitura)
   - Inputs editáveis (nome, email, telefone, localidade)
   - Botões de "Guardar" e "Apagar"

---

#### **registaClube()**
```javascript
async function registaClube() {
  const base = getBaseUrl();
  
  const nome = document.getElementById('nome').value.trim();
  const telefone = document.getElementById('telefone').value.trim();
  const email = document.getElementById('email').value.trim();
  const localidade = document.getElementById('localidade').value.trim();

  if (!nome || !email || !telefone || !localidade) {
    alert("Preenche todos os campos obrigatórios.");
    return;
  }

  try {
    const response = await fetch(`${base}/clubes`, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, email, telefone, localidade })
    });

    if (response.ok) {
      alert("Clube criado!");
      document.getElementById('nome').value = '';
      document.getElementById('email').value = '';
      document.getElementById('telefone').value = '';
      document.getElementById('localidade').value = '';
      listarClubes();
    }
  } catch (error) {
    handleAjaxError(error);
  }
}
```

**O que faz:**
1. Obtém os valores dos inputs
2. Valida se todos os campos estão preenchidos
3. Envia um `POST` com os dados em JSON
4. Se sucesso:
   - Mostra alerta
   - Limpa os inputs
   - Recarrega a tabela com `listarClubes()`
5. Se erro, chama `handleAjaxError()`

---

#### **atualizarClube(id)**
```javascript
async function atualizarClube(id) {
  const base = getBaseUrl();

  const nome = document.getElementById(`nome_${id}`).value;
  const email = document.getElementById(`email_${id}`).value;
  const telefone = document.getElementById(`tel_${id}`).value;
  const localidade = document.getElementById(`localidade_${id}`).value;

  const dados = { nome, email, telefone, localidade };

  try {
    const response = await fetch(`${base}/clubes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });

    if (response.ok) {
      alert('Clube atualizado com sucesso!');
      listarClubes();
    }
  } catch (error) {
    handleAjaxError(error);
  }
}
```

**O que faz:**
1. Obtém o ID do clube a atualizar
2. Recolhe os valores dos inputs da linha (nome_${id}, email_${id}, etc)
3. Envia um `PUT` para `PUT /clubes/{id}`
4. Se sucesso, recarrega a tabela
5. Se erro, mostra mensagem de erro

---

#### **apagarClube(id)**
```javascript
async function apagarClube(id) {
  const base = getBaseUrl();

  if (!confirm('Tem certeza que deseja apagar este clube?')) return;

  try {
    const response = await fetch(`${base}/clubes/${id}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      alert('Clube apagado com sucesso!');
      listarClubes();
    }
  } catch (error) {
    handleAjaxError(error);
  }
}
```

**O que faz:**
1. Pede confirmação ao utilizador
2. Se confirmar, envia `DELETE /clubes/{id}`
3. Se sucesso, recarrega a tabela
4. Se erro, mostra mensagem de erro

---

#### **handleAjaxError(error)**
```javascript
function handleAjaxError(error) {
  console.error('Erro:', error);
  alert('Erro ao comunicar com a API: ' + (error.message || 'desconhecido'));
}
```

Função auxiliar que:
- Mostra o erro na consola
- Alerta o utilizador com mensagem de erro

---

#### **onMounted()**
```javascript
onMounted(() => {
  window.atualizarClube = atualizarClube;
  window.apagarClube = apagarClube;
  window.guardarBase = guardarBase;
  window.registaClube = registaClube;
  window.listarClubes = listarClubes;

  document.getElementById('baseUrl').value = getBaseUrl();
  listarClubes();
});
```

**O que faz quando o componente é montado:**
1. **Expõe funções globalmente** para `onclick` funcionar (importante!)
2. Carrega a base URL guardada no campo
3. Carrega a lista de clubes

---

## Fluxo de Dados

### Criar Clube
```
Utilizador preenche form → Clica "Criar" 
→ registaClube() executa
→ POST /clubes 
→ Sucesso: limpa form + recarrega tabela
→ Erro: mostra alerta
```

### Listar Clubes
```
Página carrega 
→ onMounted() chama listarClubes()
→ GET /clubes
→ Tabela é renderizada com inputs para edição
```

### Atualizar Clube
```
Utilizador edita campo na tabela
→ Clica botão "Guardar"
→ atualizarClube(id) executa
→ PUT /clubes/{id}
→ Sucesso: recarrega tabela
→ Erro: mostra alerta
```

### Apagar Clube
```
Utilizador clica "Apagar"
→ Confirma ação
→ apagarClube(id) executa
→ DELETE /clubes/{id}
→ Sucesso: recarrega tabela
→ Erro: mostra alerta
```

---

## Métodos HTTP Usados

| Método | Endpoint | Função | Descrição |
|--------|----------|--------|-----------|
| GET | `/clubes` | `listarClubes()` | Lista todos os clubes |
| POST | `/clubes` | `registaClube()` | Cria novo clube |
| PUT | `/clubes/{id}` | `atualizarClube()` | Atualiza clube |
| DELETE | `/clubes/{id}` | `apagarClube()` | Apaga clube |

---

## Tecnologias Usadas

- **Vue 3**: Framework JavaScript
- **Nuxt.js**: Meta-framework Vue
- **Fetch API**: Requisições HTTP
- **localStorage**: Armazenamento local (base URL)
- **HTML5**: Inputs e tabelas

---

## Pontos Importantes

1. **Exposição Global de Funções**
   - Necessário para `onclick` funcionar em HTML injetado dinamicamente
   - Feito no `onMounted()` com `window.funcao = funcao`

2. **Validação**
   - Valida se campos estão preenchidos antes de criar
   - Pede confirmação antes de apagar

3. **localStorage**
   - A base URL é guardada localmente
   - Permite trocar de servidor sem alterar código

4. **Tratamento de Erros**
   - Todos os `fetch` têm `try/catch`
   - Erros são mostra ao utilizador

5. **Recarregamento de Dados**
   - Após criar/atualizar/apagar, recarrega a tabela
   - Garante dados sempre atualizados

---

## Como Usar

1. **Configurar Base URL**
   - Campo no topo da página
   - Ex: `http://192.168.1.83:8000`
   - Clicar "Guardar"

2. **Criar Clube**
   - Preencher formulário
   - Clicar "Criar"

3. **Editar Clube**
   - Clicar no campo para editar
   - Clicar "Guardar"

4. **Apagar Clube**
   - Clicar "Apagar"
   - Confirmar

---