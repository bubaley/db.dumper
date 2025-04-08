<script setup lang="ts">
import ItemLayout from "../../layouts/ItemLayout.vue";
import { configRepo } from "../../models/config/configRepo.ts";
import { s3ConnectionRepo } from "../../models/s3Connection/s3ConnectionRepo.ts";
import { sshConnectionRepo } from "../../models/sshConnection/sshConnectionRepo.ts";
import { ref } from "vue";
import { workflowRepo } from "../../models/workflow/workflowRepo.ts";
import { useToast } from "primevue";
import type { Workflow } from "../../models/workflow/workflow.ts";
import { workflowEventRepo } from "../../models/workflowEvent/workflowEventRepo.ts";

const options = ref([
  { name: "Настройки", value: 1 },
  { name: "История", value: 2 },
]);

const databaseTypes = ref([
  { name: "Postgres", value: "postgres" },
  { name: "Docker Postgres", value: "docker_postgres" },
]);
const value = ref(1);
const dialog = ref(false);
const linkLoading = ref(false);
const toast = useToast();
const selectedWorkflow = ref<Workflow>();
const downloadLink = ref<string>();

const loadHistory = () => {
  if (!configRepo.item?.id) return;
  void workflowRepo.list({ config: configRepo.item.id }, { pageSize: 50 });
};

const loadWorkflowHistory = async (workflow: Workflow) => {
  linkLoading.value = true;
  workflowEventRepo.items = [];
  downloadLink.value = undefined;
  selectedWorkflow.value = workflow;
  void workflowEventRepo.list({ workflow: workflow.id }, { pageSize: "all" });
  dialog.value = true;
  if (selectedWorkflow.value.active) {
    const result = await workflowRepo.getDownloadUrl(selectedWorkflow.value);
    downloadLink.value = result.url;
  }
  linkLoading.value = false;
};

const build = async () => {
  if (!configRepo.item?.id) return;
  try {
    await configRepo.build(configRepo.item);
    toast.add({ severity: "success", summary: "Запущено" });
  } catch {
    toast.add({ severity: "error", summary: "Ошибка создания" });
  }
  loadHistory();
  value.value = options.value[1].value;
};
</script>

<template>
  <ItemLayout :repo="configRepo" @preload="loadHistory">
    <template v-slot:header-actions>
      <Button severity="warn" @click="build">Запустить</Button>
    </template>
    <SelectButton
      class="mb-6"
      v-model="value"
      optionLabel="name"
      optionValue="value"
      :options="options"
    />
    <div class="flex-col" v-if="configRepo.item">
      <div class="flex-col flex gap-3" v-if="value === 1">
        <FloatLabel variant="on">
          <InputText v-model="configRepo.item.name" />
          <label>Наименование</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <InputText id="on_label" v-model="configRepo.item.key" />
          <label for="on_label">Идентификатор</label>
        </FloatLabel>
        <FloatLabel class="w-full" variant="on">
          <Select
            v-model="configRepo.item.s3Connection"
            inputId="on_label"
            :options="s3ConnectionRepo.items"
            optionLabel="name"
            class="w-full"
          />
          <label for="on_label">S3 Подключение</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <Select
            v-model="configRepo.item.sshConnection"
            inputId="on_label"
            :options="sshConnectionRepo.items"
            optionLabel="name"
            class="w-full"
          />
          <label for="on_label">SSH Подключение</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <InputNumber :use-grouping="false" id="on_label" v-model="configRepo.item.maxVersions" />
          <label for="on_label">Количество версий</label>
        </FloatLabel>
        <div class="flex items-center gap-4">
          <ToggleSwitch
            v-model="configRepo.item.autoBuild"
            aria-label="asdsad"
          />
          Автоматический режим
        </div>
        <div class="my-4">Подключение к базе данных</div>
        <SelectButton
          v-model="configRepo.item.databaseConnection.type"
          optionLabel="name"
          optionValue="value"
          :options="databaseTypes"
        />
        <FloatLabel variant="on">
          <InputText
            id="on_label"
            v-model="configRepo.item.databaseConnection.host"
          />
          <label for="on_label">
            {{
              configRepo.item.databaseConnection.type === "postgres"
                ? "Адрес"
                : "Контейнер"
            }}
          </label>
        </FloatLabel>
        <FloatLabel
          variant="on"
          v-if="configRepo.item.databaseConnection.type === 'postgres'"
        >
          <InputNumber
            :use-grouping="false"
            id="on_label"
            v-model="configRepo.item.databaseConnection.port"
          />
          <label for="on_label">Порт</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <InputText
            id="on_label"
            v-model="configRepo.item.databaseConnection.db"
          />
          <label for="on_label">Наименование базы</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <InputText
            id="on_label"
            v-model="configRepo.item.databaseConnection.user"
          />
          <label for="on_label">Пользователь</label>
        </FloatLabel>
        <FloatLabel
          variant="on"
          v-if="configRepo.item.databaseConnection.type === 'postgres'"
        >
          <InputText
            id="on_label"
            v-model="configRepo.item.databaseConnection.password"
          />
          <label for="on_label">Пароль</label>
        </FloatLabel>
      </div>
      <div class="flex-col flex gap-3" v-else>
        <DataTable
          :value="workflowRepo.items"
          @row-click="loadWorkflowHistory($event.data)"
        >
          <Column field="filename" header="Ссылка"></Column>
          <Column field="status" header="Статус"></Column>
          <Column field="createdAt" header="Дата создания"></Column>
          <Column field="active" header="Активен"></Column>
        </DataTable>
      </div>

      <!--      <FloatLabel variant="on">-->
      <!--        <InputText id="on_label" v-model="configRepo.item.url" />-->
      <!--        <label for="on_label">Адрес</label>-->
      <!--      </FloatLabel>-->
      <!--      <FloatLabel variant="on">-->
      <!--        <InputText id="on_label" v-model="configRepo.item.region" />-->
      <!--        <label for="on_label">Регион</label>-->
      <!--      </FloatLabel>-->
      <!--      <FloatLabel variant="on">-->
      <!--        <InputText id="on_label" v-model="configRepo.item.bucket" />-->
      <!--        <label for="on_label">Бакет</label>-->
      <!--      </FloatLabel>-->
      <!--      <FloatLabel variant="on">-->
      <!--        <InputText id="on_label" v-model="configRepo.item.root" />-->
      <!--        <label for="on_label">Корневой каталог</label>-->
      <!--      </FloatLabel>-->
    </div>
    <Dialog v-model:visible="dialog" modal header="Информация" class="w-6/12">
      <Button
        v-if="downloadLink"
        as="a"
        class="mb-3"
        :href="downloadLink"
        target="_blank"
        >Скачать
      </Button>
      <Skeleton
        v-if="linkLoading"
        height="41px"
        class="mb-3"
        width="86px"
      ></Skeleton>
      <DataTable :value="workflowEventRepo.items">
        <Column field="name" header="Шаг"></Column>
        <Column field="isError" header="Ошибка"></Column>
        <Column
          class="text-nowrap"
          field="createdAt"
          header="Дата создания"
        ></Column>
        <Column field="text" header="Сообщение"></Column>
      </DataTable>
    </Dialog>
  </ItemLayout>
</template>

<style scoped></style>
