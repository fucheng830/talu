<template>
	<div
		class="page-login-bg relative w-full h-full flex justify-center items-center"
	>
		<!-- 登录表单区 -->
		<div
			class="absolute w-[90%] max-w-[500px] p-8 rounded-2xl bg-[white] shadow-lg"
		>
			<div class="text-center" :style="{ color: globalColors.txtDeep }">
				<h3 class="text-[24px] font-bold pb-[8px] pb-6">欢迎来到QuChat！</h3>

				<n-tabs type="segment" v-model:value="data.curTab">
					<n-tab-pane name="weichatAccount" tab="登录">
						<n-form
							ref="refForm"
							:model="data.form_login"
							:rules="data.formRules"
							:show-label="false"
							class="text-left py-[24px]"
						>
							<n-form-item path="account">
								<n-input
									v-model:value="data.form_login.account"
									@keydown.enter.prevent="handleSubmit"
									placeholder="请输入邮箱号码"
									clearable
									size="large"
									style="border-radius: 8px"
									@blur="handleCheckRegister"
								/>
							</n-form-item>
							<n-form-item path="verify" v-if="data.opt.showVerify">
								<div class="w-full flex gap-2">
									<n-input
										v-model:value="data.form_login.verify"
										@keydown.enter.prevent="handleSubmit"
										placeholder="请输入验证码"
										clearable
										size="large"
										style="border-radius: 8px"
									/>
									<n-button
										type="primary"
										size="large"
										@click="handleSendVerify"
										:disabled="data.opt.btnSendVerifyDisabled"
										style="border-radius: 8px; min-width: 110px; padding: auto"
									>
										{{ data.opt.btnVerifyTxt }}
									</n-button>
								</div>
							</n-form-item>
							<n-form-item path="pwd">
								<n-input
									v-model:value="data.form_login.pwd"
									type="password"
									@keydown.enter.prevent="handleSubmit"
									placeholder="请输入登录密码"
									show-password-on="click"
									clearable
									size="large"
									style="border-radius: 8px"
								/>
							</n-form-item>
							<n-button
								type="primary"
								block
								size="large"
								@click="handleSubmit"
								style="border-radius: 8px"
							>
								{{ data.opt.btnSubmitTxt }}
							</n-button>
						</n-form>

						<p :style="{ color: globalColors.txtDeep }">
							登录即同意
							<n-button text :color="globalColors.btnActive">
								《Quchat 服务协议》
							</n-button>
						</p>

						<p
							class="mt-[20px] cursor-pointer text-center"
							:style="{ color: globalColors.btnActive }"
						>
							忘记密码？
						</p>

						<div class="flex items-center justify-center mt-[20px]">
							<div class="w-1/4 h-[1px] bg-gray-300 mr-2"></div>
							<p class="text-center" :style="{ color: globalColors.txtDeep }">
								第三方登录
							</p>
							<div class="w-1/4 h-[1px] bg-gray-300 ml-2"></div>
						</div>

						<div class="flex justify-center gap-4 mt-[20px] p-2">
							<div class="bg-green-500 p-3 rounded-full">
								<Icon icon="cib:wechat" style="color: white" width="30" />
							</div>
						</div>
					</n-tab-pane>

					<!-- 注册表单 -->
					<n-tab-pane name="registerMail" tab="注册">
						<n-form
							ref="refFormMail"
							:model="data.form_register"
							:rules="data.formRules"
							:show-label="false"
							class="text-left py-[24px]"
						>
							<n-form-item path="mail">
								<n-input
									v-model:value="data.form_register.account"
									@keydown.enter.prevent
									@blur="handleCheckRegisterForRegister"
									placeholder="邮箱"
									clearable
									size="large"
									style="border-radius: 8px"
								/>
							</n-form-item>
							<n-form-item path="code">
								<div class="w-full flex gap-2">
									<n-input
										v-model:value="data.form_register.txtCode"
										@keydown.enter.prevent
										placeholder="验证码"
										clearable
										size="large"
										style="border-radius: 8px"
									/>
									<n-button
										:disabled="data.opt.btnSendVerifyDisabled"
										type="primary"
										size="large"
										@click="sendMailCodeClick"
										style="border-radius: 8px; min-width: 110px; padding: auto"
									>
										{{ data.form_register.btnTxtMail }}
									</n-button>
								</div>
							</n-form-item>
							<n-form-item path="pwd">
								<n-input
									v-model:value="data.form_register.txtPwd"
									type="password"
									@keydown.enter.prevent
									placeholder="密码"
									clearable
									size="large"
									style="border-radius: 8px"
									show-password-on="click"
								/>
							</n-form-item>
							<n-form-item path="pwdComfirm">
								<n-input
									v-model:value="data.form_register.txtPwdComfirm"
									type="password"
									@keydown.enter.prevent
									placeholder="确认密码"
									clearable
									size="large"
									style="border-radius: 8px"
									show-password-on="click"
								/>
							</n-form-item>
							<n-form-item path="invite">
								<n-input
									v-model:value="data.form_register.referee"
									@keydown.enter.prevent
									:readonly="data.flagReadonlyInvite"
									placeholder="邀请码，没有可不填"
									clearable
									size="large"
									style="border-radius: 8px"
								/>
							</n-form-item>
							<n-form-item>
								<n-button
									type="primary"
									block
									size="large"
									@click="handleRegister"
									style="border-radius: 8px"
								>
									注册
								</n-button>
							</n-form-item>
						</n-form>
					</n-tab-pane>
				</n-tabs>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, nextTick, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import { FormItemRule, useMessage } from "naive-ui";
import { api } from "@/api/common";
import { useAppStore, useUserStore } from "@/store";
import { onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const msg = useMessage();
const userStore = useUserStore();
const appStore = useAppStore();
const route = useRoute();
const router = useRouter();

const refForm = ref();
const refFormMail = ref();

const data = reactive({
	curTab: "weichatAccount",
	// 手机或邮箱 正则
	regEmail: /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
	// "(^13[0-9]{9}$|14[0-9]{9}|15[0-9]{9}$|18[0-9]{9}$)|(^0(10|2[0-5789]|\\d{3})\\d{7,8}$)",
	// 手机和邮箱
	// /^(1[3456789]\d{9})$|^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
	form_login: {
		account: "",
		verify: "",
		pwd: "",
	},
	form_register: {
		account: "",
		txtPwd: "",
		txtPwdComfirm: "",
		txtCode: "",
		btnTxtMail: "发送验证码",
		referee: "",
		flagDisabledBtnMail: false,
	},
	opt: {
		isShowModal: computed(() => appStore.showLoginModal),
		showVerify: false, // 表单是否显示 验证码
		btnVerifyTxt: "获取验证码", // 验证码按钮 文本
		btnSendVerifyDisabled: true, // 禁用 发送验证码按钮
		btnSubmitTxt: "登录",
	},
	formRules: {
		account: [
			{
				key: "account",
				required: true,
				validator(rule: FormItemRule, value: string) {
					if (!value) {
						return new Error("请输入邮箱号码");
					} else if (!data.regEmail.test(value)) {
						return new Error("请输入正确的邮箱号码");
					}
					return true;
				},
				trigger: ["blur"],
			},
		],
		verify: [
			{
				key: "verify",
				validator(rule: FormItemRule, value: string) {
					if (!value) {
						return new Error("请输入验证码");
					}
					return true;
				},
				trigger: ["blur"],
			},
		],
		pwd: [
			{
				key: "pwd",
				required: true,
				validator(rule: FormItemRule, value: string) {
					if (!value) {
						return new Error("请输入密码");
					} else if (value.length < 8 || value.length > 16) {
						return new Error("密码在8-16位之间");
					}
					return true;
				},
				trigger: ["blur"],
			},
		],
	},
});

// 专门用于注册表单的邮箱验证方法
const handleCheckRegisterForRegister = () => {
	if (data.regEmail && !data.regEmail.test(data.form_register.account)) {
		msg.error("请输入正确的邮箱格式");
		return;
	}

	api
		.check_mail({
			email: data.form_register.account,
		})
		.then((res) => {
			msg.success("邮箱可用");
			data.opt.btnSendVerifyDisabled = false;
		})
		.catch((err) => {
			msg.error(err.message);
			data.opt.btnSendVerifyDisabled = true;
		});
};

// 登录/注册 按钮
const handleSubmit = () => {
	// 根据是否显示验证码来判断是登录还是注册
	if (!data.opt.showVerify) {
		// 登录
		refForm.value.validate().then(() => {
			handleLogin();
		});
	}
};

// 发送验证码
const sendMailCodeClick = () => {
	if (data.opt.btnSendVerifyDisabled) return;

	data.opt.btnVerifyTxt = 10; // 倒计时 最大值
	data.opt.btnSendVerifyDisabled = true; // 禁用 发送按钮

	// 发送验证码
	api
		.send_code({
			email: data.form_register.account, // 修改为正确的引用
		})
		.then((res) => {
			if (res.status != "Success") return msg.error(res.message);

			msg.success(res.message);
		});

	// 开始倒计时
	const timer = setInterval(() => {
		if (data.opt.btnVerifyTxt <= 1) {
			clearInterval(timer);
			data.opt.btnVerifyTxt = "重新发送";
			data.opt.btnSendVerifyDisabled = false; // 取消禁用 发送按钮
			return;
		}
		// 倒计时 减少
		data.opt.btnVerifyTxt = data.opt.btnVerifyTxt -= 1;
	}, 1000);
};

// 注册
const handleRegister = () => {
	// 移除 return; 语句
	api
		.apiUserRegister({
			email: data.form_register.account, // 修改为正确的引用
			emailCode: data.form_register.txtCode, // 修改为正确的引用
			password: data.form_register.txtPwd, // 修改为正确的引用
			referee: data.form_register.referee, // 修改为正确的引用
		})
		.then((res) => {
			if (res.status != "Success") return msg.error(res.message);

			userStore.updateUserInfo(res.data);
			msg.success(res.message);
		});
};

// 登录按钮
const handleLogin = () => {
	api
		.login({
			email: data.form_login.account,
			password: data.form_login.pwd,
		})
		.then((res) => {
			if (res?.status != "Success") return msg.error(res.message);
			userStore.updateUserInfo(res.data);
			msg.success(res.message);
			router.replace("/");
		})
		.catch((error) => {
			msg.error(error.message);
		});
};

const init = () => {
	if (!route.params.referee) return;
	// url携带邀请码时

	// 读取邀请码
	data.form_register.referee = route.params.referee;

	// 切换tab到注册表单
	data.curTab = "registerMail";
};

// 监听用户登录状态，改变模态框显示
onMounted(() => {
	init();
});
</script>

<style lang="less" scoped>
.page-login-bg {
	background-image: url("@/assets/images/login/bg_login.jpg");
	background-size: 100% 100%;
	background-repeat: no-repeat;
}
</style>
