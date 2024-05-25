<template>
	<div class="w-full h-full bg-gradient overflow-y-auto">
		<BgTopBar class="pt-2 px-3">
			<div class="flex flex-col items-center mt-[6rem]">
				<div class="relative flex justify-center">
					<div class="relative flex">
						<n-avatar
							round
							:size="72"
							:src="data.userInfo.avatar || '/avatar.jpg'"
						/>
					</div>
					<!-- 头像底部 vip按钮 -->
					<div
						class="absolute bottom-0 flex justify-center items-center w-full"
					>
						<!-- 转到vip支付页 -->
						<div
							v-if="!data.isvip"
							class="translate-y-1/2 flex-none"
							@click="routerGo('vipPay')"
						>
							<img
								:src="imgDownload"
								alt="imgDownload"
								class="h-[16px] rounded-full"
							/>
						</div>
						<div
							v-else
							class="translate-y-1/3 rounded-full bg-[#FFC300] flex items-center px-2"
						>
							<Icon icon="mingcute:vip-1-fill" style="color: #ff8d1a" />
							<div class="text-white rounded-full pl-1 font-bold">VIP</div>
						</div>
					</div>
				</div>

				<!-- 用户名 -->
				<div
					class="mt-[16px] text-[16px] leading-[22px] text-primary font-bold h-[22px]"
				>
					{{ data.userInfo?.username }}
				</div>

				<!-- 会员开通情况 -->
				<div class="mt-[4px] text-[14px] leading-[20px] h-[20px]">
					<span v-if="!data.isvip"> {{ $t("vip.notVIP") }} </span>
				</div>
			</div>

			<!-- 成为(激活)会员 -->
			<div class="w-full px-[32px] flex flex-col items-center">
				<div class="mt-[48px] flex items-center w-full max-w-[1120px]">
					<div class="h-[1px] flex-1 bg-[#E2E0E2]"></div>
					<div
						class="text-[32px] leading-[45px] mx-[24px] font-bold text-[#333639]"
					>
						{{ $t("vip.joinVIP") }}
					</div>
					<div class="h-[1px] flex-1 bg-[#E2E0E2]"></div>
				</div>
			</div>

			<!-- 激活按钮 -->
			<div class="mt-[16px] flex justify-center items-center">
				<n-button color="blue" size="large" round @click="changeModalShow">
					<div class="px-3 flex-center font-bold">
						<Icon icon="octicon:key-16" width="18" />
						<span class="ml-2"> {{ $t("vip.joinVIPKey") }} </span>
					</div>
				</n-button>
			</div>

			<!-- 套餐列表 grid -->
			<div class="w-full flex justify-center pb-8">
				<div
					class="grid max-w-[1120px] w-[95%] gap-[20px] mt-[32px]"
					:class="[isMobile ? 'grid-cols-1' : 'grid-cols-2']"
				>
					<!-- 单个 套餐 -->
					<template
						v-for="(item, i) in data.arrOrder"
						:key="`${item.title}${i}`"
					>
						<div class="flex justify-center">
							<div
								class="py-[24px] w-full max-w-[544px] items-start rounded-[16px] bg-white hover:translate-y-[-8px] hover:shadow-lg flex transition-transform cursor-pointer"
							>
								<div class="pl-[32px] flex-1 flex flex-col">
									<ul class="flex flex-wrap text-primary flex-col func-list">
										<!-- 单个 能力条 -->
										<template
											v-for="(curAbility, iAbility) in data.opt.ability"
											:key="`${curAbility.key}-${iAbility}`"
										>
											<li
												v-if="item.ability.hasOwnProperty(curAbility.key)"
												class="flex items-center mb-[16px] w-full text-[14px] leading-[28px]"
											>
												<Icon
													icon="dashicons:yes"
													:color="globalColors.btnActive"
													:width="18"
												/>
												<span class="ml-4 mr-1"> {{ curAbility.label }}: </span>
												<span :style="{ color: globalColors.btnActive }">
													<!-- 不同能力 福利 -->
													<span v-if="curAbility.key == 'roleCreatePro'">
														{{ $t("vip.support") }}
													</span>
													<span v-else-if="curAbility.key == 'useableRoleType'">
														{{ $t("vip.proEdition") }}
													</span>
													<span v-else>
														{{ item.ability[curAbility.key] }}
														<!-- <span v-if="curAbility.key == 'creatableRoleCount'">
															个
														</span> -->
													</span>
												</span>

												<span></span>
											</li>
										</template>
									</ul>
								</div>

								<!-- 右侧 描述 -->
								<div class="flex flex-col items-center border-l h-full w-[35%]">
									<!-- 标题 -->
									<div class="text-[14px] leading-[20px]">
										{{ item.title }}
									</div>
									<!-- 副标题 -->
									<div class="text-[12px] text-[#93909F] text-center">
										{{ item.subtitle }}
									</div>
									<!-- 套餐价格 -->
									<div class="mt-[16px] text-primary font-bold flex items-end">
										<div class="text-[18px] leading-[22px] mb-[4px]">￥</div>
										<div
											class="text-[48px] h-[48px] font-bold flex items-center"
										>
											{{ item.money }}
										</div>
									</div>
									<!-- 过期天数 -->
									<div class="mt-[4px] text-primary text-[14px]">
										{{ item.expire }} {{ $t("common.days") }}
									</div>
									<!-- 购买按钮 -->
									<div class="mt-[12px]">
										<n-button
											color="blue"
											size="large"
											style="border-radius: 8px"
											@click="payEvent(item)"
										>
											<span class="px-3"> {{ $t("common.purchase") }} </span>
										</n-button>
									</div>
								</div>
							</div>
						</div>
					</template>
				</div>
			</div>
		</BgTopBar>
	</div>

	<activate-vip ref="refModalActivateVip" />
	<ScanQrModal
		:show="data.qrshow"
		:orderId="data.orderId"
		:QrUrl="data.qr"
		@closeModal="data.qrshow = false"
	/>
	<PayCheck
		:orderId="data.orderId"
		:show="data.orderCheckShow"
		@close="data.orderCheckShow = false"
	/>
</template>

<script lang="ts" setup>
import BgTopBar from "@/views/layout/BgTopBar.vue";
import { computed, reactive, ref } from "vue";
import imgDownload from "@/assets/images/nav/icon_download.png";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import ActivateVip from "./components/ActivateVip.vue";
import ScanQrModal from "./components/ScanQrModal.vue";
import PayCheck from "./components/PayCheck.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useUserStore } from "@/store";
import { api } from "@/api/common";
import { useMessage } from "naive-ui";
import { t } from "@/locales";

const { isMobile } = useBasicLayout();
const userStore = useUserStore();
const message = useMessage();

const refModalActivateVip = ref();
const data = reactive({
	orderCheckShow: false,
	qrshow: false,
	qr: "",
	orderId: 0,
	// 用户信息
	userInfo: computed(() => userStore.userInfo),
	isvip: computed(() => userStore.isvip()),
	currentPlan: null,
	// 套餐列表 数据
	arrOrder: [
		{
			id: 1,
			title: t("vip.order1.title"),
			subtitle: t("vip.order1.subtitle"),
			money: 398,
			expire: 365,
			ability: {
				dailyChatCount: 200,
				creatableRoleCount: 20,
				creatableKnowledgeCount: 5,
			},
		},
		{
			id: 2,
			title: t("vip.order2.title"),
			subtitle: t("vip.order2.subtitle"),
			money: 998,
			expire: 365,
			ability: {
				dailyChatCount: 300,
				creatableRoleCount: 30,
				creatableKnowledgeCount: 10,
			},
		},
		{
			id: 3,
			title: t("vip.order3.title"),
			subtitle: t("vip.order3.subtitle"),
			money: 49,
			expire: 30,
			ability: {
				dailyChatCount: 100,
				creatableRoleCount: 5,
				creatableKnowledgeCount: 5,
			},
		},
		{
			id: 4,
			title: t("vip.order4.title"),
			subtitle: t("vip.order4.subtitle"),
			money: 128,
			expire: 30,
			ability: {
				dailyChatCount: 300,
				creatableRoleCount: 30,
				creatableKnowledgeCount: 10,
			},
		},
	],
	opt: {
		// 能力列表
		ability: [
			{
				label: t("vip.ability1"),
				key: "dailyChatCount",
			},
			{
				label: t("vip.ability2"),
				key: "roleCreatePro",
			},
			{
				label: t("vip.ability3"),
				key: "creatableRoleCount",
			},
			{
				label: t("vip.ability4"),
				key: "useableRoleType",
			},
			{
				label: t("vip.ability5"),
				key: "creatableKnowledgeCount",
			},
		],
	},
});

const changeModalShow = () => {
	refModalActivateVip.value.changeModalShow();
};

const payEvent = async (item) => {
	console.log("触发支付事件", item);
	// 根据当前的环境进行调用逻辑，分别有pc，h5，微信内
	// Define payment type based on environment
	data.orderId = new Date().valueOf();
	let trade_type = "NATIVE";
	if (isMobile.value) {
		if (window.navigator.userAgent.toLowerCase().includes("micromessenger")) {
			trade_type = "JSAPI"; // Use JSAPI for WeChat in-app payments
		} else {
			trade_type = "MWEB"; // Use MWEB for mobile web payments
		}
	}

	// Execute payment logic based on the trade type
	try {
		const response = await api.wechat_pay({
			plan_id: item.id,
			order_id: data.orderId,
			trade_type: trade_type,
		});
		handlePaymentResponse(trade_type, response);
	} catch (err) {
		// 使用message.error提示错误信息
		message.error("购买失败: " + err.message);
	}
};

// Function to handle different payment responses based on the trade type
function handlePaymentResponse(trade_type: string, response: any) {
	switch (trade_type) {
		// Handle native QR code payments
		case "NATIVE":
			data.qr = response?.code_url;
			data.qrshow = true;
			break;
		// Handle mobile web payments
		case "MWEB":
			// Redirect to MWEB URL for mobile web payments
			data.orderCheckShow = true;
			window.location.href = response.mweb_url;
			break;

		// Handle WeChat in-app payments
		case "JSAPI":
			// Start WeChat JSAPI payment process
			startWeChatPayment(response);
			break;
		default:
			message.error("Unsupported payment type: " + trade_type);
			break;
	}
}

// Function to start WeChat JSAPI payment process
function startWeChatPayment(data: any) {
	// Call WeChat JSAPI to start payment process
	WeixinJSBridge.invoke(
		"getBrandWCPayRequest",
		{
			appId: data.appId,
			timeStamp: data.timeStamp,
			nonceStr: data.nonceStr,
			package: data.package,
			signType: data.signType,
			paySign: data.paySign,
		},
		function (res: any) {
			// Handle payment result
			if (res.err_msg === "get_brand_wcpay_request:ok") {
				// Payment successful
				message.success("购买成功");
				// Check if the order is paid
				api
					.check_order({ order_id: data.orderId })
					.then((response) => {
						if (response?.status === "paid") {
							message.success("购买成功");
							userStore.updateUserInfo({
								vip_end_time: response?.vip_end_time,
								plan: response?.plan,
							});
							window.location.reload();
						}
					})
					.catch((err) => {
						console.log("订单未支付", err.message);
					});
			} else {
				// Payment failed
				message.error("购买失败: " + res.err_msg);
			}
		}
	);
}
</script>

<style></style>
