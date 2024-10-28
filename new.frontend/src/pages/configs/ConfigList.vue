<!-- src/components/ElementTable.vue -->
<template>
    <TemplateList :columns="columns" title="Configs"
                  :repo="configRepo">
        <template v-slot:column-actions="{item}">
            <button class="btn btn-sm" @click="build(item)">
                Build
            </button>
        </template>
    </TemplateList>

</template>

<script lang="ts" setup>

import {TableColumn} from "@/types/table";
import TemplateList from "@/components/template/TemplateList.vue";
import {configRepo} from "@/models/config/configRepo";
import {Config} from "@/models/config/config";
import {useRouter} from "vue-router";
import {S3Connection} from "@/models/s3Connection/s3Connection";
import {SSHConnection} from "@/models/sshConnection/sshConnection";

const router = useRouter()

const build = async (config: Config) => {
    const result = await configRepo.build(config)
    void router.push({
        name: 'workflowItem',
        params: {workflowId: result.id}
    })
}


const columns: TableColumn[] = [
    {
        name: 'id',
        title: 'ID',
    },
    {
        name: 'name',
        title: 'Name'
    },
    {
        name: 'key',
        title: 'Key'
    },
    {
        name: 's3Connection',
        title: 'S3',
        format: (v: S3Connection | null) => v?.name || '-'
    },
    {
        name: 'sshConnection',
        title: 'SSH',
        format: (v: SSHConnection | null) => v?.name || '-'
    },
    {
        name: 'actions',
        title: 'Actions'
    }
]
</script>

<style scoped>
</style>
