<template>
	<!-- 知识库详情 包围 -->
	<div class="relative w-full h-full">
		<div
			class="w-full h-full flex"
			:class="[isMobile ? 'flex-col' : '']"
			:style="{ 'background-color': 'white' }"
		>
			<!-- 左侧栏 pc端 -->
			<div v-if="!isMobile" class="flex flex-col py-4 w-[210px] border-r">
				<!-- 知识库信息 -->
				<div class="flex flex-col gap-[14px] p-[14px] pt-0 border-b mb-[14px]">
					<div class="flex items-center gap-2">
						<!-- 标题 -->
						<span
							class="w-full font-bold overflow-hidden text-ellipsis whitespace-nowrap text-xl"
						>
							{{ data.curKnowledge?.name }}
						</span>
					</div>

					<!-- 知识库类型 -->
					<div class="flex">
						<div
							class="flex items-center gap-1 border bg-[#F4F4F7] border-[#E8EBF0] rounded-lg py-[6px] px-[14px] text-[12px]"
						>
							<Icon
								icon="mingcute:storage-fill"
								color="#8A95A7"
								width="19"
								class="pb-[2px]"
							/>
							<span>{{ $t("knowledge.commonKnowledge") }}</span>
						</div>
					</div>
				</div>

				<!-- 左侧菜单栏 -->
				<div class="w-full flex-1 flex flex-col gap-2 px-4">
					<!-- 单个菜单按钮 -->
					<template v-for="item in data.opt.menuList" :key="item.key">
						<div
							@click="changeCurMenu(item)"
							class="flex items-center gap-2 py-2 px-4 rounded-lg cursor-pointer"
							:class="[data.curMenu != item.key && `hover:bg-[#EFEFF1]`]"
							:style="{
								'background-color': data.curMenu == item.key ? `#E1EAFF` : '',
							}"
						>
							<!-- 菜单图标 -->
							<Icon
								:icon="item.icon"
								:color="item.key == data.curMenu ? theme.primaryColor : ``"
								width="18"
							/>
							<!-- 菜单文本 -->
							<span
								:class="[item.key == data.curMenu && 'font-bold']"
								:style="{
									color: item.key == data.curMenu ? theme.primaryColor : '',
								}"
							>
								{{ item.label }}
							</span>
						</div>
					</template>
				</div>

				<!-- 返回 知识库首页 -->
				<div
					class="flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-[#F4F4F7] rounded-lg"
					@click="router.push('/knowledge')"
					:style="{ 'background-color': 'white' }"
				>
					<!-- 返回图标 箭头 左 -->
					<div
						class="p-1 rounded-full"
						:style="{ 'box-shadow': '1px 1px 9px rgba(0,0,0,.15)' }"
					>
						<Icon
							icon="gravity-ui:arrow-left"
							:color="theme.primaryColor"
							width="22"
						/>
					</div>
					<span>{{ $t("knowledge.knowledgeList") }}</span>
				</div>
			</div>

			<!-- 顶部栏 移动端 -->
			<div v-else class="w-full flex flex-col pt-4 px-4">
				<div class="grid grid-cols-[1fr_auto] gap-4">
					<!-- 左侧 -->
					<div class="grid grid-cols-[auto_1fr] gap-4">
						<!-- 返回图标 箭头 左 -->
						<div
							class="p-1 rounded-full"
							:style="{ 'box-shadow': '1px 1px 9px rgba(0,0,0,.15)' }"
							@click="handleClickBack"
						>
							<Icon
								icon="gravity-ui:arrow-left"
								:color="theme.primaryColor"
								width="22"
							/>
						</div>

						<!-- <div class=""> -->
						<!-- 标题 -->
						<span
							class="font-bold overflow-hidden text-ellipsis whitespace-nowrap text-xl"
						>
							{{ data.curKnowledge?.name }}
						</span>

						<!-- </div> -->
					</div>

					<!-- 右侧 知识库类型 -->
					<div
						class="flex items-center gap-1 border bg-[#F4F4F7] border-[#E8EBF0] rounded-lg py-[6px] px-[14px] text-[12px]"
					>
						<Icon
							icon="mingcute:storage-fill"
							color="#8A95A7"
							width="19"
							class="pb-[2px]"
						/>
						<span>{{ $t("knowledge.commonKnowledge") }}</span>
					</div>
				</div>
			</div>

			<!-- 右侧 内容区 -->
			<div
				class="flex-1 h-full"
				:class="[isMobile ? 'grid grid-rows-[auto_1fr]' : '']"
			>
				<!-- 顶部tab栏 -->
				<div v-if="isMobile" class="mt-2 px-4">
					<n-tabs
						v-model:value="data.curMenu"
						type="segment"
						animated
						:onUpdate:value="changeCurMenu"
					>
						<template v-for="item in data.opt.menuList" :key="item.key">
							<n-tab-pane :name="item.key" :tab="item.label"> </n-tab-pane>
						</template>
					</n-tabs>
				</div>

				<div class="w-full h-full">
					<router-view v-slot="{ Component }">
						<component ref="refRouterView" :is="Component" />
					</router-view>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useKnowledgeStore } from "@/store";
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();

const { isMobile } = useBasicLayout();
const route = useRoute();
const router = useRouter();
const knowledgeStore = useKnowledgeStore();

const refRouterView = ref();
const data = reactive({
	curKnowledge: computed(() =>
		knowledgeStore.listKnowledge.find((item) => item.uuid == route.params.id)
	),
	curMenu: "dataset", // 当前tab激活状态
	progress: {
		qa: 100,
		index: 100,
	},
	opt: {
		menuList: [
			{
				label: t("knowledge.dataset"),
				key: "dataset",
				pathName: "KnowledgeDetails_dataset",
				icon: "uil:chart",
			},
			{
				label: t("knowledge.searchTest"),
				key: "searchTest",
				pathName: "KnowledgeDetails_searchTest",
				icon: "tabler:target-arrow",
			},
			// {
			// 	label: "配置",
			// 	key: "setting",
			// 	pathName: "KnowledgeDetails_setting",
			// 	icon: "uil:setting",
			// },
		],
	},
});

// 切换左侧菜单
const changeCurMenu = (item: any) => {
	data.curMenu = item.key;

	// 获取当前tab的pathName
	const curPathName = !!isMobile.value
		? data.opt.menuList.find((cur) => cur.key == item)?.pathName
		: item.pathName;

	routerGo(curPathName);
};

// 路由跳转
const routerGo = (pathName: string) => {
	router.push({
		name: pathName,
		params: {
			id: route.params?.id,
		},
	});
};

// 点击左上角返回按钮时
const handleClickBack = () => {
	if (refRouterView?.value?.onClickBack) {
		// 路由子组件 有onClickBack处理返回方法时执行，返回true则中断返回知识库页
		const res = refRouterView?.value?.onClickBack();

		if (res) return;
	}

	router.replace("/knowledge");
};

onMounted(() => {
	// 没带id则返回数据库
	if (!route.params?.id) return router.replace({ name: "Knowledge" });

	// 同步当前tab显示状态
	data.curMenu = route.path.split("/")[2];
});
</script>

<style lang="less" scoped></style>
