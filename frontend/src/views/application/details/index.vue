<template>
	<!-- 知识库详情 包围 -->
	<div class="relative w-full h-full p-[1rem] pl-0">
		<div
			class="w-full h-full flex border border-[#DFE2EA] rounded-2xl shadow-lg"
			:style="{ 'background-color': 'white' }"
		>
			<!-- 左侧栏 -->
			<div class="flex flex-col py-4 w-[200px] border-r">
				<!-- 知识库信息 -->
				<div class="flex flex-col gap-[14px] p-[14px] pt-0 mb-[14px]">
					<div class="flex items-center gap-2">
						<!-- 头像 -->
						<n-avatar
							round
							:size="34"
							src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg"
							style="min-width: 34px"
						/>
						<!-- 标题 -->
						<span
							class="w-full font-bold overflow-hidden text-ellipsis whitespace-nowrap"
						>
							{{ data.curKnowledge?.name }}
						</span>
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
								:color="item.key == data.curMenu ? globalColors.btnActive : ``"
								width="18"
							/>
							<!-- 菜单文本 -->
							<span
								:class="[item.key == data.curMenu && 'font-bold']"
								:style="{
									color: item.key == data.curMenu ? globalColors.btnActive : '',
								}"
							>
								{{ item.label }}
							</span>
						</div>
					</template>
				</div>

				<!-- 返回 知识库首页 -->
				<div
					class="flex items-center gap-3 px-6 py-2 cursor-pointer hover:bg-[#F4F4F7]"
					@click="router.push('/createai')"
				>
					<!-- 返回图标 箭头 左 -->
					<div
						class="p-1 rounded-full"
						:style="{ 'box-shadow': '1px 1px 9px rgba(0,0,0,.15)' }"
					>
						<Icon
							icon="gravity-ui:arrow-left"
							:color="globalColors.btnActive"
							width="22"
						/>
					</div>
					<span>我的应用</span>
				</div>
			</div>

			<!-- 右侧 内容区 -->
			<div class="flex-1">
				<router-view />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { globalColors } from "@/hooks/useTheme";
import { useKnowledgeStore } from "@/store";
import { computed, onMounted, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";

const route = useRoute();
const router = useRouter();
const knowledgeStore = useKnowledgeStore();

const data = reactive({
	curKnowledge: computed(() =>
		knowledgeStore.listKnowledge.find((item) => item.uuid == route.params.id)
	),
	curMenu: "dataset",
	progress: {
		qa: 100,
		index: 100,
	},
	opt: {
		menuList: [
			{
				label: "简易配置",
				key: "simpleConfig",
				pathName: "ApplicationDetails_simpleConfig",
				icon: "mi:bar-chart",
			},
			{
				label: "高级编排",
				key: "advancedFlow",
				pathName: "ApplicationDetails_advancedFlow",
				icon: "ph:stack-bold",
			},
			{
				label: "发布应用",
				key: "publishApp",
				pathName: "ApplicationDetails_publishApp",
				icon: "uil:setting",
			},
			{
				label: "对话日志",
				key: "chatHistory",
				pathName: "ApplicationDetails_chatHistory",
				icon: "uil:setting",
			},
			{
				label: "立即对话",
				key: "goChat",
				pathName: "Chat",
				icon: "uil:setting",
			},
		],
	},
});

const changeCurMenu = (item: any) => {
	data.curMenu = item.key;
	router.push({
		name: item.pathName,
		params: {
			id: route.params?.id,
		},
	});
};

onMounted(() => {
	// 没带id则返回数据库
	if (!route.params?.id) return router.replace({ name: "Knowledge" });
	data.curMenu = route.path.split("/")[2];
});
</script>

<style lang="less" scoped></style>
