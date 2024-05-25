<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<!-- 输入 -->
		<SingleModule @add="handleAddVar">
			<template v-for="(curVar, index) in data.form.input" :key="index">
				<!-- 名称 -->
				<n-input
					v-model:value="curVar.name"
					size="small"
					placeholder="请输入名称"
				/>

				<!-- 值 -->
				<div class="flex items-center">
					<n-input-group>
						<!-- 类型 -->
						<n-select
							v-model:value="curVar.type"
							:options="data.opt.input.type"
						/>

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
						@click.stop="deleteVar(index)"
						style="padding: 0 0.8em"
					>
						<Icon icon="nimbus:stop" width="14" />
					</n-button>
				</div>
			</template>
		</SingleModule>

		<!-- SQL -->
		<SingleModule title="SQL" :useGrid="false">
			<template #extra>
				<n-button
					quaternary
					:color="globalColors.btnActive"
					@click.stop="generateSQL"
				>
					<div class="flex items-center gap-1">
						<Icon icon="mdi:refresh-auto" />
						<span>自动生成</span>
					</div>
				</n-button>
			</template>

			<n-input
				v-model:value="data.form.sql.value"
				type="textarea"
				:autosize="{
					minRows: 4,
					maxRows: 7,
				}"
				:placeholder="`您可以使用 {{变量名}}、{{变量.子变量名}}、{{变量[对应数组下标]}} 来引用输入参数中的变量。`"
			/>
		</SingleModule>

		<SingleModule title="输出" :useGrid="false" :hideBtn="true">
			<n-data-table
				:columns="data.opt.output.columns"
				:data="data.form.output.data"
				:row-key="(row) => row.name"
				default-expand-all
				size="small"
			/>
		</SingleModule>
	</div>

	<ModalGenerateSQL ref="refModalGenerateSQL" @saveForm="handleGetSQL" />

	<!-- 左侧输入 -->
	<MyHandle type="target" color="#36ADEF" />
	<!-- 右侧输出 -->
	<MyHandle type="source" color="#36ADEF" />
</template>

<script setup lang="ts">
import { h, nextTick, onMounted, reactive, ref, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { NInput, NSelect } from "naive-ui";
import CodeAction from "@/views/application/vueFlow/components/pages/components/code/Action.vue";
import ModalGenerateSQL from "@/views/application/vueFlow/components/pages/components/database/ModalGenerateSQL.vue";
import { useVueFlow } from "@vue-flow/core";

const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const refModalGenerateSQL = ref();
const data = reactive({
	form: {
		input: [
			{
				name: "",
				type: "Reference",
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
		],
		sql: {
			value: "",
		},
		output: {
			// 有children就有添加子元素按钮
			data: [
				{
					name: "outputList",
					type: "Array<Object>",
					disabled: true,
					children: [
						{
							name: "",
							type: "String",
						},
					],
				},
				{
					name: "rowNum",
					type: "Integer",
					disabled: true,
				},
			],
		},
	},
	opt: {
		isInited: false,
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
		output: {
			columns: [
				{
					title: "名称",
					key: "name",
					width: 180,
					className: "flex items-center",
					render: (row) =>
						h(NInput, {
							defaultValue: row.name,
							placeholder: "名称",
							disabled: row.disabled,
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
							disabled: row.disabled,
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
							btnDisabled: row.disabled,
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
		type: "Reference",
		valReference: undefined, // 引用 输入值
		valInput: "", // 输入 输入值
	});
};

// 删除变量
const deleteVar = (index: number) => {
	data.form.input.splice(index, 1);
};

// 自动生成SQL
const generateSQL = () => {
	changeModalShow();
};

// 获取SQL
const handleGetSQL = (res) => {
	console.log(res);
	data.form.sql.value = res.sql;
};

// 切换自动生成SQL模态框显示
const changeModalShow = () => {
	refModalGenerateSQL.value.changeModalShow();
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
