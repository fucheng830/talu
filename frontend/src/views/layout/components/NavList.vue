<template>
	<div class="flex-1 flex flex-col select-none">
		<template v-for="(item, i) in data.navList" :key="item.label">
			<div
				@click.stop="setNavActive(item, i)"
				class="relative layout-menu mb-4 hover:bg-white hover:cursor-pointer flex flex-col items-center justify-center w-[68px] h-[68px]"
			>
				<!-- 左侧导航栏按钮 -->
				<div
					class="flex justify-center items-center w-[40px] h-[40px] rounded-full"
					:style="{
						'background-color':
							data.curActive == i ? globalColors.btnActive : '',
					}"
				>
					<!-- 图标 -->
					<Icon
						:icon="data.curActive == i ? item.iconActive : item.icon"
						:width="28"
						:color="data.curActive == i ? 'white' : globalColors.btnDeactive"
					/>
				</div>
				<span
					class="font-bold"
					:style="{
						color:
							data.curActive == i
								? globalColors.btnActive
								: globalColors.btnDeactive,
					}"
					>{{ $t(`navigator.${item.label}`) }}</span
				>
			</div>
		</template>
	</div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from "vue";
import { useChatStore, useNavStore } from "@/store";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import { useRoute, useRouter } from "vue-router";
import { useBasicLayout } from "@/hooks/useBasicLayout";

const route = useRoute();
const router = useRouter();
const navStore = useNavStore();
const chatStore = useChatStore();

const data = reactive({
	curActive: computed(() => navStore.curActive),
	navList: computed(() => navStore.navList),
});

const setNavActive = (item, i: number): void => {
	navStore.setNavActive(i);
	if (item.path == "/chat") return chatStore.gotoChat(router);
	router.push(data.navList[data.curActive].path);
};

// 实时更新导航栏 激活状态，刷新页面时
watch(
	() => route.fullPath,
	(val) => {
		// 根据路由路径，找到当前的下标
		const curNavIndex = data.navList.findIndex((item) => {
			// 不止一层路由时只取第一层，chat路由带id
			const basePath = val.split("/")[1];
			return `/${basePath}` == item.path;
		});
		curNavIndex >= 0 && navStore.setNavActive(curNavIndex);
	},
	{ immediate: true, deep: true }
);
</script>

<style></style>
