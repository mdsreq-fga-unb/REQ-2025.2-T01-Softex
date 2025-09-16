# Instruções de Uso - MkDocs + GitHub Pages

## 🚀 Configuração Inicial

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Testar Localmente

```bash
mkdocs serve
```

Acesse: `http://127.0.0.1:8000`

### 3. Configurar GitHub Pages

1. Vá para **Settings** do seu repositório no GitHub
2. Clique em **Pages** no menu lateral
3. Em **Source**, selecione **GitHub Actions**
4. Faça push das mudanças para a branch `main`

## 📝 Personalização

### Alterar Informações do Projeto

Edite o arquivo `mkdocs.yml` e altere:

```yaml
site_name: REQ-2025.2-T01-Softex  # Nome do site
site_author: Guilherme            # Seu nome
repo_name: seu-usuario/REQ-2025.2-T01-Softex  # Seu repositório
```

### Adicionar Novas Páginas

1. Crie um arquivo `.md` na pasta apropriada
2. Adicione no `mkdocs.yml` na seção `nav`
3. Execute `mkdocs serve` para testar

### Personalizar Tema

Edite a seção `theme` no `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo  # Cor principal
      accent: indigo   # Cor de destaque
```

## 🔧 Comandos Úteis

```bash
# Servidor de desenvolvimento
mkdocs serve

# Construir documentação
mkdocs build

# Deploy para GitHub Pages (manual)
mkdocs gh-deploy

# Ajuda
mkdocs --help
```

## 📁 Estrutura de Arquivos

```
REQ-2025.2-T01-Softex/
├── .github/
│   └── workflows/
│       └── docs.yml          # GitHub Actions
├── docs/                     # Documentação
│   ├── introducao.md
│   ├── instalacao.md
│   └── uso.md
├── api/                      # API Docs
│   └── referencia.md
├── mkdocs.yml               # Configuração
├── requirements.txt         # Dependências
├── index.md                 # Página inicial
├── sobre.md                 # Página sobre
└── README.md                # Info básica
```

## 🌐 Deploy Automático

O GitHub Actions está configurado para:

- Fazer build automaticamente quando houver push na branch `main`
- Deploy automático para GitHub Pages
- Suporte a pull requests para preview

## 🎨 Recursos do Tema Material

- ✅ Modo escuro/claro automático
- ✅ Busca integrada
- ✅ Navegação responsiva
- ✅ Syntax highlighting
- ✅ Ícones FontAwesome
- ✅ Plugins Git (data de modificação, contribuidores)

## 📚 Documentação Adicional

- [MkDocs](https://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)

## ❓ Solução de Problemas

### Erro de Permissão (Windows)
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependências em Conflito
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Deploy Falhou
Verifique se:
- O repositório está público
- GitHub Pages está habilitado
- O workflow está ativo nas Actions
