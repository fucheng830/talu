<template>
	<mModal
		ref="refModal"
		title="身份验证"
		footerBtnSize="medium"
		footerComfirmBtnType="primary"
		txtCancel="取消"
		txtConfirm="保存"
		@onShowChange="onShowChange"
		@onPositiveClick="handleComfirm"
		style="position: fixed; top: 10%; left: 50%; transform: translate(-50%, 0)"
	>
		<div class="max-h-[70vh] overflow-y-auto">
			<div class="mb-4">
				<p class="mb-1">身份验证方式</p>
				<n-radio-group
					v-model:value="data.form.authenticationType"
					name="authenticationType"
				>
					<n-space>
						<n-radio
							v-for="item in data.opt.authenticationType"
							:key="item.value"
							:value="item.value"
						>
							{{ item.label }}
						</n-radio>
					</n-space>
				</n-radio-group>
			</div>

			<!-- 方式 apiKey -->
			<template v-if="data.form.authenticationType == 'apiKey'">
				<div class="mb-4">
					<p class="mb-1">API Key</p>
					<n-input
						v-model:value="data.form.apikey.apiKey"
						type="text"
						placeholder="[HIDDEN]"
					/>
				</div>

				<div>
					<p class="mb-1">身份类型</p>
					<n-radio-group
						v-model:value="data.form.apikey.authType"
						name="authType"
					>
						<n-space>
							<n-radio
								v-for="item in data.opt.authType"
								:key="item.value"
								:value="item.value"
							>
								{{ item.label }}
							</n-radio>
						</n-space>
					</n-radio-group>
				</div>
			</template>

			<!-- 方式 oAuth -->
			<template v-if="data.form.authenticationType == 'oAuth'">
				<div class="mb-4">
					<p class="mb-1">ID</p>
					<n-input
						v-model:value="data.form.oAuth.id"
						type="text"
						placeholder="<HIDDEN>"
					/>
				</div>

				<div class="mb-4">
					<p class="mb-1">私钥</p>
					<n-input
						v-model:value="data.form.oAuth.secret"
						type="text"
						placeholder="<HIDDEN>"
					/>
				</div>

				<div class="mb-4">
					<p class="mb-1">授权地址</p>
					<n-input
						v-model:value="data.form.oAuth.authorizationURL"
						type="text"
						placeholder=""
					/>
				</div>

				<div class="mb-4">
					<p class="mb-1">token地址</p>
					<n-input
						v-model:value="data.form.oAuth.tokenURL"
						type="text"
						placeholder=""
					/>
				</div>

				<div class="mb-4">
					<p class="mb-1">域名</p>
					<n-input
						v-model:value="data.form.oAuth.scope"
						type="text"
						placeholder=""
					/>
				</div>

				<div>
					<p class="mb-1">token传输方式</p>
					<n-radio-group
						v-model:value="data.form.oAuth.tokenExchangeMethod"
						name="tokenExchangeMethod"
					>
						<n-space vertical>
							<n-radio
								v-for="item in data.opt.tokenExchangeMethod"
								:key="item.value"
								:value="item.value"
							>
								{{ item.label }}
							</n-radio>
						</n-space>
					</n-radio-group>
				</div>
			</template>
		</div>
	</mModal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { computed, reactive, ref } from "vue";

const emits = defineEmits(["saveForm"]);

const refModal = ref();
const data = reactive({
	form: {
		authenticationType: "none",
		txtAuthenticationType: computed(
			() =>
				data.opt.authenticationType.find(
					(item) => item.value == data.form.authenticationType
				)?.label
		),
		apikey: {
			apiKey: "", // API Key
			authType: "basic", // 身份类型
		},
		oAuth: {
			id: "",
			secret: "",
			authorizationURL: "",
			tokenURL: "",
			scope: "",
			tokenExchangeMethod: "default",
		},
	},
	formBackup: {}, // 表单备份，用于重置
	opt: {
		authenticationType: [
			{
				label: "无",
				value: "none",
			},
			{
				label: "API Key",
				value: "apiKey",
			},
			{
				label: "oAuth",
				value: "oAuth",
			},
		],
		authType: [
			{
				label: "Basic",
				value: "basic",
			},
			{
				label: "Bearer",
				value: "bearer",
			},
			{
				label: "Custom",
				value: "custom",
			},
		],
		tokenExchangeMethod: [
			{
				label: "默认（POST请求）",
				value: "default",
			},
			{
				label: "基础身份请求头",
				value: "basic",
			},
		],
	},
});

// 确认
const handleComfirm = () => {
	console.log("commit", data.form);
	// todo 提交配置更改
	emits("saveForm", data.form);
};

// 重置表单
const resetForm = () => {
	data.form = { ...data.form, ...data.formBackup };
};

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return resetForm();

	// 备份表单，用于重置
	data.formBackup = JSON.parse(JSON.stringify(data.form));
};

// 改变模态框显示
const changeModalShow = (show: boolean = undefined) => {
	refModal.value.toggleModal(show);
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
