<template>
	<div class="flex justify-center items-center py-2 bg-[#F8F8F8] border-b">
		<span>输入</span>
	</div>

	<!-- 触发器 -->
	<div class="relative flex items-center gap-1 px-4 py-2">
		<MyHandle color="#9CA2A8" />

		<span>触发器</span>

		<IconPopover>
			<div class="text-[14px]">
				<p>大部分时候,你不需要连接该属性。</p>
				<p>当你需要延迟执行，或精确控制执行时机时，可以连接该属性</p>
			</div>
		</IconPopover>
	</div>

	<!-- 选择知识库 -->
	<div class="relative gap-2 mt-4">
		<!-- 分组名 -->
		<div class="flex items-center gap-1 px-4">
			<span>选择知识库</span>
			<span class="text-[#F04438]">*</span>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
			<n-button block :color="globalColors.btnActive" @click="changeModalShow">
				<Icon icon="mage:mouse-pointer" />
				<span>选择</span>
			</n-button>

			<template v-for="item in data.knowledgeList" :key="item?.key">
				<div></div>
			</template>
		</div>
	</div>

	<ModalKnowledgeSelect ref="refModalSelect" />
</template>

<script setup lang="ts">
import IconPopover from "@/components/common/IconPopover/index.vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import { Icon } from "@iconify/vue";
import { reactive, ref } from "vue";
import { globalColors } from "@/hooks/useTheme.ts";
import ModalKnowledgeSelect from "@/views/application/vueFlow/components/pages/components/ModalKnowledgeSelect.vue";

const refModalSelect = ref();
const data = reactive({
	knowledgeList: [], // 选中的知识库
	opt: {},
});

// 改变选择模态框显示
const changeModalShow = () => {
	refModalSelect.value.changeModalShow();
};
</script>

<style lang="less" scoped></style>
