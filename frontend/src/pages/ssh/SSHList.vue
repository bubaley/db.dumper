<script setup lang="ts">
import ListLayout from "../../layouts/ListLayout.vue";
import { sshConnectionRepo } from "../../models/sshConnection/sshConnectionRepo.ts";
</script>

<template>
  <ListLayout
    title="SSH Подключения"
    :repo="sshConnectionRepo"
  ></ListLayout>
</template>

<style scoped></style>
