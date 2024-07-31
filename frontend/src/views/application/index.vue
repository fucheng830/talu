<template>
	<div
		class="w-full h-full flex-1 flex-col px-[56px]"
	>
		<header class="py-[22px] flex justify-between items-center border-b">
			<div class="flex items-center">
				<div
					class="w-[6px] h-[50px] rounded-[3px] mr-[24px]"
				></div>
				<div class="flex flex-col">
					<span class="font-bold text-[24px]"> 我的应用 </span>
				</div>
			</div>

			<div class="mr-[20px]">
				<n-button
					ghost
					:style="{ 'border-radius': globalConfig.btnRadius }"
					@click="changeModalAddAppShow"
				>
					<span class="flex items-center px-2">
						<Icon icon="ic:round-plus" width="24" />
						新增
					</span>
				</n-button>
			</div>
		</header>

		<!-- 应用列表 -->
		<ul
			class="mt-[32px] grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-[20px] mb-[2rem]"
		>
			<!-- 单个知识库 -->
			<template v-for="(item, i) in data.appList" :key="i">
				<li
					@click="goAppDetails(item)"
					class="relative bg-[white] border cursor-pointer rounded-lg py-[12px] px-[18px]"
				>
					<!-- 右上角 下拉菜单 -->
					<div @click.stop="() => {}" class="absolute top-[1rem] right-[1rem]">
						<NDropdown
							trigger="hover"
							:options="data.opt.dropdownMenu"
							@select="(key) => handleMenuSelect(key, item.uuid)"
						>
							<button
								class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200"
							>
								<Icon icon="ri:more-fill" width="20" color="#111824" />
							</button>
						</NDropdown>
					</div>

					<!-- 内容 卡片 -->
					<div class="items-center flex pb-2">
						<div
							class="bg-[#F6F5F9] rounded-full flex items-center justify-center w-[56px] h-[56px] text-[44px]"
						>
							<Icon icon="tdesign:data" width="34" />
						</div>
						<span class="font-bold text-[18px] pl-[10px]">
							{{ item.name }}
						</span>
					</div>
					<p class="text-[#84818F] text-[12px]">
						{{ item.desc || "这个应用还没写介绍~" }}
					</p>
					<div class="flex justify-between items-center mt-4">
						<!-- 私有/公开 -->
						<div class="flex items-center">
							<Icon
								icon="bx:lock"
								color="#485264"
								width="19"
								class="pb-[2px]"
							/>
							<span class="text-[#485264]">私有</span>
						</div>

						<!-- 知识库类型 -->
						<div
							class="flex items-center gap-1 border bg-[#F4F4F7] border-[#E8EBF0] rounded-lg px-2 py-1 text-[12px]"
						>
							<Icon
								icon="mingcute:storage-fill"
								color="#8A95A7"
								width="19"
								class="pb-[2px]"
							/>
							<span>通用知识库</span>
						</div>
					</div>
				</li>
			</template>
		</ul>

		<!-- 上传模态框 -->
		<AddApp ref="refModalAddApp" />
		<!-- 确认删除模态框 -->
		<n-modal
			v-model:show="data.showModalDeleteApp"
			preset="dialog"
			type="info"
			:icon="
				() =>
					renderIcon({
						icon: 'jam:triangle-danger-f',
						width: 18,
						color: '#7A7AF9	',
					})
			"
			title="删除提示"
			content="确认删除该应用所有信息？"
			positive-text="确认"
			negative-text="算了"
			:negative-button-props="{
				size: 'large',
			}"
			:positive-button-props="{
				size: 'large',
			}"
			@positive-click="handleDeleteApp"
		/>
	</div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { globalConfig } from "@/hooks/useTheme";
import { reactive, ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import AddApp from "@/views/application/components/AddApp.vue";
import { useKnowledgeStore } from "@/store";
import { useIconRender } from "@/hooks/useIconRender";
import { renderIcon } from "@/utils/functions";

const router = useRouter();

const { iconRender } = useIconRender();
const knowledgeStore = useKnowledgeStore();

// ref 上传模态框
const refModalAddApp = ref();
const data = reactive({
	// 知识库列表
	// todo 替换为app列表
	appList: computed(() => knowledgeStore.listKnowledge),
	curDeleteUUID: "", // 当前要删除的应用UUID
	showModalDeleteApp: false, // 确认删除模态框
	opt: {
		dropdownMenu: [
			{
				label: "删除",
				key: "delete",
				icon: iconRender({ icon: "ri:delete-bin-line" }),
			},
		],
	},
});

// 显示新增应用模态框
const changeModalAddAppShow = () => {
	if (refModalAddApp.value) {
		refModalAddApp.value.changeModalShow();
	}
};

// 更新知识库列表
// const updateKnowledgeList = () => {
// 	knowledgeStore.getListKnowledge();
// };

// 删除应用
const handleDeleteApp = (index: string) => {
	console.log(index);
	// todo 请求接口 删除应用
	// api.delete_knowledge({ knowledge_id: data.curDeleteUUID }).then(() => {
	// 	if (res.status != "Success") return msg.error(res.message);

	// 	msg.success(res.message);
	// 	updateKnowledgeList();
	// });
};

// 下拉菜单 选择
const handleMenuSelect = (key: string | number, item) => {
	switch (key) {
		// 删除
		case "delete":
			// handleDeleteApp(item);
			data.showModalDeleteApp = true;
			data.curDeleteUUID = item.uuid;
	}
};

// 前往 知识库详情
const goAppDetails = (item: any) => {
	router.push({
		name: "ApplicationDetails_simpleConfig",
		params: {
			id: item?.uuid,
		},
	});
};

onMounted(() => {
	// updateKnowledgeList();
});
</script>

<style></style>
