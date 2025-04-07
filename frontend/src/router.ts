import { createRouter, createWebHistory } from "vue-router";
import SSHList from "./pages/ssh/SSHList.vue";
import SSHItem from "./pages/ssh/SSHItem.vue";
import S3List from "./pages/s3/S3List.vue";
import S3Item from "./pages/s3/S3Item.vue";
import ConfigList from "./pages/config/ConfigList.vue";
import ConfigItem from "./pages/config/ConfigItem.vue";
import Auth from "./pages/Auth.vue";
import MainPage from "./pages/MainPage.vue";

const routes = [
  {
    path: "/",
    component: MainPage,
    children: [
      {
        name: "sshList",
        path: "ssh",
        component: SSHList,
      },
      {
        name: "sshItem",
        path: "ssh/:sshId",
        component: SSHItem,
      },
      {
        name: "s3List",
        path: "s3",
        component: S3List,
      },
      {
        name: "s3Item",
        path: "s3/:s3Id",
        component: S3Item,
      },
      {
        name: "configList",
        path: "config",
        component: ConfigList,
      },
      {
        name: "configItem",
        path: "config/:configId",
        component: ConfigItem,
      },
    ],
  },
  {
    name: "auth",
    path: "/auth",
    component: Auth,
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
