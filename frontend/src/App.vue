<script setup lang="ts">
import Auth from '@/components/pages/Auth.vue'
import Dashboard from '@/components/pages/Dashboard.vue'
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated } = useAuth()
</script>

<template>
  <Auth v-if="!isAuthenticated" />
  <Dashboard v-else />
</template>

<style scoped>

</style>
