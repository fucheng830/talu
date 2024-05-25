<template>
	<mModal
		ref="refLogin"
		:show-footer="false"
		:closable="false"
		@onClose="handleModalLoginClose"
	>
		<div class="flex justify-end">
			<!-- 关闭 按钮 -->
			<Icon
				icon="simple-line-icons:close"
				width="22"
				color="#4D5052"
				@click="handleModalLoginClose"
			/>
		</div>
		<div
			id="hidden-element"
			tabindex="-1"
			style="position: absolute; left: -9999px"
		></div>
		<div class="text-center" :style="{ color: globalColors.txtDeep }">
			<h3 class="text-[24px] font-bold pb-3">
				{{ $t("common.welcome") }}
			</h3>
			<div class="modal-top" tabindex="-1">
				<input
					type="text"
					id="hidden-input"
					style="position: absolute; opacity: 0; pointer-events: none"
				/>
			</div>

			<n-tabs type="segment">
				<n-tab-pane name="weichatAccount" :tab="$t('common.login')">
					<!-- 二维码部分 -->
					<div v-if="data.showQRCode" class="qr-code-container">
						<div class="modal-mask"></div>
						<!-- 半透明遮罩层 -->
						<div class="qr-code-box">
							<h2>{{ $t("login.wechat") }}</h2>
							<img :src="data.qrCodeUrl" alt="WeChat QR Code" />
							<!-- 二维码图片 -->
							<n-button @click="closeQRCode">{{
								$t("login.backLoginEmail")
							}}</n-button>
						</div>
					</div>

					<!-- 邮箱登录表单 -->
					<div v-else>
						<n-form
							ref="refForm"
							:model="data.form_login"
							:rules="data.formRules"
							:show-label="false"
							class="text-left py-[24px]"
							:autofocus="false"
						>
							<n-form-item path="account">
								<n-input
									v-model:value="data.form_login.account"
									@keydown.enter.prevent="handleSubmit"
									:placeholder="$t('login.placeholderEmail')"
									clearable
									size="large"
									style="border-radius: 8px"
									:autofocus="false"
								/>
							</n-form-item>
							<n-form-item path="verify" v-if="data.opt.showVerify">
								<div class="w-full flex gap-2">
									<n-input
										v-model:value="data.form_login.verify"
										@keydown.enter.prevent="handleSubmit"
										:placeholder="$t('login.placeholderVerify')"
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
									:placeholder="$t('login.placeholderPwd')"
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
							{{ $t("login.AgreeWhenLogin") }}
							<n-button text :color="globalColors.btnActive">
								{{ $t("login.serviceAgreement", { msg: "Quchat" }) }}
							</n-button>
						</p>

						<p
							class="mt-[20px] cursor-pointer text-center"
							:style="{ color: globalColors.btnActive }"
						>
							{{ $t("login.forgetPwd") }}
						</p>

						<div class="flex items-center justify-center mt-[20px]">
							<div class="w-1/4 h-[1px] bg-gray-300 mr-2"></div>
							<p class="text-center" :style="{ color: globalColors.txtDeep }">
								{{ $t("login.thirdPartyLogin") }}
							</p>
							<div class="w-1/4 h-[1px] bg-gray-300 ml-2"></div>
						</div>

						<div class="flex justify-center gap-4 mt-[20px] p-2">
							<div
								class="bg-green-500 p-3 rounded-full"
								@click="handleThirdPartyLogin"
							>
								<Icon icon="cib:wechat" style="color: white" width="30" />
							</div>
						</div>
					</div>
				</n-tab-pane>

				<!-- 注册表单 -->
				<n-tab-pane name="registerMail" :tab="$t('common.register')">
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
								:placeholder="$t('login.placeholderEmail')"
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
									:placeholder="$t('login.placeholderVerify')"
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
								:placeholder="$t('login.placeholderPwd')"
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
								:placeholder="$t('login.placeholderPwdComfirm')"
								clearable
								size="large"
								style="border-radius: 8px"
								show-password-on="click"
							/>
						</n-form-item>
						<n-form-item path="invite">
							<n-input
								v-model:value="data.form_register.txtInvite"
								@keydown.enter.prevent
								:readonly="data.flagReadonlyInvite"
								:placeholder="$t('login.placeholderInviteCode')"
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
								{{ $t("common.register") }}
							</n-button>
						</n-form-item>
					</n-form>
				</n-tab-pane>
			</n-tabs>
		</div>
	</mModal>
</template>

<script lang="ts" setup>
import mModal from "@/components/common/mModal/index.vue";
import { computed, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import { FormItemRule, useMessage } from "naive-ui";
import { api } from "@/api/common";
import { useAppStore, useUserStore } from "@/store";
import { onMounted } from "vue";
import { isWeChatBrowser } from "@/utils/is";
import { nextTick } from "vue";
import { t } from "@/locales";

const msg = useMessage();
const userStore = useUserStore();
const appStore = useAppStore();

const refForm = ref();
const refFormMail = ref();
const refLogin = ref<typeof mModal>();

const data = reactive({
	isInWechatBrowser: computed(() => isWeChatBrowser()),
	qrCodeUrl: "", // 用来储存二维码 URL
	showQRCode: false, // 控制二维码显示和隐藏的状态
	loginType: "mail", // 登录方式
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
		btnTxtMail: t("login.getVerifyCode"),
		referee: "",
		flagDisabledBtnMail: false,
	},
	opt: {
		isShowModal: computed(() => appStore.showLoginModal),
		showVerify: false, // 表单是否显示 验证码
		btnVerifyTxt: t("login.getVerifyCode"), // 验证码按钮 文本
		btnSendVerifyDisabled: true, // 禁用 发送验证码按钮
		btnSubmitTxt: t("common.login"),
	},
	formRules: {
		account: [
			{
				key: "account",
				required: true,
				validator(rule: FormItemRule, value: string) {
					if (!value) {
						return new Error(t("login.placeholderEmail"));
					} else if (!data.regEmail.test(value)) {
						return new Error(t("login.errEmail"));
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
						return new Error(t("login.placeholderVerify"));
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
						return new Error(t("login.placeholderPwd"));
					} else if (value.length < 4 || value.length > 16) {
						return new Error(t("login.errPwdLength"));
					}
					return true;
				},
				trigger: ["blur"],
			},
		],
	},
});
const closeQRCode = () => {
	data.showQRCode = false;
};

// 处理第三方登录的方法
const handleThirdPartyLogin = async () => {
	const referee = data.form_register.referee || userStore.$state?.invitecode;
	console.log("是否在微信环境", data.isInWechatBrowser);
	if (data.isInWechatBrowser) {
		try {
			// 调用微信授权登录
			handleLoginWeichatAuth();
			//
		} catch (error) {
			msg.error("微信授权登录失败: " + error.message);
		}
	} else {
		console.log("二维码登录");
		try {
			// 获取微信登录二维码
			// 调用相应的api获取二维码链接
			const scene_id = Math.floor(Math.random() * 100000) + 1;
			const resData = await api.scan_qr({
				scene_id: scene_id,
				referee: referee,
			});
			data.qrCodeUrl =
				"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=" + resData?.ticket;
			data.showQRCode = true;

			let countDown = 3600;
			const timer = setInterval(() => {
				if (countDown <= 0) {
					clearInterval(timer);
				} else {
					countDown--;
					if (countDown % 4 === 0) {
						api
							.check_wechat_login({
								scene_id: scene_id,
								referee:
									data.form_register.referee || userStore.$state?.invitecode,
							})
							.then((response) => {
								if (response.status === "Success") {
									msg.success(response.message);
									userStore.updateUserInfo(response.data);
									clearInterval(timer);
									// 无刷新更新页面
									window.location.reload();
								}
							});
					}
				}
			}, 1000);
		} catch (error) {
			msg.error(`${t("login.errGetWechatQRCode")}: ${error.message}`);
		}
	}
};

// 微信浏览器中授权登录的方法
const handleLoginWeichatAuth = () => {
	// 微信授权登录
	const appId = import.meta.env.VITE_APP_WECHAT_APPID;
	const redirectUri = encodeURIComponent(
		import.meta.env.VITE_APP_WECHAT_REDIRECT_URI
	);

	const url = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${appId}&redirect_uri=${redirectUri}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect`;
	console.log(url);
	window.location.href = url;
};

// 专门用于注册表单的邮箱验证方法
const handleCheckRegisterForRegister = () => {
	if (data.regEmail && !data.regEmail.test(data.form_register.account)) {
		msg.error(t("login.errEmail"));
		return;
	}

	api
		.check_mail({
			email: data.form_register.account,
		})
		.then((res) => {
			msg.success(t("login.validEmail"));
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
			data.opt.btnVerifyTxt = t("login.resend");
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
		.register({
			email: data.form_register.account, // 修改为正确的引用
			emailCode: data.form_register.txtCode, // 修改为正确的引用
			password: data.form_register.txtPwd, // 修改为正确的引用
			referee: data.form_register.referee || userStore.$state?.invitecode, // 修改为正确的引用
		})
		.then((res) => {
			if (res.status != "Success") return msg.error(res.message);

			userStore.updateUserInfo(res.data);
			msg.success(res.message);
			changeLogin();
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
			changeLogin();
		})
		.catch((error) => {
			msg.error(error.message);
		});
};

const changeLogin = (show: boolean | undefined = undefined) => {
	if (refLogin.value) {
		refLogin.value.toggleModal(show);
	}
};

// 登录框 关闭时
const handleModalLoginClose = () => {
	appStore.changeShowLoginModal(false);
};

// 监听用户登录状态，改变模态框显示
onMounted(async () => {
	if (userStore.$state.userInfo == null) {
		appStore.changeShowLoginModal(true);
	}
	nextTick(() => {
		const hiddenInput = document.getElementById("hidden-input");
		if (hiddenInput) {
			hiddenInput.focus();
		}
	});
});

defineExpose({
	changeModalLoginShow: changeLogin,
});
</script>

<style lang="less" scoped></style>
