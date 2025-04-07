<script setup lang="ts">
import { ref } from "vue";

const items = ref([
  {
    icon: "pi pi-server",
    title: "ssh",
    routeName: "sshList",
  },
  {
    icon: "pi pi-cloud",
    title: "s3",
    routeName: "s3List",
  },
  {
    icon: "pi pi-sitemap",
    title: "config",
    routeName: "configList",
  },
  // {
  //   icon: "pi pi-check",
  //   title: "test",
  // },
]);
</script>

<template>
  <div
    class="w-auto h-screen p-5 bg-surface-50 dark:bg-surface-900 h-full flex flex-col justify-between"
  >
    <div class="w-12 flex flex-col items-center">
      <div class="font-medium">dump</div>
      <div class="mt-10 flex flex-col gap-2">
        <div
          v-for="(el, index) in items"
          :key="index"
          @click="$router.push({ name: el.routeName })"
          class="px-4 py-1 flex items-center gap-1 cursor-pointer text-base rounded-lg transition-all select-none w-12 justify-center py-4 text-muted-color hover:bg-emphasis bg-transparent"
          data-pd-tooltip="true"
        >
          <i :class="el.icon"></i><span class="hidden">・</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
