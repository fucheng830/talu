<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<!-- 包一层div，防止切换时高度抖动 -->
		<div class="h-[2.5rem]">
			<n-tabs v-model:value="data.mode" type="segment" animated>
				<!-- 单次 -->
				<n-tab-pane name="SingleTime" tab="单次"> </n-tab-pane>
				<!-- 批量 -->
				<n-tab-pane name="BatchProcessing" tab="批量"> </n-tab-pane>
			</n-tabs>
		</div>

		<div class="flex flex-col gap-4">
			<!-- 模型、相关度 -->
			<div class="flex bg-[#F7F7F7] rounded-lg p-2 pb-4">
				<div class="flex-1 py-1 px-2">
					<div class="text-[#1c1f23cc] mb-1">模型</div>
					<n-select
						v-model:value="data.form.single.model"
						:options="data.opt.single.model"
					/>
				</div>
				<div class="flex-1 py-1 px-2 border-l">
					<div class="text-[#1c1f23cc] mb-1">
						模型<span class="text-[red]">*</span>
					</div>
					<n-input-number
						v-model:value="data.form.single.temperature"
						type="number"
						placeholder=""
					/>
				</div>
			</div>

			<!-- 批量 -->
			<template v-if="data.mode === 'BatchProcessing'">
				<SingleModule title="批量" :useGrid="false" @add="handleAddBatchVar">
					<div class="grid grid-cols-[30%_1fr_auto] gap-2">
						<template
							v-for="(curVar, index) in data.form.batch.varList"
							:key="index"
						>
							<!-- 名称 -->
							<n-input v-model:value="curVar.name" placeholder="请输入名称" />

							<!-- 值 -->
							<n-select
								v-model:value="curVar.value"
								:options="data.opt.batch.variable[index]"
								placeholder="请选择值"
							/>

							<n-button
								text
								@click.stop="handleDeleteBatchVar(index)"
								style="padding: 0 0.8em"
							>
								<Icon icon="nimbus:stop" width="14" />
							</n-button>
						</template>
					</div>
				</SingleModule>
			</template>

			<!-- 输入 -->
			<SingleModule title="输入" @add="handleAddVar">
				<VariableList :list="data.form.single.input" />
			</SingleModule>

			<!-- 提示词 -->
			<SingleModule title="回答内容" :useGrid="false">
				<n-input
					v-model:value="data.form.single.prompt"
					type="textarea"
					:autosize="{
						minRows: 4,
						maxRows: 7,
					}"
					:placeholder="`您可以使用 {{变量名}}、{{变量.子变量名}}、{{变量[对应数组下标]}} 来引用输入参数中的变量。`"
				/>
			</SingleModule>

			<!-- 输出 -->
			<SingleModule title="输出" :useGrid="false">
				<!-- 右侧添加按钮 -->
				<template #extra>
					<n-button
						quaternary
						style="padding: 0.4rem"
						:disabled="data.mode == 'BatchProcessing'"
						@click.stop="handleAddOutput"
					>
						<Icon
							icon="ph:plus"
							width="24"
							:color="
								data.mode == 'BatchProcessing'
									? '#1c1f2359'
									: globalColors.btnActive
							"
						/>
					</n-button>
				</template>

				<n-data-table
					:columns="data.opt.single.output.columns"
					:data="
						data.mode == 'BatchProcessing'
							? [
									{
										name: 'outputList',
										type: 'Array<Object>',
										desc: '',
										children: data.form.single.output,
										disabled: true,
									},
							  ]
							: data.form.single.output
					"
					:row-key="(row) => row.name"
					:default-expand-all="true"
					size="small"
				/>
			</SingleModule>
		</div>
	</div>

	<!-- 左侧输入 -->
	<MyHandle type="target" color="#36ADEF" />
	<!-- 右侧输出 -->
	<MyHandle type="source" color="#36ADEF" />
</template>

<script setup lang="ts">
import { computed, h, nextTick, onMounted, reactive, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { useChatStore } from "@/store";
import VariableList from "@/views/application/vueFlow/components/pages/components/VariableList.vue";
import { NInput, NSelect } from "naive-ui";
import CodeAction from "@/views/application/vueFlow/components/pages/components/code/Action.vue";
import { useVueFlow } from "@vue-flow/core";

const chatStore = useChatStore();
const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	mode: "SingleTime", // 单次/批量	SingleTime/BatchProcessing
	form: {
		// 单次
		single: {
			model: "", // 模型
			temperature: 0.7, // 相关度
			// 输入 变量列表
			input: [
				{
					name: "",
					type: "Reference", // 'Reference'|'input'
					valReference: undefined, // 引用 输入值
					valInput: "", // 输入 输入值
				},
			],
			prompt: "", // 提示词
			output: [
				{
					name: "",
					type: "String",
					desc: "",
				},
				{
					name: "",
					type: "String",
					desc: "",
				},
			], // 输出 变量列表
		},
		// 批量
		batch: {
			// 变量列表
			varList: [
				{
					name: "",
					value: undefined,
				},
			],
			maximumTimes: 10, // 最大次数
		},
	},
	opt: {
		isInited: false,
		single: {
			model: computed(() =>
				chatStore.agentList.map((item) => ({
					label: item.name,
					value: item.id,
				}))
			),
			output: {
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
						disabled: true,
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
						disabled: true,
					},
				],
				descRows: [1],
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
								disabled: row?.disabled,
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
						width: 180,
						// className: "flex items-start",
						render: (row) =>
							h(NSelect, {
								defaultValue: row.type,
								options: data.opt.single.output.type,
								placeholder: "类型",
								disabled: row?.disabled,
								// 值改变时
								"on-update:value": (val) => {
									row.type = val;
								},
							}),
					},
					{
						title: "描述",
						key: "desc",
						render: (row, index) =>
							h(NInput, {
								defaultValue: row.desc,
								type: "textarea",
								placeholder: "描述变量的用途",
								// 聚焦时显示3行
								autosize: getCurOptoutSize(index, row),
								maxlength: 300,
								showCount: getCurOutputRowsIndex(index, row) > 1,
								disabled: row?.disabled,
								// 值改变时
								"on-update:value": (val) => {
									row.desc = val;
								},
								onFocus: () => changeOutputRows(row),
								onBlur: () => handleOutputDescBlur(row),
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
											}
										}
									};

									deleteCurRow(data.form.single.output, row);
								},
							}),
					},
				],
			},
		},
		batch: {
			variable: [[]],
		},
	},
});

// 单次 输入 添加变量
const handleAddVar = () => {
	data.form.single.input.push({
		name: "",
		type: "Reference", // 'Reference'|'input'
		valReference: undefined, // 引用 输入值
		valInput: "", // 输入 输入值
	});
};

// 批量 添加变量
const handleAddBatchVar = () => {
	data.form.batch.varList.push({
		name: "",
		value: undefined,
	});

	// 添加对应候选空列表，供搜索时更新
	data.opt.batch.variable.push([]);
};

// 批量 删除变量
const handleDeleteBatchVar = (index: number) => {
	// 删除对应变量表单
	data.form.batch.varList.splice(index, 1);
	// 删除对应候选列表
	data.opt.batch.variable.splice(index, 1);
};

// 单次 输出 添加变量
const handleAddOutput = () => {
	data.form.single.output.push({
		name: "",
		type: "String",
		desc: "",
	});
};

// 单次 输出 删除当前变量
const deleteOutputVar = (index: number) => {
	data.form.single.output.splice(index, 1);
	// 同步删除对应候选列表
	data.opt.single.output.descRows.splice(index, 1);
};

// 获取当前输出变量的索引
const getCurOutputIndex = (data, row) => {
	for (let i = 0; i < data.length; i++) {
		const curRow = data[i];

		// 如果当前行与目标行相等，直接删除
		if (curRow === row) return i;

		// 如果当前行有children属性，则递归调用查找函数
		if (curRow.children) {
			getCurOutputIndex(curRow.children, row);
		}
	}
	return -1;
};

// 获取当前输出变量的行数
// !attention 目前只支持2层，即固定的outputList:[列表]
const getCurOutputRowsIndex = (index: number, row) => {
	let curIndex = index;

	// 批量 重新获取当前行的索引
	// !attention 目前只支持2层，即固定的outputList:[列表]
	if (data.mode == "BatchProcessing")
		curIndex = getCurOutputIndex(data.form.single.output, row);

	return data.opt.single.output.descRows[curIndex];
};

// 获取当前行的desc描述输入框行数
const getCurOptoutSize = (index: number, row) => {
	return getCurOutputRowsIndex(index, row) > 1
		? { minRows: 3, maxRows: 3 }
		: { minRows: 1, maxRows: 1 };
};

// 单次 输出 修改对应desc行数
const changeOutputRows = (row, rows = 3) => {
	const index = getCurOutputIndex(data.form.single.output, row);

	if (!data.opt.single.output.descRows[index])
		data.opt.single.output.descRows[index] = 1;

	data.opt.single.output.descRows[index] = rows;
};

// 单次 输出 desc行数失去焦点
const handleOutputDescBlur = (row) => {
	const index = getCurOutputIndex(data.form.single.output, row);

	if (!data.opt.single.output.descRows[index]) return;

	data.opt.single.output.descRows[index] = 1;
};

// 初始化
const init = () => {
	data.form.single.model = data.opt.single.model[0].value;

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

<style lang="less">
// !attention 即使表格中其他单元格变高也保持对齐顶部，使用全局，因action列不在此组件中
td[data-col-key="type"],
td[data-col-key="action"] {
	vertical-align: top;
}
</style>
