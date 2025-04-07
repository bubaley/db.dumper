<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import type BaseRepo from "../corexModels/apiModels/baseRepo.ts";
import ItemHeader from "./ItemHeader.vue";
import type { BaseModel } from "../corexModels/apiModels/baseModel.ts";
import { router } from "../router.ts";

const emit = defineEmits(["preload"]);
const route = useRoute();

const props = defineProps<{
  repo: BaseRepo<any>;
}>();

onMounted(() => {
  void loadItem();
});

const routeValue = computed(() => {
  if (!props.repo.routeKey) return;
  return route.params[`${props.repo.routeKey}Id`];
});

const loadItem = async () => {
  if (!routeValue.value) return;
  if (routeValue.value === "new") props.repo.item = props.repo.defaultItem();
  else await props.repo.retrieve(routeValue.value as string);
  emit("preload", props.repo.item);
};

const handleSave = (item: BaseModel) => {
  if (routeValue.value === "new") {
    void router.replace({
      name: route.name,
      params: { [`${props.repo.routeKey}Id`]: item.id },
    });
  }
};
</script>

<template>
  <div class="flex-col p-6">
    <ItemHeader class="mb-6" :repo="props.repo" @save="handleSave($event)">
      <template v-slot:header-actions>
        <slot name="header-actions"></slot>
      </template>
    </ItemHeader>
    <slot></slot>
  </div>
</template>

<style scoped></style>
