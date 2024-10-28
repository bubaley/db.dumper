<!-- src/components/ElementTable.vue -->
<template>
    <template-list @click="dialog = true" :columns="columns" title="S3 Connections"
                   :repo="s3ConnectionRepo"></template-list>
    <!--    <CDialog v-model="dialog">-->
    <!--        asdaskljdsalk-->
    <!--    </CDialog>-->
</template>

<script lang="ts" setup>

import {TableColumn} from "@/types/table.ts";
import TemplateList from "@/components/template/TemplateList.vue";
import {s3ConnectionRepo} from "@/models/s3Connection/s3ConnectionRepo.ts";
// import CDialog from "@/components/template/CDialog.vue";

// const dialog = ref(false)

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
        name: 'bucket',
        title: 'Bucket'
    },

    {
        name: 'url',
        title: 'Url'
    },
    {
        name: 'region',
        title: 'Region'
    },
    {
        name: 'root',
        title: 'Root'
    },
]
</script>

<style scoped>
</style>
