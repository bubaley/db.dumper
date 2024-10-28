<template>
    <dialog class="modal" :class="{ 'modal-open': model }" @click="model = false">
        <div class="modal-box" @click.stop>
            <h3 class="text-lg font-bold">Hello!</h3>
            <p class="py-4">Press ESC key or click outside to close</p>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button>close</button>
        </form>
    </dialog>
</template>

<script setup lang="ts">
const model = defineModel<boolean>()
</script>

<style scoped>

</style>
