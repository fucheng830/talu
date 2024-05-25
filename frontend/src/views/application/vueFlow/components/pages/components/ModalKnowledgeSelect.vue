<template>
	<mModal
		ref="refModal"
		title="选择知识库"
		footerBtnSize="medium"
		footerComfirmBtnType="primary"
		txtCancel="关闭"
		txtConfirm="完成"
		@onShowChange="onShowChange"
		@onPositiveClick="handleComfirm"
		style="
			width: 90%;
			max-width: 900px;
			position: fixed;
			top: 10%;
			left: 50%;
			transform: translate(-50%, 0);
		"
	>
		<!-- 选中的知识库 -->
		<div class="flex"></div>

		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
			<template v-for="item in data.opt.knowledgeList" :key="item?.uuid">
				<!-- 知识库列表 -->
				<div class="flex flex-col">
					<div
						class="flex items-center gap-2 p-4 border rounded-lg hover:shadow-lg"
					>
						<div class="w-[34px] min-w-[34px] pt-1">
							<n-avatar round size="medium" :src="logo" />
						</div>
						<span class="text-[18px] font-bold">{{ item.name }}</span>
					</div>

					<div class="flex justify-end">
						<!-- 知识库类型？ -->
					</div>
				</div>
			</template>
		</div>
	</mModal>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useKnowledgeStore } from "@/store";
import mModal from "@/components/common/mModal/index.vue";
import logo from "@/assets/logo.png";

const konwledgeStore = useKnowledgeStore();

const refModal = ref();
const data = reactive({
	curKnowledgeList: [],
	opt: {
		knowledgeList: computed(() => konwledgeStore.listKnowledge),
	},
});

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return;

	console.log(konwledgeStore.listKnowledge);
};

// 确认
const handleComfirm = () => {
	console.log("commit");
	// todo 提交选择
};

// 改变模态框显示
const changeModalShow = () => {
	refModal.value.toggleModal();
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
