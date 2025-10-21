import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const increment = () => {
    count.value++
  }

  const decrement = () => {
    count.value--
  }

  const double = computed(() => count.value * 2)

  const reset = () => {
    count.value = initialValue
  }

  return {
    count,
    increment,
    decrement,
    double,
    reset
  }
}
