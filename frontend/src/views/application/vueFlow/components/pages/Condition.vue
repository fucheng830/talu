<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<div class="relative">
			<SingleModule title="If" :useGrid="false" @add="handleAdd">
				<div class="grid grid-cols-[15%_20%_20%_1fr_3rem] gap-y-2 gap-x-2">
					<span></span>
					<span class="text-[#1c1d2359] pl-2">变量</span>
					<span class="text-[#1c1d2359] pl-2">条件</span>
					<span class="text-[#1c1d2359] pl-2">对照</span>
					<span></span>

					<template
						v-for="(item, index) in data.form.conditoinList"
						:key="index"
					>
						<!-- 连接方式 -->
						<span v-if="index == 0" class="ml-[10%] text-[#1d1c2399]">
							条件
						</span>
						<n-select
							v-else
							v-model:value="item.ifType"
							:options="data.opt.ifType"
						/>

						<!-- 变量 -->
						<n-select
							v-model:value="item.variable"
							:options="data.opt.variable"
							filterable
							placeholder="变量"
						/>

						<!-- 条件 -->
						<n-select
							v-model:value="item.condition"
							:options="data.opt.condition"
							filterable
							placeholder="条件"
						/>

						<!-- 对照 -->
						<n-input-group>
							<!-- 类型 -->
							<n-select
								v-model:value="item.comparisonType"
								:options="data.opt.comparisonType"
								style="width: 200px"
							/>

							<!-- 引用 值 -->
							<template v-if="item.comparisonType === 'Reference'">
								<!-- !todo loading值放 data.form.varList的话，如果要监测form变化后执行方法，可能会陷入死循环，可能需要单独用一个数组储存各变量的loading，现暂用options个数判断 -->
								<n-select
									v-model:value="item.valReference"
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
								<n-input v-model:value="item.valInput" placeholder="请输入值" />
							</template>
						</n-input-group>

						<span v-if="index == 0"></span>
						<n-button v-else text @click.stop="deleteCondition(index)">
							<Icon icon="nimbus:stop" width="18" />
						</n-button>
					</template>
				</div>
			</SingleModule>

			<!-- 左侧输入 -->
			<MyHandle
				type="target"
				color="#36ADEF"
				style="transform: translateX(-1.5rem)"
			/>
			<!-- 右侧输出 -->
			<MyHandle type="source" color="#36ADEF" />
		</div>

		<div class="relative bg-[#F7F7F7] rounded-lg p-4">
			<span>Else</span>

			<!-- 右侧输出 -->
			<MyHandle type="source" color="#36ADEF" />
		</div>
	</div>
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
		conditoinList: [
			{
				ifType: undefined,
				variable: undefined, // 变量
				condition: undefined, // 条件
				comparisonType: "Reference", // 对照类型
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
		],
	},
	opt: {
		isInited: false,
		ifType: [
			{
				label: "并且",
				value: "AND",
			},
			{
				label: "或",
				value: "OR",
			},
		],
		variable: [], // 变量
		condition: [], // 条件
		// 对照类型
		comparisonType: [
			{
				label: "引用",
				value: "Reference",
			},
			{
				label: "输入",
				value: "Input",
			},
		],
		reference: [],
	},
});

// 添加条件
const handleAdd = () => {
	data.form.conditoinList.push({
		ifType: data.form.conditoinList?.length > 0 ? "AND" : undefined,
		variable: undefined, // 变量
		condition: undefined, // 条件
		comparisonType: "Reference", // 对照类型
		valReference: undefined, // 引用 输入值
		valInput: "", // 输入 输入值
	});
};

// 删除条件
const deleteCondition = (index: number) => {
	data.form.conditoinList.splice(index, 1);
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
