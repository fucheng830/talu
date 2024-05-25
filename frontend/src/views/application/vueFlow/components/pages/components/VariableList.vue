<template>
	<template v-for="(curVar, index) in props.list" :key="index">
		<!-- 名称 -->
		<n-input v-model:value="curVar.name" placeholder="请输入名称" />

		<!-- 值 -->
		<div class="flex items-center">
			<n-input-group>
				<!-- 类型 -->
				<n-select v-model:value="curVar.type" :options="data.opt.input.type" />

				<!-- 引用 值 -->
				<template v-if="curVar.type === 'Reference'">
					<!-- !todo loading值放 data.form.varList的话，如果要监测form变化后执行方法，可能会陷入死循环，可能需要单独用一个数组储存各变量的loading，现暂用options个数判断 -->
					<n-select
						v-model:value="curVar.valReference"
						filterable
						placeholder="引用"
						:options="data.opt.reference"
						:loading="data.opt.reference?.length <= 0"
						clearable
						remote
						@search="handleReferenceSearch"
					/>
				</template>

				<!-- input 值 -->
				<template v-else>
					<n-input v-model:value="curVar.valInput" placeholder="请输入值" />
				</template>
			</n-input-group>

			<n-button
				text
				@click.stop="handleDeleteVar(index)"
				style="padding: 0 0.8em"
			>
				<Icon icon="nimbus:stop" width="14" />
			</n-button>
		</div>
	</template>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { defineProps, reactive } from "vue";

const emits = defineEmits(["deleteVar"]);
const props = defineProps({
	list: {
		type: Array,
		default: [],
	},
});

const data = reactive({
	form: {
		mode: "generate",
		input: [
			{
				name: "",
				type: "Reference",
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
		],
	},
	opt: {
		input: {
			type: [
				{
					label: "引用",
					value: "Reference",
				},
				{
					label: "输入",
					value: "Input",
				},
			],
		},
	},
});

// 删除变量
const handleDeleteVar = (index: number) => {
	props.list.splice(index, 1);
	emits("deleteVar");
};
</script>

<style lang="less" scoped></style>
