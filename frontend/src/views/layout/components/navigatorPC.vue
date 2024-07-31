<!-- 最左侧导航栏 -->
<template>
	<div
		class="h-full w-[88px] bg-[#F2F5F8] flex flex-col items-center py-[10px] select-none"
	>
		<div class="h-full flex flex-col items-center justify-between">
			<div class="flex flex-col items-center">
				<!-- 导航列表 -->
				<nav-list />
			</div>

			<!-- 下半部分 -->
			<div class="flex-col flex items-center" v-if="data.userInfo">
				<!-- 邀请 -->
				<div
					@click="changeModalInviteUrlShow"
					class="w-[84px] h-[98px] relative mb-[20px] cursor-pointer"
				>
					<img
						:src="imgBgCard"
						alt="imgBgCard"
						class="w-full h-full absolute left-0 top-0"
					/>
					<div class="flex flex-col w-full h-full relative items-center">
						<img
							:src="imgIconGift"
							alt="imgIconGift"
							class="w-[32px] h-[32px] mt-[12px]"
						/>
						<span class="w-[48px] text-[12px] text-[#93909F] text-center">
							{{ $t("share.inviteFriendReward") }}
						</span>
					</div>
				</div>

				<!-- 头像 -->
				<div class="cursor-pointer mb-[20px]">
					<div
						class="relative flex justify-center"
						@click="routerGo('/vipPay')"
					>
						<div class="relative flex">
							<n-avatar
								round
								size="large"
								:src="data.userInfo.avatar ?? ''"
							/>
						</div>
						<!-- 头像底部 vip按钮 -->
						<div
							class="absolute bottom-0 flex justify-center items-center w-full"
						>
							<!-- 转到vip支付页 -->
							<div v-if="!userStore.isvip()" class="translate-y-1/2 flex-none">
								<div class="rounded-full bg-white flex items-center p-[2px]">
									<img
										:src="imgDownload"
										alt="imgDownload"
										class="h-[16px] rounded-full"
									/>
								</div>
							</div>
							<div
								v-else
								class="rounded-full flex items-center px-1 p-[1px] bg-[#FFC300]"
								style="transform: translateY(60%)"
							>
								<Icon
									icon="mingcute:vip-1-fill"
									style="color: #ff8d1a; font-size: 0.7rem"
								/>
								<div
									class="text-white rounded-full pl-1 font-bold"
									style="font-size: 0.6rem"
								>
									VIP
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- 设置按钮 -->
				<div
					@click="changeModalSettingShow"
					class="w-[40px] h-[40px] bg-white rounded-full m-button flex justify-center items-center cursor-pointer"
					:class="`hover:text-[${globalColors.btnActive}]`"
				>
					<Icon icon="uiw:setting-o" :width="20" />
				</div>
			</div>
			<!-- 登录 -->
			<div v-else class="p-2">
				<n-button :color="globalColors.btnActive" @click="showModalLogin">
					{{ $t("common.login") }}
				</n-button>
			</div>
		</div>
	</div>

	
</template>

<script setup lang="ts">
import { computed, reactive} from "vue";
import { globalColors } from "@/hooks/useTheme";
import imgBgCard from "@/assets/images/nav/bg_card.png";
import imgIconGift from "@/assets/images/nav/icon_gift.png";
import imgDownload from "@/assets/images/nav/icon_download.png";
import { Icon } from "@iconify/vue";
import NavList from "@/views/layout/components/NavList.vue";
import { RouteLocationRaw, useRouter } from "vue-router";
import { useAppStore, useUserStore } from "@/store";

const router = useRouter();

const userStore = useUserStore();
const appStore = useAppStore();

const emits = defineEmits([
	"changeModalSettingShow",
	"changeModalInviteUrlShow",
]);

const data = reactive({
	userInfo: computed(() => userStore.userInfo),
});

const changeModalInviteUrlShow = () => {
	emits("changeModalInviteUrlShow");
};

const changeModalSettingShow = () => {
	emits("changeModalSettingShow");
};

// 转到
const routerGo = (path: RouteLocationRaw) => {
	router.push(path);
};

// 显示 登录弹窗
const showModalLogin = () => {
	appStore.changeShowLoginModal(true);
};
</script>

<style></style>
