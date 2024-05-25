<template>
	<n-scrollbar>
		<div class="flex flex-col flex-1 min-h-0 px-[8px]">
			<div class="flex-1 min-h-0 pb-4 overflow-hidden">
				<!-- 聊天选项 单个 -->
				<template v-for="item in data.chatList" :key="item.id">
					<div
						@click="setChatActive(item)"
						class="chat-item-wrap w-full overflow-hidden grid grid-cols-[minmax(0,1fr)_1rem] px-[12px] py-[10px] rounded-md hover:cursor-pointer mb-1 items-center relative"
						:class="[`hover:bg-[${globalColors.bgChatActive}]`]"
						:style="{
							'background-color':
								data.curActiveChat == item.id ? globalColors.bgChatActive : '',
						}"
					>
						<div class="relative w-full flex">
							<n-avatar
								round
								size="large"
								:src="item.avatar"
								class="mr-[8px]"
							/>
							<div class="flex flex-col flex-1 overflow-hidden">
								<div
									class="flex flex-1 items-center mb-1 text-primary text-sm font-bold text-overflow"
								>
									<span class="overflow-hidden flex-shrink truncate mr-[5px]">
										{{ item.name }}
									</span>
								</div>
								<div class="text-placeholder truncate text-xs">
									{{ item.description }}
								</div>
							</div>
						</div>

						<!-- 右侧更多选项 -->
						<div
							class="chat-opt text-[#D4D4D4]"
							:class="[item.id == data.curActiveChat ? 'visible' : 'invisible']"
						>
							<n-dropdown
								trigger="hover"
								:options="data.opt.menuDropDown"
								@select="handleMenuSelect"
							>
								<div @click.stop="prehandlemenuSelect(item)">
									<Icon icon="mingcute:more-2-fill" width="18" />
								</div>
							</n-dropdown>
						</div>

						<div class="badge-container absolute -top-[3px] -right-[6px]">
							<div
								:class="[
									item.isPin && 'barge',
									item.id == data.curActiveChat ? 'opacity-100' : 'opacity-50',
								]"
							></div>
						</div>
					</div>
				</template>
			</div>
		</div>

		<mModal
			ref="refDeleteChat"
			title="删除"
			txtConfirm="确认"
			footerBtnSize="medium"
			footerBtnPadding=".5rem"
			footerComfirmBtnType="primary"
			@onPositiveClick="handleDelete"
		>
			<p>是否确认删除</p>
		</mModal>
	</n-scrollbar>
</template>

<script setup lang="ts">
import { globalColors } from "@/hooks/useTheme";
import { useChatStore, useNavStore } from "@/store";
import { reactive, computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { Icon } from "@iconify/vue";
import { renderIcon } from "@/utils/functions/index";
import { useMessage } from "naive-ui";
import mModal from "@/components/common/mModal/index.vue";
import { t } from "@/locales";

const { isMobile } = useBasicLayout();
const router = useRouter();
const navStore = useNavStore();
const chatStore = useChatStore();
const msg = useMessage();

const refDeleteChat = ref();
const data = reactive({
	curActiveChat: computed(() => chatStore.$state.curActive), // 当前激活的聊天ID
	chatList: computed(() => chatStore.$state.agentList),
	curActionTarget: {},
	opt: {
		menuDropDown: [
			{
				label: t("common.pin"),
				key: "pin",
				icon: () => renderIcon({ icon: "clarity:pin-line", width: 18 }),
			},
			{
				label: t("common.delete"),
				key: "delete",
				icon: () => renderIcon({ icon: "ph:trash", width: 18 }),
			},
		],
	},
});

// 激活标签
const setChatActive = (item): void => {
	chatStore.setCurrentAgent(item.id);
	router.push(`/chat/${item.id}`);
	if (isMobile.value) navStore.changeNavCollapsed();
};

// 预处理 打开下拉菜单时
const prehandlemenuSelect = (item) => {
	// 保存当前操作对象
	data.curActionTarget = item;
};

// 删除会话
const handleDelete = () => {
	// todo 删除接口 chatStore.deleteChat中请求
	const res = chatStore.deleteAgent(data.curActionTarget.id);
	console.log("删除", res);
	if (res) msg.success("删除成功");
	changeDeleteModalShow();
};

// 选择菜单中选项
const handleMenuSelect = (key: string | number, opt: DropdownOption, item) => {
	switch (key) {
		// 置顶
		case "pin":
			chatStore.pinChat(data.curActionTarget);
			break;

		// 删除
		case "delete":
			changeDeleteModalShow();
			break;
	}
};

// 改变模态框显示
const changeDeleteModalShow = () => {
	refDeleteChat.value.toggleModal();
};

// 页面加载时
onMounted(() => {});
</script>

<style lang="less" scoped>
// 单个聊天标签 包围
.chat-item-wrap {
	// 去除svg点击后出现的黑框
	svg {
		outline-style: none;
	}

	&:hover .chat-opt {
		visibility: visible;
	}

	// 单个聊天标签 右侧选项按钮
	// .chat-opt {
	//   // transition: all 0.1s ease-in;
	// }
}

.barge {
	width: 20px;
	height: 20px;
	transform-origin: left top;
	transform: rotate(-45deg);
	background-color: blue;
}
</style>
