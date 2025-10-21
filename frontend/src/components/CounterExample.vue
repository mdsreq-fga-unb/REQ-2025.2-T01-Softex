<script setup lang="ts">
import { useCounter } from '@/composables/useCounter'

const { count, increment, decrement, double, reset } = useCounter(5)
</script>

<template>
  <div class="text-center space-y-4">
    <h2 class="text-2xl font-bold">Exemplo de Composition API</h2>

    <div class="space-y-2">
      <p class="text-lg">Contador: {{ count }}</p>
      <p class="text-sm text-gray-600">Dobro: {{ double }}</p>
    </div>

    <div class="flex gap-2 justify-center">
      <button
        @click="decrement"
        class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
      >
        -1
      </button>

      <button
        @click="reset"
        class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
      >
        Reset
      </button>

      <button
        @click="increment"
        class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        +1
      </button>
    </div>
  </div>
</template>

<style scoped>
.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-2 > * + * {
  margin-top: 0.5rem;
}
</style>
