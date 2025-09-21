# Instalação

## Pré-requisitos

| Software | Versão Mínima | Link de Download |
|----------|---------------|------------------|
| **Python** | 3.8+ | [Download](https://www.python.org/downloads/) |
| **Git** | Última versão | [Download](https://git-scm.com/downloads) |
| **pip** | Última versão | [Instalação](https://pip.pypa.io/en/stable/installation/) |

## Instalação das Dependências

| Passo | Comando | Descrição |
|-------|---------|-----------|
| **1. Clone o Repositório** | `git clone https://github.com/seu-usuario/REQ-2025.2-T01-Softex.git`<br>`cd REQ-2025.2-T01-Softex` | Baixar o código fonte do projeto |
| **2. Ambiente Virtual** | **Windows:**<br>`python -m venv venv`<br>`venv\Scripts\activate`<br><br>**Linux/macOS:**<br>`python -m venv venv`<br>`source venv/bin/activate` | Criar ambiente isolado para o projeto |
| **3. Instalar Dependências** | `pip install -r requirements.txt` | Instalar todas as bibliotecas necessárias |

## Verificação e Execução

### Verificar Instalação
```bash
mkdocs --version
```
Você deve ver a versão do MkDocs instalada.

### Executar o Servidor de Desenvolvimento
```bash
mkdocs serve
```
A documentação estará disponível em: `http://127.0.0.1:8000`

### Construir a Documentação
```bash
mkdocs build
```
Os arquivos serão gerados na pasta `site/`.

### Deploy para GitHub Pages
```bash
mkdocs gh-deploy
```
A documentação será publicada no GitHub Pages.

## Solução de Problemas

### Erro de Permissão (Windows)
Se encontrar erros de permissão, execute o PowerShell como Administrador:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependências em Conflito
Se houver conflitos de dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problemas com Git
Se o comando `mkdocs gh-deploy` falhar, configure o Git:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```
