<template>
	<div
		class="relative overflow-y-auto w-full h-full flex flex-col items-center"
	>
		<BgTopBar class="pt-2 px-3">
			<div class="absolute top-[.7rem] w-[60%] max-w-[25rem] z-20 select-none">
				<n-tabs v-model:value="data.curPage" type="segment" animated>
					<n-tab-pane name="role" tab="角色"> </n-tab-pane>
					<n-tab-pane name="plugin" tab="插件"> </n-tab-pane>
				</n-tabs>
			</div>

			<template v-if="data.curPage == 'role'">
				<RoleView />
			</template>

			<template v-else-if="data.curPage == 'plugin'">
				<PluginView />
			</template>
		</BgTopBar>
	</div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import { useRouter } from "vue-router";
import BgTopBar from "@/views/layout/BgTopBar.vue";
import { useAgentStore, useUserStore } from "@/store";
import RoleView from "./RoleView.vue";
import PluginView from "./PluginView.vue";

const agentsStore = useAgentStore();
const userStore = useUserStore();

onMounted(async () => {
	await agentsStore.updateAgents();
	data.dataList = data.dataListBackup;
	updateInviteCode();
});

const router = useRouter();

const updateInviteCode = () => {
	const url = new URL(window.location.href);
	const params = new URLSearchParams(url.search);
	const invitecode = params.get("invitecode");

	if (invitecode) {
		userStore.$state.invitecode = invitecode;
		console.log("invitecode", invitecode);
	}
};

const data = reactive({
	curPage: "role"
});
</script>
