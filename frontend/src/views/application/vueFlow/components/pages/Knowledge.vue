<template>
	<div class="flex flex-col gap-2 p-4">
		<!-- 输入 -->
		<SingleModule :hideBtn="true">
			<span class="ml-2 flex items-center">
				查询<span class="text-[red]">*</span>
			</span>

			<!-- 值 -->
			<div class="flex items-center">
				<n-input-group>
					<!-- 类型 -->
					<n-select
						v-model:value="data.form.input.type"
						:options="data.opt.input.type"
					/>

					<!-- 引用 值 -->
					<template v-if="data.form.input.type === 'Reference'">
						<!-- !todo loading值放 data.form.varList的话，如果要监测form变化后执行方法，可能会陷入死循环，可能需要单独用一个数组储存各变量的loading，现暂用options个数判断 -->
						<n-select
							v-model:value="data.form.input.valReference"
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
						<n-input
							v-model:value="data.form.input.valInput"
							placeholder="请输入值"
						/>
					</template>
				</n-input-group>

				<n-button text @click.stop="deleteVar(index)" style="padding: 0 0.8em">
					<Icon icon="nimbus:stop" width="14" />
				</n-button>
			</div>
		</SingleModule>

		<!-- 知识库 -->
		<SingleModule :useGrid="false" title="知识库" @add="addKnowledge">
			<div class="flex flex-col gap-2">
				<template v-for="(item, index) in data.form.knowledge.list" :key="item">
					<div class="flex items-center gap-2 px-1">
						<n-select
							v-model:value="data.form.knowledge.list[index]"
							:options="data.opt.knowledge.list[index]"
						/>

						<n-button
							text
							style="padding: 0.4rem"
							@click.stop="deleteKnowledge(index)"
						>
							<Icon
								icon="nimbus:stop"
								width="18"
								:color="theme.primaryColor"
							/>
						</n-button>
					</div>
				</template>
			</div>

			<!-- 其他配置 -->
			<div class="grid grid-cols-[40%_1fr] gap-2 mt-4 px-6">
				<!-- 搜索策略 -->
				<div class="flex items-center">
					<span> 搜索策略 </span>
					<IconTip>
						从知识库中获取知识的检索方法，不同的检索策略可以更有效地找到正确的信息，从而提高生成答案的准确性和可用性。
					</IconTip>
				</div>
				<n-select
					v-model:value="data.form.knowledge.searchStrategy"
					:options="data.opt.knowledge.searchStrategy"
				/>

				<!-- 最大回调次数 -->
				<!-- todo 无法取消拖拽 -->
				<div class="flex items-center">
					<span> 最大回调次数 </span>
					<IconTip>
						根据知识返回到模型的最大段落数。数字越大，返回的内容越多。
					</IconTip>
				</div>
				<n-slider
					v-model:value="data.form.knowledge.maxRecalls"
					:step="1"
					:min="1"
					:max="10"
					:marks="{ 1: '1', 3: '默认', 10: '10' }"
				/>

				<!-- 最小匹配度 -->
				<div class="flex items-center">
					<span> 最小匹配度 </span>
					<IconTip>
						根据设置的匹配度选择段落并返回到模型中。匹配度低于设置的内容将不会被调用。
					</IconTip>
				</div>
				<n-slider
					v-model:value="data.form.knowledge.minMatchDegree"
					:step="0.01"
					:min="0.01"
					:max="0.99"
					:marks="{ 0.01: '0.01', 0.5: '默认', 0.99: '0.99' }"
				/>
			</div>
		</SingleModule>

		<!-- 输出 -->
		<SingleModule :useGrid="false" title="输出" :hideBtn="true">
			<OutputTree :data="data.form.output" />
		</SingleModule>
	</div>

	<!-- 左侧输入 -->
	<MyHandle type="source" color="#36ADEF" />
	<!-- 右侧输出 -->
	<MyHandle type="target" color="#36ADEF" />
</template>

<script setup lang="ts">
import { computed, h, nextTick, onMounted, reactive, watch } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { Icon } from "@iconify/vue";
import { useKnowledgeStore } from "@/store";
import IconTip from "@/components/common/IconTip/index.vue";
import OutputTree from "@/views/application/vueFlow/components/pages/components/OutputTree.vue";
import { useVueFlow } from "@vue-flow/core";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const konwledgeStore = useKnowledgeStore();
const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	form: {
		input: {
			type: "Reference",
			valReference: undefined, // 引用 输入值
			valInput: "", // 输入 输入值
		},
		knowledge: {
			list: [""], // 知识库引用
			searchStrategy: "Semantic", // 搜索策略
			maxRecalls: 3, // 最大回调次数
			minMatchDegree: 0.5, // 最小匹配度
		},
		output: [
			{
				label: "OutputList",
				key: "OutputList",
				tag: "Array<Object>",
				children: [
					{
						label: "Output",
						key: "Output",
						tag: "String",
					},
				],
			},
		],
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
		knowledge: {
			// 每个知识库下拉框的选项，默认第一个全可选
			list: [
				konwledgeStore.listKnowledge.map((item) => ({
					label: item.name,
					value: item.uuid,
					disabled: false,
				})),
			],
			searchStrategy: [
				{
					label: "语义搜索",
					value: "Semantic",
				},
				{
					label: "混合搜索",
					value: "Hybrid",
				},
				{
					label: "全文搜索",
					value: "Full-Text",
				},
			],
		},
	},
});

// 添加知识库
const addKnowledge = () => {
	data.form.knowledge.list.push("");
};

// 移除当前知识库
const deleteKnowledge = (index: number) => {
	data.form.knowledge.list.splice(index, 1);
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

// 实时更新知识库各个下拉框可选状态
watch(
	() => data.form.knowledge.list,
	(val) => {
		// 循环当前已选知识库
		val.forEach((item, index) => {
			// 若没有该选项组，则创建空数组
			if (!data.opt.knowledge.list[index]) data.opt.knowledge.list[index] = [];

			// 循环所有知识库，处理数据结构
			data.opt.knowledge.list[index] = konwledgeStore.listKnowledge.map(
				(cur) => ({
					label: cur.name,
					value: cur.uuid,
					// 是否禁用
					disabled:
						// 非当前选中
						cur.uuid !== item &&
						// 查出是否已选
						val.filter((curItem) => curItem != "").includes(cur.uuid),
				})
			);
		});
	},
	{ deep: true }
);

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
