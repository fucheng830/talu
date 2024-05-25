<template>
	<div class="h-full flex flex-col gap-6 overflow-auto px-4 py-6 text-sm">
		<div class="flex">
			<!-- 返回 -->
			<n-button @click="changeShowAddAction">
				<Icon icon="mingcute:left-line" width="24" />
			</n-button>

			<div class="grow flex flex-col items-center gap-2 px-8 text-center">
				<span class="text-xl font-bold">添加请求</span>
				<span class="text-sm text-[#9B9B9B]">
					让您的GPT检索信息或执行对话之外的其他操作。
				</span>
				<span class="text-sm text-[#9B9B9B] cursor-pointer">学习更多</span>
			</div>

			<!-- 删除 -->
			<n-button @click="deleteAction">
				<Icon icon="mi:delete" width="18" color="#EF4444" />
			</n-button>
		</div>

		<!-- 身份 -->
		<div class="flex flex-col gap-1.5">
			<span class="font-medium">身份信息</span>

			<div
				@click="changeModalAuthShow(true)"
				class="flex rounded-lg border border-token-border-medium text-sm hover:cursor-pointer"
			>
				<div class="h-9 grow px-3 py-2">
					<span>{{ data.form.txtAuthenticationType }}</span>
				</div>
				<div class="border-l flex items-center px-3">
					<Icon icon="uil:setting" width="18" />
				</div>
			</div>
		</div>

		<!-- 方案 -->
		<div class="flex flex-col gap-1.5">
			<div class="flex justify-between items-center">
				<span class="font-medium">方案</span>
				<div class="flex gap-2">
					<template v-if="!data.isImportingFromUrl">
						<n-button @click="data.isImportingFromUrl = true"
							>从链接导入</n-button
						>

						<n-select
							value="示例"
							@update:value="handleExampleSelect"
							:options="data.opt.example"
							style="width: 120px"
						/>
					</template>

					<!-- 导入状态 -->
					<template v-else>
						<n-input
							v-model:value="data.txtImportFromUrl"
							placeholder="https://..."
						/>
						<n-button type="primary" @click="handleImportFromUrl"
							>导入</n-button
						>
						<n-button @click="data.isImportingFromUrl = false">取消</n-button>
					</template>
				</div>
			</div>

			<n-input
				v-model:value="data.form.instructions"
				type="textarea"
				:autosize="{
					minRows: 7,
					maxRows: 14,
				}"
				placeholder="请输入您的OpenAPI方案"
			/>
		</div>

		<!-- 可用请求 -->
		<div v-if="dataTable.data.length > 0" class="flex flex-col gap-1.5">
			<span class="font-medium">身份信息</span>

			<n-data-table
				size="small"
				:columns="dataTable.columns"
				:data="dataTable.data"
				:pagination="dataTable.pagination"
				:loading="dataTable.loading"
				:bordered="false"
				:paginate-single-page="false"
			/>
		</div>

		<!-- 隐私策略 -->
		<div class="flex flex-col gap-1.5">
			<div class="cursor-default">
				<n-tooltip trigger="hover">
					<template #trigger>
						<span class="font-medium">隐私策略</span>
					</template>
					<span> 所有公共GPT都需要隐私策略 </span>
				</n-tooltip>
			</div>

			<n-input
				v-model:value="data.form.policy"
				type="text"
				clearable
				placeholder="https://api.example-weather-app.com/privacy"
			/>
		</div>
	</div>

	<ModalAuth ref="refModalAuth" @saveForm="saveFormAuth" />
</template>

<script setup lang="ts">
// 用于 @/views/createai/components/AddAction.vue
import { Icon } from "@iconify/vue";
import { NButton, useDialog, useMessage } from "naive-ui";
import { h, reactive, ref, watch } from "vue";
import ModalAuth from "@/views/createai/components/ModalAuth.vue";

const dialog = useDialog();

const emits = defineEmits(["changeShowAddAction", "saveForm"]);
const props = defineProps({
	curIndex: {
		type: Number,
		default: undefined,
	},
	curAction: {
		type: Object,
		default: {},
	},
});

const msg = useMessage();

const refModalAuth = ref();
const data = reactive({
	form: {
		// 子表单，还有 ModalAuth模态框 返回的其他子参数未写进来
		authenticationType: "none", // 当前身份校验方式
		txtAuthenticationType: "无",
		apikey: {},
		oAuth: {},

		// 本页表单
		name: "", // 用于外部显示的名称
		policy: "", // 隐私策略
	},
	txtImportFromUrl: "", // 从链接导入
	showModalAuth: false,
	isImportingFromUrl: false,
	opt: {
		example: [
			{
				label: "JSON",
				value: "json",
			},
			{
				label: "YAML",
				value: "yaml",
			},
			{
				label: "空白示例",
				value: "blank",
			},
		],
	},
});

const dataTable = reactive({
	data: [
		// !DELETE 对接接口后删除
		{
			name: "名称",
			method: "GET",
			path: "/path",
		},
	],
	loading: false,
	pagination: { pageSize: 10 },
	columns: [
		{
			title: "名称",
			key: "name",
		},
		{
			title: "请求方式",
			key: "method",
		},
		{
			title: "路径",
			key: "path",
		},
		{
			title: "",
			key: "actions",
			width: 80,
			render(row) {
				return h(
					NButton,
					{
						strong: true,
						tertiary: true,
						onClick: () => testAction(row),
					},
					{ default: () => "测试" }
				);
			},
		},
	],
});

// 选择示例时
const handleExampleSelect = (val, opt) => {
	console.log("当前示例", val);
	switch (val) {
		// todo 填充对应数据 到 form.
		case "json":
			break;

		case "yaml":
			break;

		case "blank":
			break;
	}
};

// 从链接导入
const handleImportFromUrl = () => {
	console.log("handleImportFromUrl");
	// todo 处理导入链接
	data.txtImportFromUrl = "";
	data.isImportingFromUrl = false;
	// msg.success("导入成功");
};

// 测试请求
const testAction = (row) => {
	console.log("row", row);
	// todo 在页面右侧预览对话页里发送请求
};

// 删除当前请求
const deleteAction = () => {
	dialog.info({
		title: "删除请求",
		content: "是否删除当前请求?",
		positiveText: "确认",
		negativeText: "取消",
		positiveButtonProps: {
			size: "large",
		},
		negativeButtonProps: {
			size: "large",
		},
		onPositiveClick: () => {
			emits("deleteAction", props.curIndex);
			emits("changeShowAddAction");
		},
		style: {
			position: "fixed",
			top: "15%",
			left: "50%",
			transform: "translate(-50%, -50%)",
		},
	});
};

// 保存身份信息修改
const saveFormAuth = (curForm) => {
	data.form = { ...data.form.auth, ...curForm };
};

// 回到上一页
const changeShowAddAction = () => {
	emits("changeShowAddAction");
};

// 改变身份模态框显示
const changeModalAuthShow = (show: boolean = undefined) => {
	refModalAuth.value.changeModalShow(show);
};

// 实时更新当前表单
watch(
	() => data.form,
	() => {
		emits("saveForm", props.curIndex, {
			...data.form,
			// todo 替换为实际名称，或在任何位置直接改变data.form里的name
			name: `Actions-${props.curIndex}`,
		});
	},
	{ deep: true }
);

defineExpose({
	changeModalShow: changeModalAuthShow,
});
</script>

<style lang="less" scoped></style>
