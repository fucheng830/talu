<template>
	<mModal
		ref="refModal"
		title="自动生成"
		footerBtnSize="medium"
		footerComfirmBtnType="primary"
		txtCancel="关闭"
		txtConfirm="完成"
		:comfirmDisabled="
			data.form.agent === undefined ||
			data.form.queryTarget === '' ||
			data.form.sql === ''
		"
		@onShowChange="onShowChange"
		@onPositiveClick="handleComfirm"
		style="
			width: 90%;
			max-width: 500px;
			position: fixed;
			top: 10%;
			left: 50%;
			transform: translate(-50%, 0);
		"
	>
		<div class="flex flex-col gap-6 pt-4">
			<!-- 选择数据库 -->
			<div>
				<span class="font-bold">选择包含所需数据库的Agent</span>

				<div class="mt-2">
					<n-select
						v-model:value="data.form.agent"
						filterable
						placeholder="请选择一个Agent"
						:options="data.opt.agent"
						:loading="data.opt.isSearchingAgent"
						clearable
						remote
						@search="handleReferenceSearch"
					/>
				</div>
			</div>

			<!-- 查询目标 -->
			<div>
				<span class="font-bold">查询目标</span>

				<div class="mt-2">
					<n-input
						v-model:value="data.form.queryTarget"
						type="textarea"
						:autosize="{
							minRows: 4,
							maxRows: 7,
						}"
						:placeholder="`通过自然语言描述查询目标`"
					/>
				</div>
			</div>

			<!-- SQL -->
			<div>
				<div class="flex justify-between">
					<span class="font-bold">SQL</span>

					<!-- 右侧按钮 -->
					<n-button
						quaternary
						:color="theme.primaryColor"
						:loading="data.opt.isSearchingSQL"
						:disabled="
							data.form.agent === undefined || data.form.queryTarget === ''
						"
						@click.stop="generateSQL"
					>
						<div class="flex items-center gap-1">
							<Icon icon="mdi:refresh-auto" />
							<span>自动生成</span>
						</div>
					</n-button>
				</div>

				<div class="mt-2">
					<n-input
						v-model:value="data.form.sql"
						type="textarea"
						:autosize="{
							minRows: 4,
							maxRows: 7,
						}"
						placeholder=""
						:readonly="true"
						style="background-color: #f8f8f8"
					/>
				</div>
			</div>
		</div>
	</mModal>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useChatStore } from "@/store";
import mModal from "@/components/common/mModal/index.vue";
import logo from "@/assets/logo.png";
import { Icon } from "@iconify/vue";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();

const chatStore = useChatStore();

const emits = defineEmits(["saveForm"]);

const refModal = ref();
const data = reactive({
	form: {
		agent: undefined,
		queryTarget: "",
		sql: "",
	},
	formBackup: {}, // 表单备份，用于重置
	opt: {
		// todo 替换为个人创建的agent列表
		agent: computed(() =>
			chatStore.agentList.map((item) => ({ label: item.name, value: item.id }))
		),
		isSearchingAgent: false,
		isSearchingSQL: false,
	},
});

// 自动生成SQL
const generateSQL = () => {
	data.opt.isSearchingSQL = true;
	// todo 对接生成接口
	// !temp 临时代码，后续替换为接口
	setTimeout(() => {
		data.form.sql = "res sql";
		data.opt.isSearchingSQL = false;
	}, 2000);
};

// 确认
const handleComfirm = () => {
	emits("saveForm", data.form);
	changeModalShow();
};

// 重置表单
const resetForm = () => {
	// data.form = { ...data.form, ...data.formBackup };
	data.form = data.formBackup;
};

// 改变模态框显示
const changeModalShow = () => {
	refModal.value.toggleModal();
};

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return resetForm();

	// 备份表单，用于重置
	data.formBackup = JSON.parse(JSON.stringify(data.form));
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
