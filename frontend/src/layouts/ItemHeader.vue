<script setup lang="ts">
import type BaseRepo from "../corexModels/apiModels/baseRepo.ts";
import { useToast } from "primevue";

const emit = defineEmits(["save"]);
const toast = useToast();

const props = defineProps<{
  repo: BaseRepo<any>;
}>();

const saveItem = async () => {
  try {
    const result = await props.repo.updateOrCreate(props.repo.item);
    emit("save", result.item);
    toast.add({ severity: "success", summary: "Сохранено" });
  } catch {
    toast.add({ severity: "error", summary: "Ошибка сохранения" });
  }
  props.repo.loadings.save = false;
};
</script>

<template>
  <div class="flex gap-4 items-center">
    <Button :loading="repo.loadings.save" @click="saveItem">Сохранить</Button>
    <slot name="header-actions"></slot>
  </div>
</template>

<style scoped></style>
