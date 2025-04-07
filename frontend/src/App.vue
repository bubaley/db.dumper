<script setup lang="ts">
import { onMounted, ref } from "vue";
import { authentication } from "./models/authentication/authentication.ts";
import { useRouter } from "vue-router";

const ready = ref(false);
const router = useRouter();
onMounted(async () => {
  try {
    await authentication.me();
  } catch {
    void router.replace({ name: "auth" });
  }
  ready.value = true;
});
</script>

<template>
  <Toast />
  <router-view v-if="ready"></router-view>
</template>

<style scoped></style>
