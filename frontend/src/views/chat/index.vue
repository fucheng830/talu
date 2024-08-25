<template>

	<div class="w-full h-full flex">
		<!-- 左侧 列表栏 -->
		<div
			v-if="!isMobile"
			class="flex flex-col h-full box-border relative overflow-hidden duration-500 ease-in-out border-l"
			:class="[data.opt.collapseLeft ? 'w-0' : 'w-[276px]']"
		>
		<div class="w-full p-4 flex justify-center items-center">
			<!-- 点击跳转路由到/createai/createRole-->
			<n-button
				style="background-color: #fff; width: 100%; padding-top: 1rem; padding-bottom: 1rem;"
				@click="router.push('/createai/createRole')"
			>
			<Icon icon="fluent:add-12-filled"/>
			<span class="pl-1">{{$t('chat.createAgent')}}</span>
			</n-button>
		</div>

			<!-- 聊天对象列表 -->
			<ChatList @changeAgent="changeAgent"/>
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
				</div>
			</div>

			<!-- 内容区 -->
			<Chat :messages="data.curChatInfo.agentHistory" :conversation_id="data.curChatInfo.conversation_id"/>
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
import { computed, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useChatStore, useNavStore, useUserStore, useSettingStore } from "@/store";
import { useRoute, useRouter } from "vue-router";
import Chat from "@/views/chat/components/Chat.vue";
import DropdownMenu from "@/components/common/DropdownMenu.vue";
import ChatList from "@/views/chat/components/ChatList.vue";
import ChatDetail from "@/views/chat/components/ChatDetail.vue";
import ShareChat from "@/views/chat/components/ShareChat.vue";
import { useThemeVars } from "naive-ui";
import { onMounted } from "vue";
import { v4 as uuidv4 } from 'uuid';

const { isMobile } = useBasicLayout();

const theme = useThemeVars();
// @ts-ignore
const btnDeactiveColor = computed(() => theme.value.btnDeative || '#D4D4D4'); // 添加默认值

const chatStore = useChatStore();
const navStore = useNavStore();
const userStore = useUserStore();
const settingStore = useSettingStore();
const router = useRouter();


const route = useRoute();

// 这是一个用于存储模态邀请链接的变量
const refModalShareChat = ref();

// 这是一个用于存储聊天详情的变量
const refChatDetail = ref();

// 当前页面数据
const data = reactive({
	curChatInfo: {
		agent: computed(() => chatStore.currentAgent()),
		agentHistory: [],
		conversation_id: uuidv4(),
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

function changeAgent(id: string) {
	console.log('changeAgent', id);
	// 修改当前智能体
	chatStore.setCurrentAgent(id);
	data.curChatInfo.agentHistory = [],
	data.curChatInfo.conversation_id = uuidv4();
}

onMounted(() => {
	// 当前页面智能体id
	const id = route.params.id;
	if (id) {
		changeAgent(String(id));
	}
	settingStore.fetchLLMConfig();
});
</script>


