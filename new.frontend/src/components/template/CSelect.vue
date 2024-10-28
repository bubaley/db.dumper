<template>
    <div class="form-control">
        <label class="label" v-if="label">
            <span class="label-text">{{ label }}</span>
        </label>
        <select
            class="select select-bordered select-sm w-full max-w-xs"
            v-model="model"
        >
            <option
                v-for="option in items"
                :key="option[itemValue || 'id']"
                :value="option[itemValue || 'id']"
            >
                {{ option[itemLabel || 'name'] }}
            </option>
        </select>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    label?: string,
    items: Record<string, any>[],
    itemValue?: string
    itemLabel?: string
}>()

const model = defineModel()
</script>


<style scoped>

</style>
