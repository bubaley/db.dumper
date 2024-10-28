<template>
    <!--    <div>-->
    <!--&lt;!&ndash;        <AppDrawer/>&ndash;&gt;-->
    <!--        &lt;!&ndash;        <AppHeader/>&ndash;&gt;-->
    <!--        <main class="p-4">-->
    <!--            asdjkas-->
    <!--            &lt;!&ndash;            <router-view/>&ndash;&gt;-->
    <!--        </main>-->
    <!--    </div>-->
    <div class="drawer drawer-open">
        <input id="my-drawer" type="checkbox" class="drawer-toggle"/>
        <div class="drawer-side">
            <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
            <ul class="menu bg-base-200 text-base-content min-h-full w-80 p-4">
                <!-- Sidebar content here -->
                <li v-for="(el) in tabs" :key="el.name">
                    <router-link :to="{name:el.to}">{{ el.name }}</router-link>
                </li>
            </ul>
        </div>
        <div class="drawer-content p-5">

            <!-- Page content here -->
            <router-view></router-view>
        </div>

    </div>

    <!--    <aside class="w-64 border-r shadow-lg">-->
    <!--        <div class="p-4 text-lg font-semibold text-center border-b">DB.DUMPER</div>-->
    <!--        <ul class="mt-4">-->
    <!--            <li v-for="(item, index) in tabs" :key="index">-->
    <!--                <button-->
    <!--                    @click="$router.push({name: item.to})"-->
    <!--                    :class="{'bg-blue-100 text-blue-600': $route.name === item.to}"-->
    <!--                    class="w-full p-4 text-left transition-colors duration-200 hover:bg-blue-50 focus:outline-none"-->
    <!--                >-->
    <!--                    {{ item.name }}-->
    <!--                </button>-->
    <!--            </li>-->
    <!--        </ul>-->
    <!--    </aside>-->
    <!--    <main class="flex-1 p-6">-->

    <!--        <router-view></router-view>-->
    <!--    </main>-->

</template>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import {configRepo} from "@/models/config/configRepo";
import {authRepo} from "@/models/authentication/authRepo";
import {authentication} from "@/models/authentication/authentication";

const ready = ref(false)
const tabs = ref([
    {name: 'Configs', to: 'configList'},
    {name: 'SSH Connections', to: 'sshConnectionList'},
    {name: 'S3 Connections', to: 's3ConnectionList'},
    {name: 'Workflows', to: 'workflowList'},
])

onMounted(async () => {
    try {
        await authRepo.initialise();

    } catch {
    }
    if (!authentication.user) {
        window.location.href =
            'login?path=' + window.location.href.replace(origin + '/', '');
    } else {
        ready.value = true;
        void configRepo.list()
    }

})
</script>

<style scoped>

</style>
