<template>
	<div class="w-full h-full flex relative">
		<!-- 左侧 导航栏 -->
		<!-- PC端 -->
		<template v-if="!isMobile">
			<navigatorPC
				:userInfo="data.userInfo"
				@changeModalSettingShow="changeModalSettingShow"
				@changeModalInviteUrlShow="changeModalInviteUrlShow"
			/>
		</template>
		<template v-else>
			<!-- 移动端 -->
			<navigatorMobile
				@changeModalSettingShow="changeModalSettingShow"
				@changeModalInviteUrlShow="changeModalInviteUrlShow"
			/>
		</template>

		<!-- 主内容 -->
		<div
			class="h-full flex-1"
			:style="{ backgroundColor: globalColors.bgMain }"
			style="width: calc(100% - 88px)"
		>
			<router-view />
		</div>

		<!-- 邀请 -->
		<!-- todo 改为单独登录页的路由地址，加载邀请码 -->
		<invite-url
			ref="refModalInviteUrl"
			:title="$t('share.defaultTitle')"
			:urlCopy="`?invitecode=${data.userInfo?.user_id}#/square`"
		/>
		<!-- 设置 弹窗 -->
		<settingModel ref="refModalSetting" />
	</div>
	<Login ref="refLogin" />
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import SettingModel from "@/views/settingModal/index.vue";
import { useRouter } from "vue-router";
import InviteUrl from "@/views/layout/components/InviteUrl.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import navigatorPC from "@/views/layout/components/navigatorPC.vue";
import navigatorMobile from "@/views/layout/components/navigatorMobile.vue";
import { useAppStore, useUserStore } from "@/store";
import Login from "@/views/layout/Login.vue";

const appStore = useAppStore();
const userStore = useUserStore();
const router = useRouter();
const { isMobile } = useBasicLayout();

const refModalInviteUrl = ref();
const refModalSetting = ref();

const refLogin = ref();
const data = reactive({
	userInfo: computed(() => userStore.$state.userInfo),
});

// 改变邀请弹窗的显示
const changeModalInviteUrlShow = () => {
	refModalInviteUrl.value.changeModalShow();
};

// 改变设置弹窗的显示
const changeModalSettingShow = () => {
	if (refModalSetting.value) {
		refModalSetting.value.changeModalShow();
	}
};

// 实时更新设置模态框显示状态
watch(
	() => appStore.showSettingModal,
	(val) => {
		changeModalSettingShow(val);
	},
	{ deep: true }
);

// 更改登录弹窗 显示
watch(
	() => appStore.showLoginModal,
	(val) => {
		refLogin.value.changeModalLoginShow(val);
	}
);
</script>

<style lang="less" scoped></style>
