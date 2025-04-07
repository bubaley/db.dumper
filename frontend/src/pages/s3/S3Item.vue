<script setup lang="ts">
import ItemLayout from "../../layouts/ItemLayout.vue";
import { s3ConnectionRepo } from "../../models/s3Connection/s3ConnectionRepo.ts";
</script>

<template>
  <ItemLayout :repo="s3ConnectionRepo">
    <div class="flex flex-col gap-3" v-if="s3ConnectionRepo.item">
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.name" />
        <label for="on_label">Наименование</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.url" />
        <label for="on_label">Адрес</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.region" />
        <label for="on_label">Регион</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.bucket" />
        <label for="on_label">Бакет</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.root" />
        <label for="on_label">Корневой каталог</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.accessKey" />
        <label for="on_label">Публичный ключ</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="s3ConnectionRepo.item.secretKey" />
        <label for="on_label">Приватный ключ</label>
      </FloatLabel>
    </div>
  </ItemLayout>
</template>

<style scoped></style>
