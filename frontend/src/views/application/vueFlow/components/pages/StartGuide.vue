<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<SingleModule title="输入" :useGrid="false" @add="handleAddVar">
			<div class="grid grid-cols-[25%_25%_1fr_3rem_3rem] gap-y-2 gap-x-2">
				<span class="text-[#1c1d2359] pl-2">名称</span>
				<span class="text-[#1c1d2359] pl-2">类型</span>
				<span class="text-[#1c1d2359] pl-2">描述</span>
				<span class="text-[#1c1d2359] pl-2">必选</span>
				<span></span>

				<template v-for="(curVar, index) in data.form.varList" :key="index">
					<!-- 名称 -->
					<n-input v-model:value="curVar.name" placeholder="请输入名称" />

					<!-- 类型 -->
					<n-select v-model:value="curVar.type" :options="data.opt.type" />

					<!-- 描述 -->
					<n-input v-model:value="curVar.desc" placeholder="描述变量的用途" />

					<!-- 必选 -->
					<div class="flex justify-center items-center">
						<n-checkbox v-model:checked="curVar.required" label="" />
					</div>

					<n-button text @click.stop="deleteVar(index)">
						<Icon icon="nimbus:stop" width="18" />
					</n-button>
				</template>
			</div>
		</SingleModule>
	</div>

	<!-- 右侧输出 -->
	<MyHandle type="source" color="#36ADEF" />
</template>

<script setup lang="ts">
import { nextTick, onMounted, reactive, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import { Icon } from "@iconify/vue";
import mCollapse from "@/components/common/mCollapse/index.vue";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { debounce, watchDebounce } from "@/utils/functions/debounce";
import { useVueFlow } from "@vue-flow/core";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	form: {
		varList: [
			{
				name: "",
				type: "string",
				desc: "",
				required: true,
			},
		],
	},
	opt: {
		isInited: false,
		type: [
			{
				label: "String",
				value: "String",
			},
			{
				label: "Integer",
				value: "Integer",
			},
			{
				label: "Boolean",
				value: "Boolean",
			},
			{
				label: "Number",
				value: "Number",
			},
			{
				label: "Object",
				value: "Object",
			},
			{
				label: "Array<String>",
				value: "Array<String>",
			},
			{
				label: "Array<Integer>",
				value: "Array<Integer>",
			},
			{
				label: "Array<Boolean>",
				value: "Array<Boolean>",
			},
			{
				label: "Array<Number>",
				value: "Array<Number>",
			},
			{
				label: "Array<Object>",
				value: "Array<Object>",
			},
		],
	},
});

// 添加变量
const handleAddVar = () => {
	data.form.varList.push({
		name: "",
		type: "string",
		desc: "",
		required: true,
	});
};

// 删除当前变量
const deleteVar = (index: number) => {
	data.form.varList.splice(index, 1);
};

// const saveForm = (val) => {
// 	debounce(() => {
// 		console.log("before", props.node);
// 		updateNodeData(props.node.id, val);
// 		console.log("after", props.node);
// 	}, 2000);
// };

// watch(
// 	() => data.form,
// 	(val) => {
// 		debounce(() => {
// 			console.log("before", props.node);
// 			updateNodeData(props.node.id, val);
// 			console.log("after", props.node);
// 		}, 2000);
// 	},
// 	{ deep: true }
// );

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
