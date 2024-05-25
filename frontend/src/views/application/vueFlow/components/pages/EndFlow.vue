<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-4 p-4">
		<!-- 模式 -->
		<div class="grid grid-cols-[30%_1fr] gap-2 items-center">
			<span class="font-bold">选择模式</span>

			<n-select v-model:value="data.form.mode" :options="data.opt.mode" />
		</div>

		<SingleModule title="输出变量" @add="handleAddVar">
			<VariableList :list="data.form.input" />
		</SingleModule>

		<!-- 左侧输入 -->
		<MyHandle type="target" color="#36ADEF" />
	</div>
</template>

<script setup lang="ts">
import { reactive, watch, defineProps, onMounted, nextTick } from 'vue';
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { Icon } from "@iconify/vue";
import VariableList from "@/views/application/vueFlow/components/pages/components/VariableList.vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import { useVueFlow } from "@vue-flow/core";

const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
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
		isInited: false,
		mode: [
			{
				label: "返回由智能体生成的变量",
				value: "generate",
			},
			{
				label: "使用回答内容直接回答",
				value: "directly",
			},
		],
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

// 添加变量
const handleAddVar = () => {
	data.form.input.push({
		name: "",
		type: "Reference",
		valReference: undefined, // 引用 输入值
		valInput: "", // 输入 输入值
	});
};

// 初始化
const init = () => {
	nextTick(() => {
		data.opt.isInited = true;
	});
};

onMounted(() => {
	init();
});

// watch中使用防抖执行无效，改为手动执行
let timerSaveForm;
watch(
	() => data.form,
	(val) => {
		clearTimeout(timerSaveForm);

		// 未初始化完不执行提交
		if (!data.opt.isInited) return;

		timerSaveForm = setTimeout(() => {
			// 更新flow组件内的node数据
			updateNodeData(props.node.id, { ...props.node?.data, form: val });
			// 更新自定义的节点数组数据
			emits("saveForm", props.node?.id, val);
		}, 2000);
	},
	{ deep: true }
);
</script>

<style lang="less" scoped></style>
