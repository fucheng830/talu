<template>
	<BgTopBar :isShow="isMobile" :showAvatar="false" class="p-2">
		<n-scrollbar>
			<div
				class="w-full h-full flex-1 flex-col"
				:class="[
					isMobile ? 'pt-[10px] px-[16px] shadow-inner' : 'pt-[1rem] px-[56px]',
				]"
				:style="{ 'background-color': theme.baseColor }"
			>
				<div class="h-full flex flex-col gap-4">
					<!-- 单个板块 角色、工作流、插件 -->
					<template v-for="curBlock in data.blockList" :key="curBlock.title">
						<div class="border-b pb-4">
							<mCollapseTransition>
								<template #header="{ changeCollapsed }">
									<div
										class="flex justify-between items-center mr-4"
										@click="changeCollapsed"
									>
										<header class="pt-[.5rem] flex items-center select-none">
											<!-- 标签左侧标线 -->
											<div
												class="w-[6px] h-[50px] rounded-[3px] mr-[24px]"
												:style="{ 'background-color': theme.primaryColor }"
											></div>
											<div class="flex flex-col">
												<!-- 标题 -->
												<span
													class="font-bold"
													:class="[!isMobile ? 'text-[22px]' : 'text-[22px]']"
												>
													{{ curBlock.title }}
												</span>

												<!-- 描述 -->
												<span
													v-if="!isMobile && curBlock?.desc?.length > 0"
													:class="[!isMobile ? 'text-[14px]' : 'text-[12px]']"
												>
													{{ curBlock.desc }}
												</span>
											</div>
										</header>

										<!-- 新增按钮 -->
										<n-button
											:color="theme.primaryColor"
											ghost
											@click.stop="handleAdd(curBlock)"
										>
											<span class="flex items-center px-2">
												<Icon icon="ic:round-plus" width="24" />
												创建
											</span>
										</n-button>
									</div>
								</template>

								<!-- 有数据 -->
								<template v-if="curBlock?.data?.length > 0">
									<!-- 数据列表 -->
									<ul
										class="mt-[32px] grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-[20px] mb-[2rem]"
									>
										<!-- 单个数据 -->
										<template v-for="(item, i) in curBlock.data" :key="item.id">
											<li
												@click="handleGo(curBlock, item)"
												class="relative bg-[white] border cursor-pointer rounded-lg py-[12px] px-[18px]"
											>
												<!-- 右上角 下拉菜单 -->
												<div
													@click.stop="() => {}"
													class="absolute top-[1rem] right-[1rem]"
												>
													<NDropdown
														trigger="hover"
														:options="data.opt.dropdownMenu"
														@select="
															(key) => handleMenuSelect(key, item, curBlock)
														"
													>
														<button
															class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200"
														>
															<Icon
																icon="ri:more-fill"
																width="20"
																color="#111824"
															/>
														</button>
													</NDropdown>
												</div>

												<!-- 内容 卡片 -->
												<div class="items-center flex pb-2">
													<div
														class="flex items-center justify-center w-[56px] h-[56px]"
													>
														<!-- 换成图像 -->
														<img
															:src="item.avatar"
															alt="图像"
															width="56"
															class="rounded-full"
														/>
													</div>
													<span class="font-bold text-[18px] pl-[10px]">
														{{ item.name }}
													</span>
												</div>
												<div class="mb-5">
												<p class="text-[#84818F] text-[12px] overflow-hidden line-clamp-1">
													{{ item.description || "这个应用还没写介绍~" }}
												</p>
												</div>

												
												<!-- 私有/公开 -->
												<!-- <div class="absolute bottom-0 flex items-center">
													<Icon
													icon="bx:lock"
													color="#485264"
													width="19"
													class="pb-[2px]"
													/>
													<span class="text-[#485264]">私有</span>
												</div> -->
												
											</li>
										</template>
									</ul>
								</template>

								<!-- 无数据 -->
								<div v-else class="h-[6rem] flex justify-center items-center">
									<span class="text-[grey] select-none">暂无数据</span>
								</div>
							</mCollapseTransition>
						</div>
					</template>
				</div>
			</div>
		</n-scrollbar>
	</BgTopBar>

	<UpgradeVip ref="refUpgradeVip" />
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { onMounted, computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import UpgradeVip from "./components/UpgradeVip.vue";
import BgTopBar from "@/views/layout/BgTopBar.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { mCollapseTransition } from "@/components/common";
import { useIconRender } from "@/hooks/useIconRender";
import { useFlowStore, useKnowledgeStore, useStateStore } from "@/store";
import { api } from "@/api/common";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const knowledgeStore = useKnowledgeStore();
const stateStore = useStateStore();
const flowStore = useFlowStore();
const { iconRender } = useIconRender();
const { isMobile } = useBasicLayout();
const router = useRouter();

// 升级会员弹窗
const refUpgradeVip = ref();
const data = reactive({
	blockList: [
		{
			key: "role",
			title: t("createai.myAgent"),
			desc: t("createai.myAgentDesc"),
			url: "/createai/createrole", // 详情url
			data: computed(() => stateStore.$state.myAgents),
		},
		{
			key: "flow",
			title: t("createai.myFLow"),
			desc: t("createai.myFLowDesc"),
			url: "/createai/application/advancedFlow",
			data: computed(() => flowStore.flowList),
		},
		{
			key: "plugin",
			title: "我的插件",
			desc: "根据你的个人需求创建插件",
			// todo 替换为创建插件路由
			url: "/createai/plugins",
			data: [],
		},
	],
	opt: {
		dropdownMenu: [
			{
				label: t("common.edit"),
				key: "edit",
				icon: iconRender({ icon: "akar-icons:edit" }),
			},
			{
				label: t("common.delete"),
				key: "delete",
				icon: iconRender({ icon: "ri:delete-bin-line" }),
			},
		],
	},
});

// 下拉菜单 选择 (当前操作key，当前数据，当前block配置)
const handleMenuSelect = (key: string | number, item, curBlock) => {
	switch (key) {
		// 编辑
		case "edit":
			// 携带当前id进入编辑(新增)页
			console.log('进入'+`${curBlock.url}/${item.id}`);
			router.push(`${curBlock?.url}/${item?.id}`);
			break;

		// 删除
		case "delete":
			handleDeleteApp(item);
			data.showModalDeleteApp = true;
			data.curDeleteUUID = item.id;
			break;
	}
};

// 新增
const handleAdd = (curBlock) => {
	router.push(curBlock?.url);
};

// 删除
const handleDeleteApp = (item) => {
	api.delete_agent({ id: item.id }).then((res) => {
		// 删除成功后清理本地数据
		stateStore.$state.myAgents = stateStore.$state.myAgents.filter(
			(v) => v.id !== item.id
		);
	});
};

// 转到对应页面
const handleGo = (curBlock, item) => {
	console.log(curBlock);
	// 显示开通会员弹窗
	// if (!url) return refUpgradeVip.value.changeModalShow();
	// if (!item.url) return;

	if (curBlock.key == "role") return router.push(`/chat/${item.id}`);
	console.log(curBlock?.url);
	router.push(`${curBlock?.url}/${item?.id}`);
};

// 在组件挂载时获取数据
onMounted(async () => {
	// 获取我的智能体
	await stateStore.updateMyAgents();
});
</script>

<style></style>
