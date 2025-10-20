<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center gap-8 bg-background">
    <div class="text-center space-y-4">
      <h1 class="text-4xl font-bold">shadcn-vue com Vue 3 + Vite</h1>
      <p class="text-muted-foreground">Biblioteca de componentes configurada com sucesso!</p>
    </div>
    
    <div class="flex flex-wrap gap-4 items-center justify-center">
      <Button>Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>

    <div class="flex gap-4 items-center">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
    </div>
  </div>
</template>

<style scoped>
</style>
