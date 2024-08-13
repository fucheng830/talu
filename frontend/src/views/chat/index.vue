<template>

	<div class="w-full h-full flex">
		<!-- 左侧 列表栏 -->
		<div
			v-if="!isMobile"
			class="flex flex-col h-full box-border relative overflow-hidden duration-500 ease-in-out border-l"
			:class="[data.opt.collapseLeft ? 'w-0' : 'w-[276px]']"
		>
			<div class="w-full p-4 flex justify-center align-center">
				<!-- 点击跳转路由到/createai/createRole-->
				<n-button
					class="btn-radius"
					style="background-color: #fff"
					@click="router.push('/createai/createRole')"
				>
					<span class="px-[3rem]"> {{ $t("chat.createAgent") }} </span>
				</n-button>
			</div>

			<!-- 聊天对象列表 -->
			<ChatList />
		</div>

		<!-- 中间聊天区 -->
		<div
			class="flex-1 overflow-hidden h-full flex flex-col bg-white border-l border-r"
		>
			<!-- rounded-[25px] -->
			<!-- 顶部标题栏 -->
			<div
				class="sticky top-0 left-0 right-0 px-5 justify-between relative flex items-center min-w-0 overflow-hidden h-[56px] border-b"
			>
				<!-- 左侧 -->
				<div class="flex items-center">
				 <!-- 折叠按钮 -->
				 <div class="flex items-center gap-4 mr-4">
					<n-button text @click="changeCollapseLeft">
						<Icon
							icon="mdi:arrow-collapse-left"
							width="18"
							:color="btnDeactiveColor"
							:class="[data.opt.collapseLeft || isMobile ? 'rotate-180' : '']"
						/>
					</n-button>
				</div>
				<!-- Agent展示 -->
				<div class="flex items-center space-x-2">
					<!-- 头像 -->
					<div class="rounded-full overflow-hidden w-10 h-10">
						<img :src=data.curChatInfo.agent?.avatar alt="Avatar" class="w-full h-full object-cover">
					</div>
					<!-- 名称和描述 -->
					<div>
						<div class="flex items-center space-x-1">
						<span class="font-semibold">{{ data.curChatInfo.agent?.name }}</span>
						<DropdownMenu />
						</div>
						<p class="text-xs">{{ data.curChatInfo.agent?.description }}</p>
					</div>
				</div>
				 </div>


				<!-- 右侧按钮栏 -->
				<div class="flex items-center space-x-4">
					<!-- 分享 -->
					<Icon icon="ic:outline-share" 
							width="18" 
							:color="btnDeactiveColor"
							@click="changeModalShareChatShow" />
					<!-- 配置区 -->
					<Icon
						icon="icon-park-outline:setting-config"
						width="18"
						:color="btnDeactiveColor"
						@click="changeCollapseRight"
					/>
					<!-- 详情区 展开 -->
					<Icon
						icon="mdi:arrow-collapse-right"
						width="18"
						:color="btnDeactiveColor"
						@click="changeCollapseRight"
					/>
					
				</div>
			</div>

			<!-- 内容区 -->
			<Chat />
		</div>

		<!-- 右侧 详情区 -->
		<ChatDetail ref="refChatDetail" />

		<!-- 邀请 弹窗 -->
		<ShareChat
			ref="refModalShareChat"
			:title="
				$t('share.shareAgentTitle', { name: data.curChatInfo.agent?.name })
			"
			:urlCopy="`chat/${data.curChatInfo.agent?.id}`"
		/>
	</div>
</template>

<script setup lang="ts">
import { globalConfig } from "@/hooks/useTheme";
import { computed, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useChatStore, useNavStore, useUserStore } from "@/store";
import { useRoute, useRouter } from "vue-router";
import Chat from "@/views/chat/components/Chat.vue";
import DropdownMenu from "@/components/common/DropdownMenu.vue";
import ChatList from "@/views/chat/components/ChatList.vue";
import ChatDetail from "@/views/chat/components/ChatDetail.vue";
import ShareChat from "@/views/chat/components/ShareChat.vue";
import { useThemeVars } from "naive-ui";

import { watch } from "vue";
import { onMounted } from "vue";


const { isMobile } = useBasicLayout();

const theme = useThemeVars();
// @ts-ignore
const btnDeactiveColor = computed(() => theme.value.btnDeative || '#D4D4D4'); // 添加默认值

const chatStore = useChatStore();
const navStore = useNavStore();
const userStore = useUserStore();
const router = useRouter();

const route = useRoute();

// 这是一个用于存储模态邀请链接的变量
const refModalShareChat = ref();
// 这是一个用于存储聊天详情的变量
const refChatDetail = ref();
// 当前页面智能体id
const id = route.params.id || "43c7076a-861f-4454-8047-cd55afc0fef2";
console.log("初始化的agentId", id);

// 当前页面数据
const data = reactive({
	isCollapseRight: computed(() => refChatDetail.value?.collapseRight), // 显示 右侧信息栏
	curChatInfo: {
		agent: computed(() => chatStore.currentAgent()),
		agentHistory: computed(() => chatStore.currentAgentHistory()),
	},
	opt: {
		collapseLeft: false,
		userInfo: computed(() => userStore.$state.userInfo),
	},
});

// 改变左侧栏 折叠
const changeCollapseLeft = () => {
	if (isMobile.value) return navStore.changeNavCollapsed();
	data.opt.collapseLeft = !data.opt.collapseLeft;
};

// 改变右侧栏 折叠
const changeCollapseRight = () => {
	refChatDetail.value.changeCollapseRight();
};

// 改变邀请弹窗的显示
const changeModalShareChatShow = () => {
	refModalShareChat.value.changeModalShow();
};

onMounted(() => {
	// 监听当前页面智能体id的变化
	if (!id) {
		// 获取聊天记录
		console.log("没有id");
	}
});

watch(
	() => id,
	(newVal) => {
		if (newVal) {
			// 获取聊天记录
			console.log("id", newVal);
			if (newVal == null) {
				// 获取聊天记录
				console.log("ids", newVal);
			} else {
				// 获取聊天记录
				console.log("id1212", newVal);
				chatStore.setCurrentAgent(String(newVal));
			}
		}
	},
	{ immediate: true }
);
</script>

<style lang="less" scoped>
.btn-radius {
	border-radius: v-bind("globalConfig.btnRadius");
}
</style>
