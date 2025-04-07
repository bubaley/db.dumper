import { createApp } from "vue";
import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";
import "./style.css";
import App from "./App.vue";
import { router } from "./router.ts";
import ToastService from "primevue/toastservice";

const app = createApp(App);
app.use(router);
app.use(ToastService);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: true,
    },
  },
  pt: {
    inputtext: {
      root: {
        class: "w-full",
      },
    },
    inputnumber: {
      root: {
        class: "w-full",
      },
    },
    textarea: {
      root: {
        class: "w-full",
      },
    },
  },
});
app.mount("#app");
