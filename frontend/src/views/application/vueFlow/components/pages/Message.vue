<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<SingleModule title="输出变量" @add="handleAddVar">
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

		<SingleModule title="回答内容" :useGrid="false">
			<template #extra>
				<div class="flex items-center gap-4 mr-2" @click.stop>
					<div class="flex items-center gap-1 font-bold">
						流式输出
						<IconTip width="18" color="#a7a9b0">
							<span
								v-text="
									`编辑智能体的回复内容，即在工作流运行过程中，智能体会直接用此处编辑的原始内容回复对话。你可以使用 {{变量名}} 
							来引用输出变量中的变量。`
								"
							></span>
						</IconTip>
					</div>

					<n-switch v-model:value="data.form.answer.isStream" />
				</div>
			</template>

			<n-input
				v-model:value="data.form.answer.value"
				type="textarea"
				:autosize="{
					minRows: 4,
					maxRows: 7,
				}"
				:placeholder="`您可以使用 {{变量名}}、{{变量.子变量名}}、{{变量[对应数组下标]}} 来引用输入参数中的变量。`"
			/>
		</SingleModule>
	</div>

	<!-- 左侧输入 -->
	<MyHandle type="target" color="#36ADEF" />
	<!-- 右侧输出 -->
	<MyHandle type="source" color="#36ADEF" />
</template>

<script setup lang="ts">
import { nextTick, onMounted, reactive, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import { Icon } from "@iconify/vue";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
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
		input: [
			{
				name: "",
				type: "Reference",
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
		],
		answer: {
			value: "",
			isStream: false,
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
