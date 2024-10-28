<template>
  <dialog
    class="modal"
    :class="{ 'modal-open': modelValue }"
    :open="modelValue"
    @click.self="noBackdropDismiss ? void 0 : closeModal()"
    @keyup.esc="noEscDismiss ? void 0 : closeModal()"
    ref="modalRef"
  >
    <div class="modal-box">
      <slot></slot>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const modelValue = defineModel<boolean>()
const modalRef = ref<HTMLDialogElement | null>(null)

const props = defineProps<{
  noBackdropDismiss?: boolean
  noEscDismiss?: boolean
  noFocus?: boolean
}>()

const closeModal = () => {
  modelValue.value = false
}

watch(modelValue, v => {
  if (v && modalRef.value && !props.noFocus) modalRef.value.focus()
})
</script>

<style scoped>
dialog {
  border-color: unset !important;
}
</style>
