<template>
	<n-modal
		v-model:show="data.showModal"
		preset="dialog"
		:show-icon="false"
		:closable="false"
		style="
			width: 90%;
			max-width: 850px;
			padding: 0;
			border-radius: 10px;
			overflow: hidden;
		"
	>
		<div class="flex">
			<!-- modal 内部撑高 -->
			<div class="min-h-[560px] w-full" :class="[!isMobile && 'flex']">
				<!-- 左侧 tab栏 -->
				<div v-if="!isMobile" class="bg-[#F9FAFB] relative w-[240px]">
					<h3 class="p-[20px] text-[18px]">{{ $t("setting.title") }}</h3>
					<div class="mx-[20px]">
						<n-menu
							v-model:value="data.curMenu"
							:collapsed="data.collapsed"
							:collapsed-width="64"
							:collapsed-icon-size="22"
							:options="data.arrMenu"
						/>
					</div>

					<!-- 底部退出登录 -->
					<div class="absolute left-[24px] bottom-[16px]">
						<n-button ghost @click="handleLogout">
							<Icon icon="line-md:log-out" :width="20" />
							<span class="ml-1"> {{ $t("common.logout") }} </span>
						</n-button>
					</div>
				</div>

				<!-- 右侧 视图区 -->
				<div class="flex-1 flex flex-col">
					<header
						class="h-[64px] flex items-center px-[24px] border-b justify-between"
					>
						<h3 class="text-[16px]">{{ data.curMenuTxt }}</h3>
						<!-- 关闭 按钮 -->
						<Icon
							icon="simple-line-icons:close"
							width="22"
							color="#4D5052"
							@click="data.showModal = false"
						/>
					</header>

					<!-- 主视图 表单区 -->
					<main class="flex-1 relative overflow-hidden px-[24px] h-full">
						<!-- pc端 -->
						<div v-if="!isMobile" class="h-full">
							<!-- 用户设置 -->
							<template v-if="data.curMenu == 'userSetting'">
								<UserSetting />
							</template>
							<!-- 邀请好友 -->
							<template v-else-if="data.curMenu == 'invite'">
								<Invite />
							</template>
							<!-- 我的订单 -->
							<template v-else-if="data.curMenu == 'myOrder'">
								<MyOrder />
							</template>
							<!-- 激活码 -->
							<template v-else-if="data.curMenu == 'CDKey'">
								<CDKey />
							</template>
							<!-- 关于我们 -->
							<template v-else-if="data.curMenu == 'about'">
								<About />
							</template>
						</div>

						<!-- 移动端 -->
						<template v-else>
							<n-tabs
								type="line"
								animated
								tab-style=""
								@update:value="handleChangeTabs"
							>
								<n-tab-pane name="userSetting" tab="用户设置">
									<UserSetting @handleLogout="handleLogout" />
								</n-tab-pane>
								<n-tab-pane name="invite" tab="邀请好友">
									<Invite />
								</n-tab-pane>
								<n-tab-pane name="myOrder" tab="我的订单">
									<MyOrder />
								</n-tab-pane>
								<n-tab-pane name="CDKey" tab="激活码">
									<CDKey />
								</n-tab-pane>
								<n-tab-pane name="about" tab="关于我们">
									<About />
								</n-tab-pane>
							</n-tabs>
						</template>
					</main>
				</div>
			</div>
		</div>
	</n-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal";
import { computed, h, reactive, watch } from "vue";
import { Icon } from "@iconify/vue";
import UserSetting from "./UserSetting.vue";
import Invite from "./Invite.vue";
import MyOrder from "./MyOrder.vue";
import CDKey from "./CDKey.vue";
import About from "./About.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useUserStore } from "@/store";
import { useMessage } from "naive-ui";
import { globalColors } from "@/hooks/useTheme";
import { t } from "@/locales";

const renderIcon = ({ icon, color = "inherit", width = 22 }) => {
	return h(Icon, { icon, color, width });
};

const { isMobile } = useBasicLayout();
const userStore = useUserStore();
const msg = useMessage();

const colorTheme = globalColors.btnActive;

const data = reactive({
	showModal: false, // 模态框 显示
	collapsed: false, // 左侧菜单折叠
	curMenu: "userSetting",
	//   右侧面板标题
	curMenuTxt: computed(
		() => data.arrMenu.find((item) => item.key == data.curMenu).label
	),
	//   左侧菜单列表
	arrMenu: [
		{
			label: t("setting.menu.label1"),
			key: "userSetting",
			icon: () => renderIcon("mdi:person-details-outline"),
			template: UserSetting,
		},
		{
			label: t("setting.menu.label2"),
			key: "invite",
			icon: () => renderIcon("material-symbols:person-add-outline"),
			template: Invite,
		},
		{
			label: t("setting.menu.label3"),
			key: "myOrder",
			icon: () => renderIcon("lets-icons:order"),
			template: MyOrder,
		},
		{
			label: t("setting.menu.label4"),
			key: "CDKey",
			icon: () => renderIcon("ion:key-outline"),
			template: CDKey,
		},
		{
			label: t("setting.menu.label5"),
			key: "about",
			icon: () => renderIcon("material-symbols:info-outline"),
			template: About,
		},
	],
});

// 移动端改变tabs时同步更新PC端的tabs激活状态
const handleChangeTabs = (val: string) => {
	data.curMenu = val;
};

// 退出登录
const handleLogout = () => {
	userStore.resetUserInfo();
	changeModalSettingShow();
	msg.success("已退出登录！");
};

const changeModalSettingShow = () => {
	data.showModal = !data.showModal;
};

// 暴露 切换显示方法
defineExpose({
	changeModalShow: changeModalSettingShow,
});
</script>

<style lang="less" scoped>
:deep(*) {
	box-sizing: border-box;
	--n-bar-color: blue;
	--n-tab-text-color: grey;
	--n-tab-text-color-active: black;

	// menu组件 激活状态
	// v-bind无法生效，暂未使用全局变量
	// --n-item-color-active: v-bind("globalColors.btnActive");
	--n-item-color-active: #0653ff; // 激活状态背景色
	--n-item-color-active-hover: #0653ff; // 激活状态背景色 鼠标悬浮
	--n-item-text-color-active: whitesmoke; // 激活状态文字色
	--n-item-text-color-active-hover: whitesmoke; // 激活状态文字色 鼠标悬浮
}
</style>
