<template>
	<div class="flex-1 flex flex-col select-none">
		<template v-for="(item, i) in data.navList" :key="item.label">
			<div
				@click.stop="setNavActive(item, i)"
				class="relative layout-menu hover:bg-white hover:cursor-pointer flex flex-col items-center justify-center w-[50px] h-[50px] bg-white mb-4 group rounded-lg"
			>
				<!-- 左侧导航栏按钮 -->
				<div
					class="flex justify-center items-center"
				>
					<!-- 图标 -->
					<Icon
						:icon="item.icon"
						:width="25"
						:class="[isActive(item.path) ? active_color : '', 'group-hover:' + active_color]"
					/>
				</div>
				
			</div>
		</template>
	</div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from "vue";
import { useNavStore } from "@/store";
import { Icon } from "@iconify/vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const navStore = useNavStore();

const active_color = "text-blue-500";

const data = reactive({
  curActive: computed(() => navStore.curActive),
  navList: computed(() => navStore.navList),
});

const setNavActive = (item: any, i: number): void => {
  navStore.setNavActive(i);
  router.push(data.navList[data.curActive].path);
};

// 判断当前路由是否为激活状态
const isActive = (path: string): boolean => {
  return route.path === path;
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