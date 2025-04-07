<script setup lang="ts">
import ListLayout from "../../layouts/ListLayout.vue";
import { s3ConnectionRepo } from "../../models/s3Connection/s3ConnectionRepo.ts";
</script>

<template>
  <ListLayout title="S3 Подключения" :repo="s3ConnectionRepo"></ListLayout>
</template>

<style scoped></style>
