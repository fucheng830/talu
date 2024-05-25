<template>
	<!-- 模块 触发器 -->
	<div class="relative flex justify-between gap-2 my-4">
		<!-- 触发器 -->
		<div class="relative flex items-center gap-1 px-4 mt-2">
			<MyHandle color="#9CA2A8" />

			<span>触发器</span>

			<IconPopover>
				<p>大部分时候,你不需要连接该属性</p>
				<p>当你需要延迟执行,或精确控制执行时机时，可以连接该属性。</p>
			</IconPopover>
		</div>
	</div>

	<!-- 模块 回复的内容 -->
	<div class="flex flex-col gap-2">
		<!-- 分组名 -->
		<div class="relative flex items-center gap-1 px-4">
			<MyHandle color="#36ADEF" />

			<span>回复的内容</span>

			<IconPopover>
				<p>可以使用\n 来实现连续换行。</p>
				<p>
					可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。
				</p>
				<p>如传入非字符串类型数据将会自动转成字符</p>
			</IconPopover>
		</div>

		<!-- 回复的内容 输入框 -->
		<div class="flex flex-col px-4">
			<n-input
				v-model:value="data.form.txtReply"
				type="textarea"
				:autosize="{
					minRows: 7,
					maxRows: 10,
				}"
				:placeholder="`可以使用 \\n 来实现连续换行。
 可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。
 如传入非字符串类型数据将会自动转成字符`"
				style="font-size: 12px"
			/>
		</div>
	</div>

	<!-- 模块调用结束 -->
	<div class="relative flex flex-row-reverse items-center gap-1 px-4 mt-2">
		<MyHandle type="source" color="#E7D118" />
		<span>模块调用结束</span>
		<IconPopover>
			<p>模块调用结束时触发</p>
		</IconPopover>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { Icon } from "@iconify/vue";
import IconPopover from "@/components/common/IconPopover/index.vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";

const data = reactive({
	form: {
		txtReply: "",
	},
});
</script>

<style lang="less" scoped></style>
