<template>
	<BgTopBar :isShow="isMobile" :showAvatar="false" class="p-2">
		<n-scrollbar>
			<div
				class="w-full h-full flex flex-col"
				:class="[
					isMobile ? 'pt-[10px] px-[16px] shadow-inner' : 'pt-[1rem] px-[56px]',
				]"
			>
				<div
					class="grow shrink-0 flex justify-between items-center mr-4"
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
								{{ $t("knowledge.createKnowledge") }}
							</span>

							<!-- 描述 -->
							<span
								v-if="!isMobile"
								:class="[!isMobile ? 'text-[14px]' : 'text-[12px]']"
							>
								{{ $t("knowledge.knowledgeSubtitle") }}
							</span>
						</div>
					</header>

					<!-- 新增按钮 -->
					<n-button
						:color="theme.primaryColor"
						ghost
						@click.stop="changeUploadModalShow"
					>
						<span class="flex items-center px-2">
							<Icon icon="ic:round-plus" width="24" />
							{{ $t("common.create") }}
						</span>
					</n-button>
				</div>

				<ul
					class="mt-[32px] grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-[20px] mb-[6rem]"
				>
					<!-- 单个知识库 -->
					<template v-for="(item, i) in data.knowledgeList" :key="i">
						<li
							@click="goKnowledgeDetails(item)"
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
									@select="(key) => handleMenuSelect(key, item)"
								>
									<button
										class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200"
									>
										<Icon icon="ri:more-fill" width="20" color="#111824" />
									</button>
								</NDropdown>
							</div>

							<!-- 内容 卡片 -->
							<div class="items-center flex pb-[16px]">
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
								{{ item.desc || $t("knowledge.noDesc") }}
							</p>
							<div class="flex justify-between items-center">
								<!-- 私有/公开? -->
								<div></div>

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
									<span>{{ $t("knowledge.commonKnowledge") }}</span>
								</div>
							</div>
						</li>
					</template>
				</ul>

				<!-- 上传模态框 -->
				<KnowledgeSetting ref="refModalUpload" />

				<!-- 确认删除模态框 -->
				<n-modal
					v-model:show="data.showModalDelete"
					preset="dialog"
					type="error"
					:icon="
						() =>
							renderIcon({
								icon: 'jam:triangle-danger-f',
								width: 18,
								color: '#FB6547',
							})
					"
					:title="$t('common.delete')"
					:content="$t('knowledge.deleteComfirm')"
					:positive-text="$t('common.confirm')"
					:negative-text="$t('common.forgetIt')"
					:negative-button-props="{
						size: 'large',
					}"
					:positive-button-props="{
						size: 'large',
					}"
					@positive-click="handleDeleteKnowledge"
				/>
			</div>
		</n-scrollbar>
	</BgTopBar>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { reactive, ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import KnowledgeSetting from "@/views/knowledge/components/KnowledgeSetting.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { api } from "@/api/common";
import { useKnowledgeStore } from "@/store";
import { useIconRender } from "@/hooks/useIconRender";
import { useMessage } from "naive-ui";
import { renderIcon } from "@/utils/functions";
import BgTopBar from "@/views/layout/BgTopBar.vue";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const router = useRouter();

const msg = useMessage();
const { iconRender } = useIconRender();
const { isMobile } = useBasicLayout();
const knowledgeStore = useKnowledgeStore();

// ref 上传模态框
const refModalUpload = ref();
const data = reactive({
	// 知识库列表
	knowledgeList: computed(() => knowledgeStore.listKnowledge),
	// roleList: [
	// 	{
	// 		title: "创建知识库",
	// 		icon: "codicon:new-folder",
	// 		desc: "导入您自己的文本数据或通过 Webhook 实时写入数据以增强 LLM 的上下文。",
	// 		//   url: "/createai/createRole",
	// 	},
	// ],
	curDeleteUUID: "", // 当前要删除的知识库UUID
	showModalDelete: false, // 确认删除模态框
	opt: {
		dropdownMenu: [
			{
				label: t("common.delete"),
				key: "delete",
				icon: iconRender({ icon: "ri:delete-bin-line" }),
			},
		],
	},
});

// 打开上传模态框
const changeUploadModalShow = () => {
	if (refModalUpload.value) {
		refModalUpload.value.changeModalShow();
	}
};

// 更新知识库列表
const updateKnowledgeList = () => {
	knowledgeStore.getListKnowledge();
};

// 删除知识库
const handleDeleteKnowledge = () => {
	api.delete_knowledge({ knowledge_id: data.curDeleteUUID }).then((res) => {
		if (res.status != "Success") return msg.error(res.message);

		msg.success(res.message);
		updateKnowledgeList();
	});
};

// 下拉菜单 选择
const handleMenuSelect = (key: string | number, item: any) => {
	switch (key) {
		// 删除
		case "delete":
			// handleDeleteKnowledge(item);
			data.showModalDelete = true;
			data.curDeleteUUID = item.uuid;
	}
};

// 前往 知识库详情
const goKnowledgeDetails = (item: any) => {
	router.push("/knowledgeDetails/dataset/" + item.uuid);
};

onMounted(() => {
	updateKnowledgeList();
});
</script>

<style></style>
