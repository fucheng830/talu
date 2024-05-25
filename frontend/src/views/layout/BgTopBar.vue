<template>
	<!-- 右上角 头像 -->
	<div
		v-if="props.isShow"
		class="w-full top-3 right-3 z-10 flex justify-between"
		:class="props.class"
	>
		<div>
			<div
				v-if="isMobile"
				@click="changeNavCollapsed"
				class="cursor-pointer w-[38px] h-[38px] bg-white rounded-full flex items-center justify-center"
			>
				<Icon
					v-if="isMobile"
					icon="oi:collapse-left"
					width="18"
					class="duration-500 rotate-180"
				/>
			</div>
		</div>

		<template v-if="props.showAvatar">
			<!-- <template v-if="data.userInfo">
				<n-avatar
					round
					size="large"
					:src="data.userInfo?.avatar || 'src/assets/avatar.jpg'"
					@click="changeModalSettingShow"
				/>
			</template> -->
			<!-- <template v-else>
				<n-button color="#fff" round @click="showModalLogin">
					<div class="px-3 flex items-center">
						<Icon icon="octicon:person-16" width="18" color="black" />
						<span class="ml-1 text-[black]">登录/注册</span>
					</div>
				</n-button>
			</template> -->
		</template>
	</div>

	<slot></slot>
</template>

<script lang="ts" setup>
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useAppStore, useNavStore, useUserStore } from "@/store";
import { Icon } from "@iconify/vue";
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";

const navStore = useNavStore();
const appStore = useAppStore();
const userStore = useUserStore();
const router = useRouter();

const { isMobile } = useBasicLayout();

const props = defineProps({
	isShow: {
		type: Boolean,
		default: true,
	},
	showAvatar: {
		type: Boolean,
		default: true,
	},
	class: {
		type: String,
		default: "",
	},
});

const data = reactive({
	isLogined: false,
	userInfo: computed(() => userStore.userInfo),
});

// 改变左侧导航栏折叠
const changeNavCollapsed = () => {
	navStore.changeNavCollapsed();
};

// 显示设置框
const changeModalSettingShow = (show = undefined) => {
	appStore.changeShowSettingModal(show);
};

// 显示登录框
const showModalLogin = () => {
	appStore.changeShowLoginModal(true);
};
</script>

<style lang="less" scoped></style>
