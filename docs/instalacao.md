# Instalação

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Instalação das Dependências

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/REQ-2025.2-T01-Softex.git
cd REQ-2025.2-T01-Softex
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

## Verificação da Instalação

Para verificar se tudo foi instalado corretamente:

```bash
mkdocs --version
```

Você deve ver a versão do MkDocs instalada.

## Executando o Servidor de Desenvolvimento

Para visualizar a documentação localmente:

```bash
mkdocs serve
```

A documentação estará disponível em: `http://127.0.0.1:8000`

## Construindo a Documentação

Para gerar os arquivos estáticos da documentação:

```bash
mkdocs build
```

Os arquivos serão gerados na pasta `site/`.

## Deploy para GitHub Pages

Para fazer deploy da documentação para o GitHub Pages:

```bash
mkdocs gh-deploy
```

## Solução de Problemas

### Erro de Permissão

Se encontrar erros de permissão no Windows:

```bash
# Execute o PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependências em Conflito

Se houver conflitos de dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problemas com Git

Se o comando `mkdocs gh-deploy` falhar:

```bash
# Configure o Git se ainda não foi feito
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```
