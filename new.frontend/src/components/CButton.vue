<template>
  <button
    @click="onClick"
    class="btn disabled:cursor-not-allowed disabled:pointer-events-auto"
    :class="{ 'btn-loading': loading }"
    :disabled
  >
    <Transition>
      <span class="absolute loading" v-if="loading" />
    </Transition>
    <span class="btn-text">
      <slot v-if="$slots.default"></slot>
      <template v-else>{{ label }}</template>
    </span>
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  label?: string
  loading?: boolean
  disabled?: boolean
}>()

const emit = defineEmits<{
  (evt: 'click', value: Event): void
}>()

const onClick = (e: Event) => {
  if (props.disabled || props.loading) return
  emit('click', e)
}
</script>

<style scoped>
.btn.btn-loading .btn-text {
  opacity: 0;
  transition: opacity ease 0.25s;
}

.btn-loading {
  cursor: wait;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
