# shadcn-vue - Configuração Completa

Este projeto está configurado com **shadcn-vue**, uma biblioteca de componentes reutilizáveis e acessíveis para Vue 3.

## 🎨 O que foi configurado

### Dependências instaladas:
- **Tailwind CSS** - Framework CSS utility-first
- **radix-vue** - Componentes primitivos de UI acessíveis
- **class-variance-authority** - Para variantes de componentes
- **clsx** e **tailwind-merge** - Utilitários para classes CSS
- **lucide-vue-next** - Ícones (opcional)

### Estrutura criada:
```
frontend/
├── src/
│   ├── components/
│   │   └── ui/
│   │       └── button/        # Exemplo de componente
│   │           ├── Button.vue
│   │           └── index.ts
│   ├── lib/
│   │   └── utils.ts          # Função cn() para merge de classes
│   └── assets/
│       └── index.css         # Estilos Tailwind + variáveis CSS
├── components.json           # Configuração do shadcn-vue
├── tailwind.config.js        # Configuração do Tailwind
└── postcss.config.js         # Configuração do PostCSS
```

## 🚀 Como usar

### 1. Importar componentes:
\`\`\`vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<template>
  <Button>Clique aqui</Button>
  <Button variant="secondary">Botão secundário</Button>
  <Button variant="outline" size="lg">Botão grande</Button>
</template>
\`\`\`

### 2. Criar novos componentes UI:

Você pode criar novos componentes seguindo o padrão do Button:

1. Crie uma pasta em `src/components/ui/[nome-componente]`
2. Crie o arquivo `.vue` com o componente
3. Crie o `index.ts` com as variantes usando `cva`
4. Use a função `cn()` de `@/lib/utils` para merge de classes

### 3. Adicionar mais componentes do shadcn-vue:

Visite a documentação oficial e copie os componentes que precisa:
- [shadcn-vue.com](https://www.shadcn-vue.com/)

Os componentes são copiados para seu projeto (não é uma dependência npm), então você tem controle total sobre o código.

## 🎨 Customização

### Cores e temas:
Edite as variáveis CSS em `src/assets/index.css` para personalizar:
- Cores primárias e secundárias
- Modo escuro
- Raio de borda (border-radius)
- E muito mais...

### Tailwind:
Configure classes personalizadas em `tailwind.config.js`

## 📦 Componentes disponíveis no shadcn-vue:

Você pode adicionar componentes como:
- Button ✅ (já instalado)
- Card
- Dialog / Modal
- Dropdown Menu
- Form / Input
- Table
- Tabs
- Toast / Notification
- E muitos mais...

## 🌐 Executar o projeto:

\`\`\`bash
npm run dev
\`\`\`

## 📚 Recursos:

- [shadcn-vue Docs](https://www.shadcn-vue.com/)
- [Radix Vue](https://www.radix-vue.com/)
- [Tailwind CSS](https://tailwindcss.com/)

