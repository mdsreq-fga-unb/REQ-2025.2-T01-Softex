# 🚀 Softex - Sistema de Gestão de Recursos

Documentação do sistema de gestão de recursos físicos da Softex.

## 📋 Sobre o Projeto

A Softex (Associação para Promoção da Excelência do Software Brasileiro) desenvolveu um sistema para gestão eficiente de recursos físicos em ambiente híbrido, resolvendo os desafios organizacionais de coordenação entre atividades presenciais e remotas.

## 🏗️ Estrutura do Projeto

Construído com Starlight

Dentro do projeto Astro + Starlight, você verá as seguintes pastas e arquivos:

```
./docs-astro
├── public/
├── src/
│   ├── assets/
│   ├── content/
│   │   └── docs/
│   └── styles/
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

O Starlight procura por arquivos `.md` ou `.mdx` no diretório `src/content/docs/`. Cada arquivo é exposto como uma rota baseada em seu nome.

Imagens podem ser adicionadas em `src/assets/` e incorporadas no Markdown com um link relativo.

Assets estáticos, como favicons, podem ser colocados no diretório `public/`.

## 🧞 Comandos

Todos os comandos são executados a partir da raiz do projeto, em um terminal:

| Comando              | Ação                                        |
| -------------------- | ------------------------------------------- |
| pnpm install         | Instala as dependências                     |
| pnpm dev             | Inicia o servidor local em localhost:4321   |
| pnpm build           | Constrói o site de produção em ./dist/      |
| pnpm preview         | Visualiza sua build localmente, antes de fazer deploy |
| pnpm astro ...       | Executa comandos CLI como astro add, astro check |
| pnpm astro -- --help | Obtém ajuda usando a CLI do Astro           |

## 🎨 Identidade Visual

O projeto utiliza a identidade visual da Softex:
- **Cor principal:** Roxo (#8B5CF6)
- **Modo escuro:** Fundo preto com texto branco
- **Modo claro:** Fundo branco com texto preto
- **Destaques:** Elementos em roxo para manter a identidade da marca

## 👀 Quer saber mais?

Confira a [documentação do Starlight](https://starlight.astro.build/), leia a [documentação do Astro](https://docs.astro.build/).

## 📄 Sobre

Sistema de gestão de recursos físicos desenvolvido para a Softex como parte da disciplina de Engenharia de Requisitos.

### Recursos

- [Documentação Online](https://mdsreq-fga-unb.github.io/REQ-2025.2-T01-Softex/)
- [Repositório GitHub](https://github.com/mdsreq-fga-unb/REQ-2025.2-T01-Softex)