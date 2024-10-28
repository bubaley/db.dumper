<!-- src/components/ElementTable.vue -->
<template>
    <template-list :items="sshConnectionRepo.items" :columns="columns" title="SSH Connections"
                   :repo="sshConnectionRepo"></template-list>
</template>

<script lang="ts" setup>

import {TableColumn} from "@/types/table.ts";
import {sshConnectionRepo} from "@/models/sshConnection/sshConnectionRepo.ts";
import TemplateList from "@/components/template/TemplateList.vue";

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
        name: 'host',
        title: 'Host'
    },
    {
        name: 'port',
        title: 'Port'
    },
    {
        name: 'username',
        title: 'Username'
    },
]
</script>

<style scoped>
</style>
