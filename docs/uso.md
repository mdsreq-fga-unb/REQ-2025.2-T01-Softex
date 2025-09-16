# Guia de Uso

## Navegando pela Documentação

A documentação está organizada em seções principais:

### 📖 Seções Disponíveis

- **Início**: Página principal com visão geral
- **Documentação**: Guias detalhados do projeto
- **API**: Documentação técnica da API
- **Sobre**: Informações sobre o projeto

### 🔍 Busca

Use a barra de busca no topo da página para encontrar conteúdo específico.

### 📱 Navegação Mobile

A documentação é totalmente responsiva e funciona perfeitamente em dispositivos móveis.

## Funcionalidades do MkDocs

### Tema Material

Este projeto usa o tema Material para MkDocs, que oferece:

- **Modo escuro/claro**: Toggle automático baseado nas preferências do sistema
- **Navegação por abas**: Organização clara do conteúdo
- **Busca integrada**: Pesquisa rápida em todo o conteúdo
- **Código destacado**: Syntax highlighting para código
- **Ícones**: Suporte a ícones FontAwesome e Material

### Plugins Ativos

- **Git Revision Date**: Mostra a data da última modificação
- **Git Committers**: Lista os contribuidores
- **Search**: Busca integrada
- **Minify**: Otimização dos arquivos estáticos

## Personalização

### Adicionando Novas Páginas

1. Crie um novo arquivo `.md` na pasta apropriada
2. Adicione a entrada no arquivo `mkdocs.yml` na seção `nav`
3. Execute `mkdocs serve` para visualizar as mudanças

### Modificando o Tema

Edite o arquivo `mkdocs.yml` na seção `theme` para personalizar:

- Cores
- Ícones
- Funcionalidades
- Layout

### Adicionando Plugins

1. Instale o plugin: `pip install nome-do-plugin`
2. Adicione na seção `plugins` do `mkdocs.yml`
3. Configure as opções do plugin

## Comandos Úteis

```bash
# Servidor de desenvolvimento
mkdocs serve

# Servidor com auto-reload
mkdocs serve --livereload

# Construir documentação
mkdocs build

# Deploy para GitHub Pages
mkdocs gh-deploy

# Ajuda
mkdocs --help
```

## Estrutura de Arquivos

```
docs/
├── introducao.md      # Visão geral do projeto
├── instalacao.md      # Guia de instalação
└── uso.md            # Este arquivo

api/
└── referencia.md     # Documentação da API

index.md              # Página inicial
sobre.md              # Página sobre o projeto
```

## Dicas e Truques

### Markdown Avançado

- Use `===` para títulos de seção
- Use `---` para separadores
- Use `!!! note` para blocos de nota
- Use ````python` para blocos de código

### Exemplo de Bloco de Nota

!!! note "Dica Importante"
    Esta é uma dica importante sobre o uso da documentação.

### Exemplo de Código

```python
def exemplo():
    print("Olá, mundo!")
    return True
```

### Links e Referências

- [MkDocs](https://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)
