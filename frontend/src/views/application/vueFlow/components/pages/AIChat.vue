<template>
	<div class="flex justify-center items-center py-2 bg-[#F8F8F8] border-b">
		<span>输入</span>
	</div>

	<!-- 模块 触发器 -->
	<div class="flex flex-col gap-4">
		<!-- 分组名 -->
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

		<div class="flex flex-col px-4">
			<div class="mb-1">
				AI 模型
				<span class="text-[#F04438]">*</span>
			</div>

			<n-select v-model:value="data.form.AIModel" :options="data.opt.AIModel" />

			<div class="py-6">
				<n-button @click="changeModalAIModelShow">
					<Icon icon="uiw:setting-o" width="14" />
					<span class="ml-2"> AI 配置 </span>
				</n-button>
			</div>
		</div>
	</div>

	<!-- 模块 提示词 -->
	<div class="flex flex-col gap-2">
		<!-- 分组名 -->
		<div class="relative flex items-center gap-1 px-4">
			<MyHandle color="#36ADEF" />

			<span>提示词</span>

			<IconPopover>
				<p class="text-[14px] whitespace-pre-wrap">
					{{ data.opt.txtTipPlaceholder }}
				</p>
			</IconPopover>
		</div>

		<div class="flex flex-col px-4">
			<n-input
				v-model:value="data.form.txtTip"
				type="textarea"
				:autosize="{
					minRows: 5,
					maxRows: 10,
				}"
				placeholder="模型固定的引导词,通过调整该内容,可以引导模型聊天方向。该内容会被固定在上下文的开头。可使用变量，例如 {{language}}"
			/>
		</div>
	</div>

	<!-- 模块 聊天记录 -->
	<div class="flex flex-col gap-2 mt-4">
		<!-- 分组名 -->
		<div class="relative flex items-center gap-1 px-4 mt-2">
			<MyHandle color="#00A9A6" />

			<span>聊天记录</span>
			<span class="text-[#F04438]">*</span>
		</div>

		<div class="px-4">
			<n-input-number v-model:value="data.form.txtChatHistory" clearable />
		</div>
	</div>

	<!-- 模块 用户问题 -->
	<div class="relative flex justify-between gap-2 mt-6">
		<!-- 分组名 -->
		<div class="flex items-center gap-1 px-4">
			<MyHandle color="#36ADEF" />
			<span>用户问题</span>
			<span class="text-[#F04438]">*</span>
		</div>

		<!-- 用户问题 右侧输出 -->
		<div class="flex items-center gap-1 px-4">
			<MyHandle type="source" color="#36ADEF" />
			<span>用户问题</span>
		</div>
	</div>

	<!-- 模块 知识库引用 -->
	<div class="relative flex justify-between gap-2 my-4">
		<!-- 分组名 -->
		<div class="relative flex items-center gap-1 px-4 mt-2">
			<MyHandle color="#A558C9" />

			<span>知识库引用</span>

			<IconPopover>
				<p>可接收知识库搜索的结果。</p>
			</IconPopover>
		</div>
	</div>

	<div class="flex justify-center items-center py-2 bg-[#F8F8F8] border-y">
		<span>输出</span>
	</div>

	<!-- 底部输出部分 -->
	<div class="flex flex-col justify-end gap-4 mt-2">
		<!-- 模块调用结束 -->
		<div class="relative flex flex-row-reverse items-center gap-1 px-4 mt-2">
			<MyHandle type="source" color="#E7D118" />
			<span>模块调用结束</span>
			<IconPopover>
				<p>模块调用结束时触发</p>
			</IconPopover>
		</div>

		<!-- AI回复内容 -->
		<div class="relative flex flex-row-reverse items-center gap-1 px-4 mt-2">
			<MyHandle type="source" color="#36ADEF" />
			<span>AI回复内容</span>
			<IconPopover>
				<p>将在 stream 回复完毕后触发</p>
			</IconPopover>
		</div>

		<!-- 新的上下文 -->
		<div class="relative flex flex-row-reverse items-center gap-1 px-4 mt-2">
			<MyHandle type="source" color="#00A9A6" />
			<span>新的上下文</span>
			<IconPopover>
				<p>将在本次 回复内容拼接上历史记录，作为新的上下文返回</p>
			</IconPopover>
		</div>
	</div>

	<ModalAIModel ref="refModalAIModel" />
</template>

<script setup lang="ts">
import IconPopover from "@/components/common/IconPopover/index.vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import ModalAIModel from "@/views/application/vueFlow/components/pages/components/ModalAIModel.vue";

const props = defineProps({
	node: {
		type: Object,
		default: {},
	},
});

const refModalAIModel = ref();
const data = reactive({
	form: {
		AIModel: "QuChat-4k",
		txtTip: "",
		txtChatHistory: 0,
	},
	opt: {
		AIModel: [
			{
				label: "QuChat-4k",
				value: "QuChat-4k",
			},
			{
				label: "QuChat-plus",
				value: "QuChat-plus",
			},
		],
		txtTipPlaceholder: `模型固定的引导词，通过调整该内容，可以引导模型聊天方向。
该内容会被固定在上下文的开头。
可使用变量，例如{{language}}`,
	},
});

// 改变AI模型模态框显示状态
const changeModalAIModelShow = () => {
	refModalAIModel.value.changeModalShow();
};
</script>

<style lang="less" scoped></style>
