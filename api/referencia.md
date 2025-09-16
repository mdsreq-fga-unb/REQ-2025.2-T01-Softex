# Referência da API

## Visão Geral

Esta seção contém a documentação completa da API do projeto REQ-2025.2-T01-Softex.

## Endpoints

### Autenticação

#### POST /auth/login

Autentica um usuário no sistema.

**Parâmetros:**
- `username` (string, obrigatório): Nome de usuário
- `password` (string, obrigatório): Senha do usuário

**Resposta de Sucesso:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@exemplo.com"
  }
}
```

**Resposta de Erro:**
```json
{
  "error": "Credenciais inválidas",
  "code": 401
}
```

### Usuários

#### GET /users

Lista todos os usuários do sistema.

**Headers:**
- `Authorization: Bearer <token>`

**Resposta:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "usuario1",
      "email": "usuario1@exemplo.com",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### GET /users/{id}

Obtém informações de um usuário específico.

**Parâmetros:**
- `id` (integer, obrigatório): ID do usuário

**Resposta:**
```json
{
  "id": 1,
  "username": "usuario1",
  "email": "usuario1@exemplo.com",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Projetos

#### GET /projects

Lista todos os projetos.

**Resposta:**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Projeto Exemplo",
      "description": "Descrição do projeto",
      "status": "ativo",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 403 | Acesso negado |
| 404 | Não encontrado |
| 500 | Erro interno do servidor |

## Exemplos de Uso

### cURL

```bash
# Login
curl -X POST https://api.exemplo.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "senha"}'

# Listar usuários
curl -X GET https://api.exemplo.com/users \
  -H "Authorization: Bearer <token>"
```

### Python

```python
import requests

# Login
response = requests.post('https://api.exemplo.com/auth/login', json={
    'username': 'usuario',
    'password': 'senha'
})

token = response.json()['token']

# Listar usuários
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.exemplo.com/users', headers=headers)
users = response.json()
```

### JavaScript

```javascript
// Login
const loginResponse = await fetch('https://api.exemplo.com/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'usuario',
    password: 'senha'
  })
});

const { token } = await loginResponse.json();

// Listar usuários
const usersResponse = await fetch('https://api.exemplo.com/users', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const users = await usersResponse.json();
```

## Limitações e Considerações

### Rate Limiting

- **Limite**: 1000 requisições por hora por IP
- **Headers de resposta**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

### Paginação

Para endpoints que retornam listas, use os parâmetros:

- `page`: Número da página (padrão: 1)
- `limit`: Itens por página (padrão: 20, máximo: 100)

### Filtros

Alguns endpoints suportam filtros:

- `status`: Filtrar por status
- `created_at`: Filtrar por data de criação
- `search`: Busca textual

### Ordenação

Use o parâmetro `sort`:

- `sort=name`: Ordenar por nome
- `sort=-created_at`: Ordenar por data de criação (decrescente)

## Changelog

### v1.0.0 (2025-01-01)
- Versão inicial da API
- Endpoints de autenticação
- Endpoints de usuários
- Endpoints de projetos
