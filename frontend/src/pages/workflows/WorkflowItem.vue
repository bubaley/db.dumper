<template>
    <h2 class="text-2xl font-semibold mb-6">Workflow</h2>

    <div class="grid gap-y-2 bg-neutral shadow-xl rounded-xl card text-sm p-3 mb-6" v-if="item">
        <div>ID: {{ item.id }}</div>
        <div>Config: {{ item.config.name }}</div>
        <div>Status: {{ item.status }}</div>
        <div>Storage: {{ item.storage }}</div>
        <div>Filename: {{ item.filename }}</div>
        <div>Active: {{ item.active }}</div>
        <div>Created at: {{ formatDate(item.createdAt) || '-' }}</div>
        <a :href="downloadUrl || '#'">
            <button class="btn btn-md w-min flex-nowrap" v-if="item.active">
                <span v-if="urlLoading" class="loading loading-spinner loading-xs"></span>
                <span v-else>Download</span>
            </button>
        </a>

    </div>
    <TemplateList title="Events" :columns="columns" :repo="workflowEventRepo"
                  :items="workflowEventRepo.items"></TemplateList>
</template>

<script lang="ts" setup>


import {computed, onMounted, ref} from "vue";
import {workflowRepo} from "@/models/workflow/workflowRepo.ts";
import {useRoute} from "vue-router";
import {formatDate} from "@/utils/dateFunctions.ts";
import {workflowEventRepo} from "@/models/workflowEvent/workflowEventRepo.ts";
import TemplateList from "@/components/template/TemplateList.vue";
import {TableColumn} from "@/types/table.ts";
import {Workflow} from "@/models/workflow/workflow.ts";

const route = useRoute()
const urlLoading = ref(false)

const downloadUrl = ref()

const init = async () => {
    workflowRepo.item = null
    if (!route.params.workflowId) return
    void workflowEventRepo.list({workflow: route.params.workflowId})
    const workflow: Workflow = await workflowRepo.retrieve(route.params.workflowId)
    urlLoading.value = true
    if (!workflow.active) return
    try {
        const result = await workflowRepo.getDownloadUrl(workflow)
        downloadUrl.value = result.url
    } catch {
        workflow.active = false
    }
    urlLoading.value = false
}

onMounted(() => {
    void init()

})
const item = computed(() => {
    return workflowRepo.item
})


const columns: TableColumn[] = [
    {
        name: 'createdAt',
        title: 'Created at',
        format: (v?: string) => formatDate(v) || '-'
    },
    {
        name: 'name',
        title: 'Name'
    },
    {
        name: 'text',
        title: 'Text'
    },

]
</script>

<style scoped>
</style>
