<!-- src/components/ElementTable.vue -->
<template>
    <TemplateList :load-disabled="true"
                  @click="$router.push({name: 'workflowItem', params: {workflowId: $event.id}})"
                  :columns="columns" title="Workflows"
                  :repo="workflowRepo">
        <template v-slot:actions>
            <CSelect @update:model-value="loadList" v-model="workflowRepo.selectedConfig"
                     :items="configRepo.items"></CSelect>
        </template>
    </TemplateList>
</template>

<script lang="ts" setup>

import {TableColumn} from "@/types/table.ts";
import TemplateList from "@/components/template/TemplateList.vue";
import {workflowRepo} from "@/models/workflow/workflowRepo.ts";
import {Config} from "@/models/config/config.ts";
import {formatDate} from "@/utils/dateFunctions.ts";
import CSelect from "@/components/template/CSelect.vue";
import {configRepo} from "@/models/config/configRepo.ts";
import {nextTick, onMounted} from "vue";

const columns: TableColumn[] = [
    {
        name: 'id',
        title: 'ID',
    },
    {
        name: 'status',
        title: 'Status'
    },
    {
        name: 'config',
        title: 'Config',
        format: (v?: Config) => v?.name
    },
    {
        name: 'active',
        title: 'Active'
    },
    {
        name: 'createdAt',
        title: 'Created at',
        format: (v?: string) => formatDate(v) || '-'
    },

]

const loadList = () => {
    void nextTick(() => {
        void workflowRepo.list({config: workflowRepo.selectedConfig})
    })
}

onMounted(() => {
    loadList()
})
</script>

<style scoped>
</style>
