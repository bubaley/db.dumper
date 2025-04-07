<script setup lang="ts">
import type BaseRepo from "../corexModels/apiModels/baseRepo.ts";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import type { BaseModel } from "../corexModels/apiModels/baseModel.ts";

const props = defineProps<{
  repo: BaseRepo<any>;
  title?: string;
}>();

const router = useRouter();

const clickRow = (item: BaseModel | null) => {
  if (!props.repo.routeKey) return;
  const idKey = `${props.repo.routeKey}Id`;
  router.push({
    name: `${props.repo.routeKey}Item`,
    params: { [idKey]: item?.id || "new" },
  });
};

defineEmits(["rowClick"]);

onMounted(() => {
  void props.repo.list(undefined, { pageSize: "all" });
});
</script>

<template>
  <div class="flex-col p-6">
    <div class="flex items-center mb-6 gap-4">
      <div v-if="title">{{ title }}</div>
      <Button @click="clickRow(null)">Создать</Button>
    </div>
    <DataTable :value="props.repo.items" @row-click="clickRow($event.data)">
<!--      <Column field="code" header="Code"></Column>-->
      <Column field="name" header="Наименование"></Column>
<!--      <Column field="category" header="Category"></Column>-->
<!--      <Column field="quantity" header="Quantity"></Column>-->
    </DataTable>
  </div>
</template>

<style scoped></style>
