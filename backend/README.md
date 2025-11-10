# 🏢 Backend - Sistema de Reserva de Salas Softex

Backend Django REST Framework para gerenciamento de reservas de salas e cadeiras.

## 🚀 Como Rodar o Projeto

### **Pré-requisitos**
- Python 3.8+
- PostgreSQL instalado e rodando
- Git (opcional)

---

## 📋 **Instalação (Primeira Vez)**

### 1. Criar Ambiente Virtual
```powershell
python -m venv venv
```

### 2. Ativar Ambiente Virtual
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat
```

### 3. Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e configure:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_NAME=nome_do_banco
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### 5. Criar Banco de Dados
No PostgreSQL:
```sql
CREATE DATABASE nome_do_banco;
```

### 6. Aplicar Migrações
```powershell
python manage.py migrate
```

### 7. Criar Superusuário
```powershell
python manage.py createsuperuser
```

### 8. Rodar Servidor
```powershell
python manage.py runserver
```

---

## 🎯 **Uso Diário**

### **Rodar o Servidor**

**Opção 1: Script Automático**
```powershell
.\start_server.ps1
```

**Opção 2: Manual**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

O servidor estará disponível em: **http://localhost:8000**

---

## 🌐 **Endpoints da API**

| Endpoint | Descrição | Métodos |
|----------|-----------|---------|
| `/api/` | Lista todos os endpoints | GET |
| `/api/cadastro/` | Gerenciar usuários | GET, POST, PUT, PATCH, DELETE |
| `/api/plantas/` | Gerenciar plantas/layouts | GET, POST, PUT, PATCH, DELETE |
| `/api/salas/` | Gerenciar salas | GET, POST, PUT, PATCH, DELETE |
| `/api/cadeiras/` | Gerenciar cadeiras | GET, POST, PUT, PATCH, DELETE |
| `/admin/` | Painel administrativo | GET, POST |

---

## 📊 **Estrutura do Banco de Dados**

### **Entidades Principais**

```
Cadastro (Usuário)
    ↓ (cria)
Planta (Layout do prédio)
    ↓ (contém)
Sala (Espaços)
    ↓ (possui)
Cadeira (Assentos com posição X,Y)

Cadastro + Sala → Reserva (Agendamentos)
```

### **Models Django**

- **Cadastro**: Usuários com sistema de permissões (colaborador/lider/rh/admin)
- **Planta**: Layouts de andares com imagem do mapa
- **Sala**: Salas com tipo (estação/reunião) e capacidade
- **Cadeira**: Cadeiras com posição (x,y) e status
- **Reserva**: Reservas de salas com período e status

---

## 🧪 **Testando a API**

### **1. Interface Web (DRF)**
Acesse: http://localhost:8000/api/

Navegue pelos endpoints e use os formulários HTML para testar.

### **2. Script de Teste**
```powershell
.\test_api.ps1
```

Este script cria dados de exemplo automaticamente.

### **3. cURL/Postman**
Importe a coleção de endpoints ou use cURL:

```bash
# Criar usuário
curl -X POST http://localhost:8000/api/cadastro/ \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@example.com","password":"senha123"}'
```

---

## 🔧 **Comandos Úteis**

```powershell
# Ver status das migrações
python manage.py showmigrations

# Criar novas migrações após alterar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Abrir shell Django
python manage.py shell

# Criar superusuário
python manage.py createsuperuser

# Rodar testes
python manage.py test

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

---

## 📁 **Estrutura de Pastas**

```
backend/
├── core/                 # Configurações do Django
│   ├── settings.py      # Configurações principais
│   ├── urls.py          # Rotas principais
│   └── wsgi.py          # WSGI config
├── cadastro/            # App de usuários
├── planta/              # App de plantas/layouts
├── sala/                # App de salas
├── cadeira/             # App de cadeiras
├── reserva/             # App de reservas
├── venv/                # Ambiente virtual (não commitar)
├── media/               # Uploads de imagens
├── manage.py            # CLI do Django
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não commitar)
├── .env.example         # Template de configuração
├── start_server.ps1     # Script para iniciar servidor
└── test_api.ps1         # Script de testes
```

---

## 🐛 **Problemas Comuns**

### **Erro: PostgreSQL não está rodando**
```
django.db.utils.OperationalError: connection refused
```
**Solução:** Inicie o serviço do PostgreSQL

### **Erro: SECRET_KEY not found**
**Solução:** Crie o arquivo `.env` com as configurações

### **Erro: No module named 'rest_framework'**
**Solução:** Ative o venv e rode `pip install -r requirements.txt`

---

## 📚 **Tecnologias Utilizadas**

- **Django 5.2.8** - Framework web
- **Django REST Framework 3.16.1** - API REST
- **PostgreSQL** - Banco de dados
- **Pillow 12.0.0** - Processamento de imagens
- **python-decouple** - Gerenciamento de configurações

---

## 👥 **Equipe**

Projeto desenvolvido para a disciplina de Requisitos de Software - UnB

---

## 📝 **Licença**

Este projeto é parte de um trabalho acadêmico.

