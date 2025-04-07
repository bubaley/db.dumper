<template>
  <div class="min-h-screen flex">
    <!-- Sidebar (Drawer) -->

    <Drawer></Drawer>
    <div class="flex-1 flex flex-col h-screen overflow-y-auto">
      <router-view></router-view>
    </div>
    <!-- Main Content -->
    <!--    <div class="flex-1 flex flex-col overflow-hidden">-->
    <!--      &lt;!&ndash; Topbar &ndash;&gt;-->
    <!--      <div class="bg-white shadow-sm p-4 flex items-center justify-between">-->
    <!--        <Button-->
    <!--          icon="pi pi-bars"-->
    <!--          @click="toggleSidebar"-->
    <!--          class="p-button-text p-button-rounded"-->
    <!--        />-->
    <!--        <div class="flex items-center space-x-4">-->
    <!--          <span class="font-medium">Welcome, User</span>-->
    <!--          <Avatar icon="pi pi-user" class="bg-blue-500 text-white" />-->
    <!--        </div>-->
    <!--      </div>-->

    <!--      &lt;!&ndash; Page Content &ndash;&gt;-->
    <!--      <div class="flex-1 overflow-y-auto p-6 bg-white m-4 rounded-lg shadow-sm">-->
    <!--        <h1 class="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>-->

    <!--        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">-->
    <!--          <Card v-for="stat in stats" :key="stat.title" class="shadow-sm">-->
    <!--            <template #content>-->
    <!--              <div class="flex items-center justify-between">-->
    <!--                <div>-->
    <!--                  <span class="block text-gray-500 font-medium mb-1">{{-->
    <!--                    stat.title-->
    <!--                  }}</span>-->
    <!--                  <span class="block text-2xl font-bold">{{ stat.value }}</span>-->
    <!--                </div>-->
    <!--                <div :class="`p-3 rounded-full ${stat.bgColor}`">-->
    <!--                  <i :class="`pi ${stat.icon} text-lg text-white`"></i>-->
    <!--                </div>-->
    <!--              </div>-->
    <!--            </template>-->
    <!--          </Card>-->
    <!--        </div>-->

    <!--        <Card class="shadow-sm">-->
    <!--          <template #title>Recent Activity</template>-->
    <!--          <template #content>-->
    <!--            <DataTable :value="activities" class="p-datatable-sm" :rows="5">-->
    <!--              <Column field="date" header="Date"></Column>-->
    <!--              <Column field="activity" header="Activity"></Column>-->
    <!--              <Column field="status" header="Status">-->
    <!--                <template #body="{ data }">-->
    <!--                  <Tag-->
    <!--                    :value="data.status"-->
    <!--                    :severity="getSeverity(data.status)"-->
    <!--                  />-->
    <!--                </template>-->
    <!--              </Column>-->
    <!--            </DataTable>-->
    <!--          </template>-->
    <!--        </Card>-->
    <!--      </div>-->
    <!--    </div>-->
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { s3ConnectionRepo } from "../models/s3Connection/s3ConnectionRepo.js";
import { sshConnectionRepo } from "../models/sshConnection/sshConnectionRepo.js";

const visible = ref(true);

onMounted(() => {
  void s3ConnectionRepo.list(undefined, { pageSize: "all" });
  void sshConnectionRepo.list(undefined, { pageSize: "all" });
});
</script>

<style>
/* Убираем overlay для Sidebar */
.p-sidebar {
  position: relative;
  transform: none;
  box-shadow: none;
}

.p-sidebar-left {
  left: 0;
}

.p-sidebar-mask {
  display: none !important;
}
</style>
