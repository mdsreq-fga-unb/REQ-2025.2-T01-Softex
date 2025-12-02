<template>
  <router-view />
</template>

<script setup lang="ts"></script>

<style>
/* ============================================
   SCROLLBAR CUSTOMIZADA - Estilo Moderno
   ============================================ */

/* Para navegadores WebKit (Chrome, Safari, Edge) */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
  border-radius: 10px;
  border: 2px solid #f1f1f1;
  transition: background 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
}

::-webkit-scrollbar-thumb:active {
  background: linear-gradient(135deg, #6d28d9 0%, #be185d 100%);
}

/* Para Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: #8b5cf6 #f1f1f1;
}

/* Scrollbar em elementos com fundo escuro */
.dark-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.dark-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.8) 0%,
    rgba(236, 72, 153, 0.8) 100%
  );
  border: 2px solid rgba(255, 255, 255, 0.05);
}

.dark-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(
    135deg,
    rgba(124, 58, 237, 0.9) 0%,
    rgba(219, 39, 119, 0.9) 100%
  );
}

/* Scrollbar mais fina para modais e cards */
.modal-scrollbar::-webkit-scrollbar,
.card-scrollbar::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.modal-scrollbar::-webkit-scrollbar-thumb,
.card-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
  border: 1px solid transparent;
  border-radius: 8px;
}

.modal-scrollbar::-webkit-scrollbar-thumb:hover,
.card-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
}

/* Scrollbar para elementos pequenos */
.small-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.small-scrollbar::-webkit-scrollbar-thumb {
  background: #c4b5fd;
  border-radius: 6px;
}

.small-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a78bfa;
}
</style>
