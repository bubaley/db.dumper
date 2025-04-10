<script setup lang="ts">
import { ref } from "vue";
import { authentication } from "../models/authentication/authentication.ts";
import {useRouter} from "vue-router";

const email = ref("");
const password = ref("");
const router = useRouter()

const auth = async () => {
  await authentication.login({ email: email.value, password: password.value });
  void router.replace({name: 'configList'})
};
</script>

<template>
  <div
    class="bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 lg:px-20 h-screen"
  >
    <div
      class="bg-surface-0 dark:bg-surface-900 p-6 shadow rounded-border w-full lg:w-6/12 mx-auto"
    >
      <div class="text-center mb-8">
        <svg
          class="mb-4 mx-auto fill-surface-600 dark:fill-surface-200 h-16"
          viewBox="0 0 30 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M20.7207 6.18211L14.9944 3.11148L3.46855 9.28678L0.579749 7.73444L14.9944 0L23.6242 4.62977L20.7207 6.18211ZM14.9996 12.3574L26.5182 6.1821L29.4216 7.73443L14.9996 15.4621L6.37724 10.8391L9.27337 9.28677L14.9996 12.3574ZM2.89613 16.572L0 15.0196V24.2656L14.4147 32V28.8953L2.89613 22.7132V16.572ZM11.5185 18.09L0 11.9147V8.81001L14.4147 16.5376V25.7904L11.5185 24.2312V18.09ZM24.2086 15.0194V11.9147L15.5788 16.5377V31.9998L18.475 30.4474V18.09L24.2086 15.0194ZM27.0969 22.7129V10.3623L30.0004 8.81V24.2653L21.3706 28.895V25.7904L27.0969 22.7129Z"
          />
        </svg>

        <div
          class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4"
        >
          dumper
        </div>
        <span
          class="text-surface-600 dark:text-surface-200 font-medium leading-normal"
          >Дампы в один клик</span
        >
        <span class="font-medium no-underline ml-2 text-primary cursor-pointer"
          >Создавай сейчас!</span
        >
      </div>

      <div>
        <label
          for="email1"
          class="text-surface-900 dark:text-surface-0 font-medium mb-2 block"
          >Email</label
        >
        <InputText v-model="email" id="email1" type="text" class="w-full mb-4" />

        <label
          for="password1"
          class="text-surface-900 dark:text-surface-0 font-medium mb-2 block"
          >Password</label
        >
        <InputText
          id="password1"
          v-model="password"
          type="password"
          placehoder="Password"
          class="w-full mb-4"
        />

        <Button
          @click="auth"
          label="Войти"
          icon="pi pi-user !text-xl !leading-none"
          class="w-full mt-3"
        />
      </div>
    </div>
  </div>
</template>
