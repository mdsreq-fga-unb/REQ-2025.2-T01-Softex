# 🔐 Configuração do Google SSO

Guia completo para configurar autenticação via Google no backend.

---

## 📋 **O que foi Implementado**

✅ Endpoint `/api/auth/google/` para login via Google  
✅ Validação de token do Google  
✅ Criação automática de usuário no primeiro login  
✅ CORS configurado para frontend  
✅ Suporte a múltiplos domínios  

---

## 🚀 **Passos para Configurar**

### **1️⃣ Instalar Novas Dependências**

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Isso instala:
- `google-auth` - Autenticação Google
- `google-auth-oauthlib` - OAuth2
- `django-cors-headers` - CORS

---

### **2️⃣ Obter Google Client ID**

1. Acesse o **Google Cloud Console**:  
   https://console.cloud.google.com/

2. Crie um novo projeto ou selecione um existente

3. Vá em **APIs & Services** → **Credentials**

4. Clique em **+ CREATE CREDENTIALS** → **OAuth client ID**

5. Configure:
   - **Application type**: Web application
   - **Name**: Backend Softex
   - **Authorized JavaScript origins**:
     ```
     http://localhost:3000
     http://localhost:5173
     http://localhost:8080
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:3000
     http://localhost:5173
     http://localhost:8080
     ```

6. Clique em **CREATE**

7. **Copie o Client ID** (algo como `123456789-abcdef.apps.googleusercontent.com`)

---

### **3️⃣ Configurar Variável de Ambiente**

Adicione no arquivo `.env` do backend:

```env
# Google OAuth
GOOGLE_CLIENT_ID=seu-client-id-aqui.apps.googleusercontent.com
```

**Exemplo completo do `.env`:**

```env
SECRET_KEY=sua-chave-secreta
DEBUG=True

DB_NAME=softex_db
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# NOVO: Google Client ID
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
```

---

## 🌐 **Endpoint de Login Google**

### **URL**
```
POST http://localhost:8000/api/auth/google/
```

### **Requisição**
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMzQ1Njc4OTBhYmNkZWYifQ..."
}
```

### **Resposta de Sucesso (200 OK)**
```json
{
  "message": "Login realizado com sucesso!",
  "user": {
    "id": 1,
    "username": "felipe",
    "email": "felipe@gmail.com",
    "first_name": "Felipe",
    "last_name": "Pedroza",
    "tipo_permissao": "colaborador"
  },
  "is_new_user": false
}
```

### **Resposta de Erro (401 Unauthorized)**
```json
{
  "error": "Token inválido ou expirado",
  "details": "Token verification failed"
}
```

---

## 🎨 **Integração com Frontend (Vue.js)**

### **1. Instalar Google Sign-In**

```bash
npm install @react-oauth/google
# ou
npm install vue3-google-login
```

### **2. Exemplo de Código Vue.js**

```vue
<template>
  <div>
    <button @click="loginComGoogle">
      Login com Google
    </button>
  </div>
</template>

<script setup>
import { googleTokenLogin } from 'vue3-google-login'

const loginComGoogle = async () => {
  try {
    // Obter token do Google
    const response = await googleTokenLogin({
      clientId: 'SEU-CLIENT-ID.apps.googleusercontent.com'
    })
    
    // Enviar token para o backend
    const backendResponse = await fetch('http://localhost:8000/api/auth/google/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token: response.credential  // Token do Google
      })
    })
    
    const data = await backendResponse.json()
    
    if (backendResponse.ok) {
      console.log('Login sucesso:', data.user)
      // Salvar usuário no estado/localStorage
      localStorage.setItem('user', JSON.stringify(data.user))
      // Redirecionar
      router.push('/dashboard')
    } else {
      console.error('Erro:', data.error)
    }
  } catch (error) {
    console.error('Erro no login:', error)
  }
}
</script>
```

### **3. Alternativa: Google Identity Services (mais simples)**

```html
<!-- No index.html -->
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

```vue
<template>
  <div>
    <div 
      id="g_id_onload"
      data-client_id="SEU-CLIENT-ID.apps.googleusercontent.com"
      data-callback="handleCredentialResponse"
    ></div>
    <div class="g_id_signin" data-type="standard"></div>
  </div>
</template>

<script>
window.handleCredentialResponse = async (response) => {
  // Enviar token para backend
  const res = await fetch('http://localhost:8000/api/auth/google/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: response.credential })
  })
  
  const data = await res.json()
  console.log('Usuário:', data.user)
}
</script>
```

---

## 🔒 **Como Funciona**

1. **Frontend**: Usuário clica em "Login com Google"
2. **Google**: Abre popup de autenticação
3. **Usuário**: Autoriza acesso
4. **Google**: Retorna token JWT para o frontend
5. **Frontend**: Envia token para `/api/auth/google/`
6. **Backend**: Valida token com Google
7. **Backend**: Busca ou cria usuário no banco
8. **Backend**: Retorna dados do usuário
9. **Frontend**: Salva usuário e redireciona

---

## 🧪 **Testando Manualmente**

### **1. Obter Token de Teste**

Vá em: https://developers.google.com/oauthplayground

1. Selecione **Google OAuth2 API v2**
2. Marque `https://www.googleapis.com/auth/userinfo.email`
3. Clique em **Authorize APIs**
4. Faça login com sua conta Google
5. Clique em **Exchange authorization code for tokens**
6. Copie o `id_token`

### **2. Testar no Backend**

```powershell
$body = @{
    token = "SEU-TOKEN-AQUI"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/google/" `
    -Method Post -Body $body -ContentType "application/json"
```

---

## 🔧 **Configurações Adicionais**

### **CORS Configurado**

O backend já está configurado para aceitar requisições de:
- `http://localhost:3000` (React/Vite)
- `http://localhost:5173` (Vite padrão)
- `http://localhost:8080` (Vue CLI)

Para adicionar mais origens, edite `backend/core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://seu-dominio.com",  # Adicione aqui
]
```

### **Modo Produção**

Em produção, adicione o domínio real:

```python
CORS_ALLOWED_ORIGINS = [
    "https://softex.com",
    "https://www.softex.com",
]
```

E no Google Console, adicione as URLs de produção.

---

## ⚠️ **Segurança**

✅ **Boas Práticas Implementadas:**
- Token validado diretamente com Google
- Email verificado obrigatório
- Usuário criado sem senha (apenas SSO)
- Erros genéricos (não expõe detalhes)

❌ **NÃO COMMITAR:**
- `.env` (contém GOOGLE_CLIENT_ID)
- Client Secret (não é necessário no backend)

---

## 📊 **Fluxo de Dados**

```
┌─────────┐      ┌────────┐      ┌─────────┐      ┌──────────┐
│ Usuario │─────▶│ Google │─────▶│Frontend │─────▶│ Backend  │
└─────────┘      └────────┘      └─────────┘      └──────────┘
    (1)            (2)               (3)              (4)
  Clica          Autentica         Recebe           Valida
   Login                            Token            Token
                                       │                │
                                       │                ▼
                                       │          ┌──────────┐
                                       │          │PostgreSQL│
                                       │          └──────────┘
                                       │                │
                                       │◀───────────────┘
                                       │      Retorna User
                                       ▼
                                  Salva User
                                  Redireciona
```

---

## 📝 **Checklist de Configuração**

- [ ] Criar projeto no Google Cloud Console
- [ ] Obter Client ID
- [ ] Adicionar `GOOGLE_CLIENT_ID` no `.env`
- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Rodar servidor: `python manage.py runserver`
- [ ] Configurar frontend com Client ID
- [ ] Testar login

---

## 🐛 **Problemas Comuns**

### **Erro: "Token inválido"**
- Verifique se o `GOOGLE_CLIENT_ID` no `.env` está correto
- Token pode ter expirado (duram ~1 hora)
- Client ID do frontend deve ser o mesmo do backend

### **Erro: CORS**
- Adicione a origem do frontend em `CORS_ALLOWED_ORIGINS`
- Certifique-se de que `corsheaders` está instalado
- Reinicie o servidor

### **Erro: "Email não verificado"**
- O usuário precisa ter email verificado no Google
- Peça para verificar o email na conta Google

---

## 📚 **Recursos Úteis**

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google OAuth Docs](https://developers.google.com/identity/protocols/oauth2)
- [Django CORS Headers](https://pypi.org/project/django-cors-headers/)

---

**Criado para o projeto Softex - UnB 2025** 🚀

