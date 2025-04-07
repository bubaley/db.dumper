<template>
  <div class="min-h-screen flex">
    <Drawer></Drawer>
    <div class="flex-1 flex flex-col h-screen overflow-y-auto">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { s3ConnectionRepo } from "../models/s3Connection/s3ConnectionRepo.js";
import { sshConnectionRepo } from "../models/sshConnection/sshConnectionRepo.js";

onMounted(() => {
  void s3ConnectionRepo.list(undefined, { pageSize: "all" });
  void sshConnectionRepo.list(undefined, { pageSize: "all" });
});
</script>

<style lang="scss"></style>
