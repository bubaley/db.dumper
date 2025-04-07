<script setup lang="ts">
import ItemLayout from "../../layouts/ItemLayout.vue";
import { sshConnectionRepo } from "../../models/sshConnection/sshConnectionRepo.ts";
import { ref } from "vue";

const types = ref([
  { name: "Пароль", value: "password" },
  { name: "Приватный ключ", value: "private_key" },
  { name: "Приватный ключ c фразой", value: "private_key_with_passphrase" },
]);
</script>

<template>
  <ItemLayout :repo="sshConnectionRepo">
    <div class="flex flex-col gap-3" v-if="sshConnectionRepo.item">
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="sshConnectionRepo.item.name" />
        <label for="on_label">Наименование</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="sshConnectionRepo.item.host" />
        <label for="on_label">Сервер</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputNumber
          :use-grouping="false"
          id="on_label"
          v-model="sshConnectionRepo.item.port"
        />
        <label for="on_label">Порт</label>
      </FloatLabel>
      <FloatLabel variant="on">
        <InputText id="on_label" v-model="sshConnectionRepo.item.username" />
        <label for="on_label">Пользователь</label>
      </FloatLabel>
      <SelectButton
        v-model="sshConnectionRepo.item.type"
        optionLabel="name"
        optionValue="value"
        :options="types"
      />

      <FloatLabel
        variant="on"
        v-if="sshConnectionRepo.item.type === 'password'"
      >
        <InputText id="on_label" v-model="sshConnectionRepo.item.password" />
        <label for="on_label">Пароль</label>
      </FloatLabel>

      <div v-else class="flex flex-col gap-4">
        <FloatLabel variant="on" v-if="sshConnectionRepo.item.type === 'private_key_with_passphrase'">
          <InputText
            id="on_label"
            v-model="sshConnectionRepo.item.passphrase"
          />
          <label for="on_label">Секретная фраза</label>
        </FloatLabel>

        <FloatLabel variant="on">
          <Textarea v-model="sshConnectionRepo.item.privateKey" rows="5" />
          <label for="on_label">Секретный ключ</label>
        </FloatLabel>
      </div>
    </div>
  </ItemLayout>
</template>

<style scoped></style>
