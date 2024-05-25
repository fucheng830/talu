<template>
	<!-- 内容区 -->
	<div class="flex flex-col gap-2 p-4">
		<n-tabs type="segment" animated>
			<!-- 将变量传给AI -->
			<n-tab-pane name="set" tab="将变量传给AI">
				<div class="flex flex-col gap-4">
					<SingleModule firstText="字段名" :hideBtn="true">
						<n-input
							v-model:value="data.form.set.input.field"
							type="text"
							placeholder="名称"
						/>

						<!-- 值 -->
						<div class="flex items-center">
							<n-input-group>
								<!-- 类型 -->
								<n-select
									v-model:value="data.form.set.input.type"
									:options="data.opt.input.type"
								/>

								<!-- 引用 值 -->
								<template v-if="data.form.set.input.type === 'Reference'">
									<!-- !todo loading值放 data.form.set.varList的话，如果要监测form变化后执行方法，可能会陷入死循环，可能需要单独用一个数组储存各变量的loading，现暂用options个数判断 -->
									<n-select
										v-model:value="data.form.set.input.valReference"
										filterable
										placeholder="引用"
										:options="data.opt.input.reference"
										:loading="data.opt.input.isLoadingReference"
										clearable
										remote
										@search="handleReferenceSearch"
									/>
								</template>

								<!-- input 值 -->
								<template v-else>
									<n-input
										v-model:value="data.form.set.input.valInput"
										placeholder="请输入值"
									/>
								</template>
							</n-input-group>

							<!-- <n-button
							text
							@click.stop="deleteVar(index)"
							style="padding: 0 0.8em"
						>
							<Icon icon="nimbus:stop" width="14" />
						</n-button> -->
						</div>
					</SingleModule>

					<SingleModule :useGrid="false" title="输出" :hideBtn="true">
						<OutputTree :data="data.form.set.output" />
					</SingleModule>
				</div>
			</n-tab-pane>

			<!-- 从AI获取变量 -->
			<n-tab-pane name="get" tab="从AI获取变量" size="small">
				<div class="flex flex-col gap-4">
					<SingleModule :useGrid="false" :hideBtn="true">
						<div class="grid grid-cols-2 gap-2">
							<span class="text-[#1c1d2359] pl-2">变量名</span>
							<span class="text-[#1c1d2359] pl-2">值</span>

							<div class="ml-2 flex items-center">
								Key<span class="text-[red]">*</span>
							</div>

							<n-input
								v-model:value="data.form.get.input.value"
								placeholder="请输入值"
								size="small"
							/>
						</div>
					</SingleModule>

					<SingleModule title="输出" :useGrid="false" :hideBtn="true">
						<div class="grid grid-cols-2 gap-2">
							<span class="text-[#1c1d2359] pl-2">变量名</span>
							<span class="text-[#1c1d2359] pl-2">类型</span>

							<n-input
								v-model:value="data.form.get.output.name"
								placeholder="请输入值"
								size="small"
							/>

							<div class="ml-2 flex items-center">
								String<span class="text-[red]">*</span>
							</div>
						</div>
					</SingleModule>
				</div>
			</n-tab-pane>
		</n-tabs>
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
import { globalColors } from "@/hooks/useTheme";
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import OutputTree from "@/views/application/vueFlow/components/pages/components/OutputTree.vue";
import { useVueFlow } from "@vue-flow/core";

const { updateNodeData } = useVueFlow();

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	form: {
		set: {
			input: {
				field: "",
				type: "Reference",
				valReference: undefined, // 引用 输入值
				valInput: "", // 输入 输入值
			},
			output: [
				{
					label: "isSuccess",
					key: "isSuccess",
					tag: "Boolean",
				},
			],
		},
		get: {
			input: {
				value: "",
			},
			output: {
				name: "",
			},
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
			reference: [],
			isLoadingReference: false,
		},
	},
});

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
