<script setup lang="ts">
import ListLayout from "../../layouts/ListLayout.vue";
import { configRepo } from "../../models/config/configRepo.ts";
</script>

<template>
  <ListLayout title="Конфигурации" :repo="configRepo"></ListLayout>
</template>

<style scoped></style>
