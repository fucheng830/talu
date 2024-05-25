<template>
	<div class="flex flex-col gap-2 p-4">
		<!-- 输入 -->
		<SingleModule title="输入" @add="handleAddVar">
			<VariableList :list="data.form.input" />
		</SingleModule>

		<!-- 代码 -->
		<SingleModule title="代码" :hideBtn="true" :useGrid="false">
			<div class="h-[10rem] rounded-lg overflow-hidden">
				<CodeEditor v-model:value="data.form.txtCode" />
			</div>
		</SingleModule>

		<!-- 输出 -->
		<SingleModule title="输出" :useGrid="false">
			<!-- 右侧添加按钮 -->
			<template #extra>
				<n-button
					quaternary
					style="padding: 0.4rem"
					@click.stop="handleAddOutput"
				>
					<Icon icon="ph:plus" width="24" :color="globalColors.btnActive" />
				</n-button>
			</template>

			<n-data-table
				:columns="data.opt.output.columns"
				:data="data.form.output.data"
				:row-key="(row) => row.name"
				:default-expand-all="true"
				size="small"
			/>
		</SingleModule>
	</div>

	<!-- 左侧输入 -->
	<MyHandle type="target" color="#36ADEF" />
	<!-- 右侧输出 -->
	<MyHandle type="source" color="#36ADEF" />
</template>

<script setup lang="ts">
import { h, nextTick, onMounted, reactive, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import mCollapse from "@/components/common/mCollapse/index.vue";
import CodeEditor from "@/components/common/CodeEditor/index.vue";
import { NButton, NInput, NSelect } from "naive-ui";
import CodeAction from "@/views/application/vueFlow/components/pages/components/code/Action.vue";
import VariableList from "@/views/application/vueFlow/components/pages/components/VariableList.vue";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { useVueFlow } from "@vue-flow/core";

const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	form: {
		// 输入 变量列表
		input: [
			{
				name: "",
				type: "Reference", // 'Reference'|'input'
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
		],
		// 代码
		txtCode: `async function main({ params }: Args): Promise<Output> {
    const ret = {
        "key0": params.input + params.input,
        "key1": "hi",
        "key2": ["hello", "world"],
        "key3": {
            "key31": "hi"
        },
        "key4": [{
            "key41": true,
            "key42": 1,
            "key43": 12.88,
            "key44": ["hello"],
            "key45": {
                "key451": "hello"
            }
        }]
    };

    return ret;
}`,
		output: {
			data: [
				{
					name: "",
					type: "String",
					children: [
						{
							name: "",
							type: "String",
							children: [
								{
									name: "",
									type: "String",
								},
							],
						},
					],
				},
			],
		},
	},
	opt: {
		isInited: false,
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
		reference: [
			// {
			// 	label: "GPT",
			// 	value: "gpt",
			// }
		],
		output: {
			columns: [
				{
					title: "名称",
					key: "name",
					width: 200,
					className: "flex items-center",
					render: (row) =>
						h(NInput, {
							defaultValue: row.name,
							placeholder: "名称",
							// 值改变时
							onChange: (val) => {
								// !RESOLVED 使用官方演示的onUpdateValue时，直接修改原值会导致组件重新渲染，打断输入聚焦状态
								// !BUG 使用onChange会在输入框失焦时收起展开状态，疑似重新渲染
								row.name = val;
								// console.log(data.form.output.data);
							},
						}),
				},
				{
					title: "类型",
					key: "type",
					render: (row) =>
						h(NSelect, {
							defaultValue: row.type,
							options: data.opt.output.type,
							placeholder: "类型",
							// 值改变时
							"on-update:value": (val) => {
								row.type = val;
							},
						}),
				},
				{
					title: "",
					key: "action",
					width: 90,
					render: (row, index) =>
						h(CodeAction, {
							row,
							// 添加行
							onAdd: () => {
								if (!row.children) {
									row.children = [];
								}

								// 添加新行
								row.children.push({
									name: "",
									type: "String",
								});
							},
							// 删除行
							onDelete: () => {
								// 查找删除当前行
								const deleteCurRow = (data, row) => {
									for (let i = 0; i < data.length; i++) {
										const curRow = data[i];

										// 如果当前行与目标行相等，直接删除
										if (curRow === row) return data.splice(i, 1);

										// 如果当前行有children属性，则递归调用查找函数
										if (curRow.children) {
											deleteCurRow(curRow.children, row);

											// 如果当前行的children都被删除了，则也删除当前行
											// if (curRow.children.length === 0) {
											// 	data.splice(i, 1);
											// }
										}
									}
								};

								deleteCurRow(data.form.output.data, row);
							},
						}),
				},
			],
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
	},
});

// 添加变量
const handleAddVar = () => {
	data.form.input.push({
		name: "",
		type: "Reference", // 'Reference'|'input'
		valReference: undefined, // 引用 输入值
		valInput: "", // 输入 输入值
	});
};

// 搜索引用的值
const handleReferenceSearch = () => {
	// todo 引用可选项搜索接口
};

// 添加输出
const handleAddOutput = () => {
	data.form.output.data.push({
		name: "",
		type: "String",
		// children: [],
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
