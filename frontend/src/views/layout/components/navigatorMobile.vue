<template>
	<!-- 遮罩层 -->
	<div
		class="h-full absolute bg-black/40 z-40"
		:class="[navStore.isNavcollapsed ? 'w-0' : 'w-full']"
		@click="changeNavCollapsed"
	>
		<!-- 左侧导航栏 -->
		<div
			class="flex flex-col h-full overflow-hidden bg-[white] duration-500 max-w-full"
			:class="[navStore.isNavcollapsed ? 'w-0' : 'w-[314px]']"
			@click.stop="() => {}"
		>
			<!-- 顶部logo栏 -->
			<div
				class="mx-[8px] flex items-center border-darker h-layout-header flex-none border-b"
			>
				<!-- logo -->
				<div
					class="h-full flex-1 overflow-hidden px-[8px] hover:cursor-pointer flex items-center py-3"
				>
					<n-avatar
						:size="36"
						src="https://site.123qiming.com/image/3f40de780cb29eb51519a0ce4c7f5d08.png"
						class="mr-3"
					/>
					<span
						class="text-[20px] leading-[28px] text-primary font-bold text-overflow flex-1"
						>{{ data.site_name }}</span
					>
				</div>
				<!-- 折叠按钮 -->
				<div @click="changeNavCollapsed">
					<Icon icon="oi:collapse-left" width="18" class="duration-500 mr-2" />
				</div>
			</div>

			<!-- 导航按钮栏 -->
			<div class="px-[8px] flex-none">
				<div
					class="w-full flex flex-wrap layout-row-menu py-[12px] gap-[8px] border-b border-darker"
				>
					<!-- 导航按钮 单个 -->
					<template v-for="item in data.navList" :key="item.path">
						<div
							class="h-[40px] flex items-center justify-center rounded-[8px] box-content flex-1 py-[2px] bg-[#0000000A] cursor-pointer hover:bg-white transition-all"
							@click="routerGo(item.path)"
						>
							<Icon :icon="item.icon" :width="20" />
							<span class="ml-1">{{ item.label }}</span>
						</div>
					</template>
				</div>
			</div>

			<!-- 聊天列表 -->
			<ChatList />

			<div class="p-[16px]">
				<div
					@click="changeModalInviteUrlShow"
					class="hover:cursor-pointer shadow-[0px 4px 8px 0px rgba(22,3,117,0.05)] h-[40px] justify-between flex items-center text-[12px] bg-white rounded-full cursor-pointer pl-[16px] pr-[8px]"
				>
					<div class="flex items-center gap-2">
						<img
							:src="imgIconGift"
							alt="imgIconGift"
							class="w-[32px] h-[32px]"
						/>
						<span class="font-bold text-ellipsis overflow-hidden">
							{{ $t("share.inviteFriendMobile") }}
						</span>
					</div>
					<Icon icon="mingcute:right-fill" width="14" />
				</div>
			</div>

			<div
				class="flex flex-none items-center justify-between min-w-0 px-3 h-[64px] overflow-hidden border-t border-darker dark:border-neutral-800 relative"
			>
				<div class="flex-1 flex-shrink-0 overflow-hidden mr-[4px]">
					<div class="flex items-center overflow-hidden">
						<n-avatar
							round
							size="large"
							:src="data.userInfo?.avatar || '/avatar.jpg'"
						/>
						<div class="flex-1 ml-2 overflow-hidden">
							<div class="flex flex-col overflow-hidden">
								<h2
									class="flex font-bold text-sm truncate hover:cursor-pointer items-center"
								>
									<span class="text-overflow mr-[4px] max-w-[300px]">
										{{ data.userInfo?.username }}
									</span>
									<img
										:src="imgDownload"
										alt="imgDownload"
										class="h-[16px] rounded-full"
									/>
								</h2>
								<div class="flex items-center">
									<div class="text-regular text-xs mt-1 ml-1">
										<!-- 剩余聊天
                    <span
                      class="cursor-pointer"
                      :style="{
                        color: globalColors.btnActive,
                      }"
                    >
                      {{ data.userInfo?.user_info?.usable_token}}
                    </span>
                    条 -->
										<span
											class="cursor-pointer font-bold"
											:style="{
												color: globalColors.btnActive,
											}"
											@click="routerGo('/vipPay')"
										>
											{{ $t("common.JoinVIP") }}
										</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- 设置按钮 -->
				<n-button
					size="large"
					color="white"
					strong
					circle
					@click="changeModalSettingShow"
				>
					<Icon icon="uiw:setting-o" :width="20" color="black" />
				</n-button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { Icon } from "@iconify/vue";
import ChatList from "@/views/chat/components/ChatList.vue";
import { computed, reactive } from "vue";
import { useNavStore, useUserStore } from "@/store";
import { globalColors } from "@/hooks/useTheme";
import imgIconGift from "@/assets/images/nav/icon_gift.png";
import imgDownload from "@/assets/images/nav/icon_download.png";
import { useRouter } from "vue-router";

const { isMobile } = useBasicLayout();
const navStore = useNavStore();
const userStore = useUserStore();
const router = useRouter();

const emits = defineEmits([
	"changeModalSettingShow",
	"changeModalInviteUrlShow",
]);

const data = reactive({
	site_name: "QUCHAT",
	curActive: computed(() => navStore.curActive),
	navList: computed(() =>
		navStore.navList.filter((item) => item.path != "/chat")
	),
	userInfo: computed(() => userStore.userInfo),
});

// 转到指定路由
const routerGo = (path) => {
	router.push(path);
	if (!navStore.isNavcollapsed) navStore.changeNavCollapsed();
};

// 改变左侧导航栏折叠
const changeNavCollapsed = () => {
	navStore.changeNavCollapsed();
};

const changeModalInviteUrlShow = () => {
	emits("changeModalInviteUrlShow");
};

const changeModalSettingShow = () => {
	emits("changeModalSettingShow");
};
</script>

<style lang="less" scoped>
// 取消折叠过程中因空间不足导致的自动换行
* {
	white-space: nowrap;
	flex-wrap: nowrap;
}
</style>
