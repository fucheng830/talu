<template>
	<!-- 遮罩层 -->
	<div
		class="flex max-w-[276px]"
		:class="[
			data.opt.collapseRight ? 'w-0' : 'w-full',
			isMobile
				? 'h-full absolute bg-black/40 z-40'
				: 'transition-all duration-500',
		]"
		@click="changeCollapseRight"
	>
		<div
			class="h-full transition-all flex-none overflow-hidden duration-500 bg-[#F5F7FA]"
			:class="[
				isMobile ? 'fixed right-0' : 'relative',
				isMobile && data.opt.collapseRight ? 'w-0' : 'w-[276px]',
			]"
			@click.stop="() => {}"
		>
			<div class="h-full flex flex-col">
				<!-- 顶部 名称 信息 -->
				<div
					class="flex items-start justify-start py-[16px] px-[12px] mx-[8px] mb-2 border-b"
				>
					<!-- 头像 -->
					<div class="relative flex">
						<n-avatar round size="large" :src="data.chatInfo?.avatar" />
					</div>
					<div class="flex flex-col gap-y-1 text-xs ml-[10px] flex-1">
						<!-- 名称 -->
						<div class="flex-1 text-[15px] font-bold text-[#1A1A1A]">
							{{ data.chatInfo?.name }}
						</div>
						<div class="text-regular text-[12px] line-height-[17px] h-[17px]">
							<n-tag :bordered="false">
								<div class="flex items-center">
									<Icon icon="et:chat" :width="12" />
									<span class="text-xs text-[grey] ml-1">
										{{ data.chatInfo?.description }}
									</span>
								</div>
							</n-tag>
						</div>
						<!-- 总对话信息 -->
						<!-- <div class="text-regular text-[12px] line-height-[17px] h-[17px]">
							<n-tag :bordered="false">
								<div class="flex items-center">
									<Icon icon="et:chat" :width="12" />
									<span class="text-xs text-[grey] ml-1">
										共 {{ data.chatInfo?.total }} 条对话
									</span>
								</div>
							</n-tag>
						</div> -->
					</div>
				</div>

				<div class="h-full flex flex-col">
					<!-- 历史对话 -->
					<div class="flex-1">
						<div class="font-bold text-[18px] py-2 px-4">
							{{ $t("chat.chatHistory") }}
						</div>
						<div class="w-full h-full">
							<div class="flex mx-[8px] gap-x-[8px]">
								<n-button
									tag="div"
									type="primary"
									:bordered="false"
									size="large"
									@click="handleCreateChat"
									color="white"
									text-color="black"
									class="hover:text-[#0000ff] text-[black] flex-1"
								>
									<!-- class="hover:text-[#0000ff]" -->
									<!-- :style="{ background: 'white'}" -->
									<Icon
										icon="la:brush"
										width="22"
										color="black"
										style="transform: rotate(180deg)"
									/>
									<span class="ml-1"> {{ $t("chat.newTopics") }} </span>
								</n-button>
								<n-button
									tag="div"
									:bordered="false"
									size="large"
									:color="data.isCheckingMultiple ? '#ebeaed' : 'white'"
									@click="handleSelectMultiple"
								>
									<Icon icon="mynaui:list-check" width="22" color="black" />
								</n-button>
							</div>

							<!-- 列表超长度时会抢下面容器的长度，现限制下面容器已解决 -->
							<!-- <n-scrollbar> -->
							<div class="h-full overflow-auto max-h-[40vh] my-[6px]">
								<div class="flex flex-col gap-[8px] text-sm py-[16px]">
									<!-- 历史选项 单个 -->
									<template
										v-for="item in data.agentHistory.chatList"
										:key="item.id"
									>
										<div
											class="relative chat-item flex items-center mx-[8px]"
											@click="handleCurHistoryChange(item)"
										>
											<div
												class="px-[12px] flex-1 overflow-hidden h-[40px] flex hover:bg-[#ebeaed] items-center rounded-full text-base active:scale-100"
												:class="[
													item.id == data.agentHistory.curActiveChat
														? 'bg-[#ebeaed]'
														: '',
												]"
											>
												<div
													class="flex-1 overflow-hidden h-full flex items-center break-all cursor-pointer group"
												>
													<Icon
														:icon="
															item.id == data.agentHistory.curActiveChat
																? 'heroicons-solid:chat'
																: 'heroicons-outline:chat'
														"
														width="22"
														:color="
															item.id == data.agentHistory.curActiveChat
																? globalColors.btnActive
																: 'black'
														"
													/>
													<!-- 标题 -->
													<div
														class="ml-1 relative flex-1 overflow-hidden break-all text-ellipsis whitespace-nowrap text-sm select-none"
														:style="{
															color:
																item.id == data.agentHistory.curActiveChat
																	? globalColors.btnActive
																	: '',
														}"
													>
														{{ item.name }}
													</div>
												</div>

												<!-- 右侧 按钮组 -->
												<div
													class="flex gap-x-2 visible more-icon hover-visible"
												>
													<!-- 编辑按钮 -->
													<Icon
														icon="carbon:edit"
														width="18"
														:color="
															item.id == data.agentHistory.curActiveChat
																? globalColors.btnActive
																: 'black'
														"
														@click="handleEditChat(item)"
														class="cursor-pointer"
													/>
													<!-- 删除按钮 -->
													<Icon
														icon="fluent:delete-28-regular"
														width="18"
														:color="
															item.id == data.agentHistory.curActiveChat
																? globalColors.btnActive
																: 'black'
														"
														@click="handleDeleteChat(item)"
														class="cursor-pointer"
													/>
												</div>
											</div>
										</div>
									</template>
								</div>
							</div>
							<!-- </n-scrollbar> -->
						</div>
					</div>

					<!-- 提示词 -->
					<!-- <div class="h-[45vh] border-t">
						<div class="font-bold text-[18px] py-2 px-4">提示词</div>
						<div class=""></div>
					</div> -->
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useChatStore } from "@/store";

const { isMobile } = useBasicLayout();
const chatStore = useChatStore();

const data = reactive({
	agentHistory: computed(() => chatStore.currentAgentHistory()),
	chatInfo: computed(() => chatStore.currentAgent()),
	isCheckingMultiple: false, // 历史话题 多选状态
	opt: {
		collapseRight: false,
	},
});

console.log("当前的agentHistory", data.agentHistory);

// 创建 新话题
const handleCreateChat = () => {
	console.log("创建新话题");
	chatStore.addChat();
};

// 删除话题
const handleDeleteChat = (item) => {
	chatStore.deleteChat(item.id);
};

// 切换选择状态
const handleSelectMultiple = () => {
	data.isCheckingMultiple = !data.isCheckingMultiple;
};

// 修改当前激活历史
const handleCurHistoryChange = (curHistory) => {
	data.agentHistory.curActiveChat = curHistory.id;
};

// 改变右侧栏 折叠
const changeCollapseRight = () => {
	data.opt.collapseRight = !data.opt.collapseRight;
};

// 移动端时自动隐藏右侧详情栏
watch(
	() => isMobile,
	(val) => {
		// if (val.value) data.opt.collapseRight = true;
		data.opt.collapseRight = val.value;
	},
	{ deep: true, immediate: true }
);

// 暴露方法给父组件
defineExpose({
	collapseRight: computed(() => data.opt.collapseRight),
	changeCollapseRight,
});
</script>

<style lang="less" scoped>
// 取消折叠过程中因空间不足导致的自动换行
* {
	white-space: nowrap;
	flex-wrap: nowrap;
}

:deep(*) {
	--n-bar-color: blue;
	--n-tab-text-color: grey;
	--n-tab-text-color-active: black;
	// font-size: 18px;
	// color: grey;
	// background-color: transparent !important;
}

.btn {
	display: flex;
	height: 40px;
	-webkit-user-select: none;
	-moz-user-select: none;
	user-select: none;
	align-items: center;
	justify-content: center;
	border-radius: 5px;
	--tw-bg-opacity: 1;
	background-color: rgb(255 255 255 / 1);
}
</style>
