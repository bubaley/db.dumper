// src/router/index.js
import {createRouter, createWebHistory} from 'vue-router';
import LoginPage from '@/pages/LoginPage.vue'
import HomePage from '@/pages/HomePage.vue'
import ConfigList from '@/pages/configs/ConfigList.vue'
import SSHConnectionList from '@/pages/sshConnections/SSHConnectionList.vue'
import S3ConnectionList from '@/pages/s3Connections/S3ConnectionList.vue'
import WorkflowList from '@/pages/workflows/WorkflowList.vue'
import WorkflowItem from '@/pages/workflows/WorkflowItem.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/',
    name: 'home',
    component: HomePage,
    children: [
      {
        name: 'configList',
        path: 'configs',
        component: ConfigList
      },
      {
        name: 'sshConnectionList',
        path: 'ssh_connections',
        component: SSHConnectionList
      },
      {
        name: 's3ConnectionList',
        path: 's3_connections',
        component: S3ConnectionList
      },
      {
        name: 'workflowList',
        path: 'workflows',
        component: WorkflowList
      },
      {
        name: 'workflowItem',
        path: 'workflows/:workflowId',
        component: WorkflowItem
      }
    ]
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
