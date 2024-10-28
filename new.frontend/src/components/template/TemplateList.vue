<template>
    <h2 class="text-2xl font-semibold mb-6">{{ title }}</h2>
    <div class="flex items-center mb-6" v-if="$slots.actions">
        <slot name="actions"></slot>
    </div>
    <div class="card bg-neutral shadow-xl rounded-xl">
        <div class="overflow-x-auto">
            <table class="table">
                <thead>
                <tr>
                    <th v-for="(el) in columns" :class="el.class" class="text-left p-3" :key="el.name">
                        {{ el.title }}
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr @click="$emit('click', item)" v-for="(item, index) in _items" :key="index">
                    <td v-for="(column, columnIndex) in columns" :key="columnIndex" class="p-3">
                        <slot v-bind="{item}" :name="`column-${column.name}`"></slot>
                        {{ column.format ? column.format(item[column.name]) : item[column.name] }}
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

</template>

<script setup lang="ts">
import {BaseModel} from "@/corexModels/apiModels/baseModel";
import {computed, onMounted} from "vue";
import {TableColumn} from "@/types/table";
import BaseRepo from "@/corexModels/apiModels/baseRepo";

const props = defineProps<{
    title?: string,
    repo: BaseRepo<BaseModel>
    loadDisabled?: boolean
    columns: TableColumn[],
    items?: Record<string, any>[]
}>()

const loadList = () => {
    void props.repo.list()
}

onMounted(() => {
    if (!props.items && !props.loadDisabled)
        loadList()
})

const _items = computed(() => {
    return props.items || props.repo.items
})
</script>


<style scoped>

</style>
