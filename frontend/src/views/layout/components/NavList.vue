<template>
	<div class="flex-1 flex flex-col select-none">
		<template v-for="(item, i) in data.navList" :key="item.label">
			<div
				@click.stop="setNavActive(item, i)"
				class="relative layout-menu hover:bg-white hover:cursor-pointer flex flex-col items-center justify-center w-[50px] h-[50px] mb-4 group rounded-lg"
				:class="[isActive(item.path) ? 'bg-white':'']"
			>
				<!-- 左侧导航栏按钮 -->
				<div class="flex justify-center items-center">
					<!-- 图标 -->
					<Icon
						:icon="item.icon"
						:width="25"
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

const data = reactive({
  curActive: computed(() => navStore.curActive),
  navList: computed(() => navStore.navList),
});

const setNavActive = (item: any, i: number): void => {
  navStore.setNavActive(i);
  const targetPath = data.navList[i].path; // 使用点击项的路径
  if (targetPath !== route.path) { // 避免重复导航
    router.push(targetPath);
  }
};

// 判断当前路由是否为激活状态
const isActive = (path: string): boolean => {
  return data.navList[data.curActive].path === path;
};

// 实时更新导航栏激活状态，刷新页面时
watch(
  () => route.fullPath,
  (val) => {
    const basePath = val.split("/")[1];
    const curNavIndex = data.navList.findIndex((item) => {
      return `/${basePath}` === item.path;
    });
    if (curNavIndex >= 0) {
      navStore.setNavActive(curNavIndex);
    }
  },
  { immediate: true }
);
</script>

