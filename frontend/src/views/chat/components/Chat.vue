<template>
	<div ref="scrollRef" class="h-full overflow-hidden overflow-y-auto flex-1">
		<div
			class="w-full max-w-screen-xl m-auto dark:bg-[#101014] py-[24px] px-[36px]"
		>
		    <!-- 消息列表 -->
			<template v-for="(item, index) in messages" :key="item.time">
				<div
					class="flex w-full mb-6 overflow-hidden items-start"
					:class="[item.role == 'assistant' ? 'flex-row' : 'flex-row-reverse']"
					@mouseenter="handleMouseEnter(index)"
					@mouseleave="handleMouseLeave(index)"
				>
					<!-- 头像 -->
					<div
						class="flex items-center justify-center overflow-hidden rounded-full flex-none relative"
						:class="[item.role == 'assistant' ? 'mr-2' : 'ml-2']"
					>
						<n-avatar round size="medium" :src="item.avatar" />
					</div>
					<!-- 聊天区 -->
					<div class="overflow-hidden items-start">
						<!-- 聊天内容 -->
						<div
							class="flex flex-col gap-1"
							:class="[item.role == 'user' ? 'flex-row-reverse' : '']"
						>   
                           <!-- 展示输入的附件 -->
							<div v-if="item.fileData" class="flex items-center gap-2">
								<template v-for="(file, index) in item.fileData">
									<div
										v-if="file.type.startsWith('image/')"
										class="w-[100px] h-[100px] relative"
									>
										<img
											:src="file.url"
											class="w-full h-full object-cover rounded-md"
										/>
									</div>
									<div
										v-else-if="file.type.startsWith('video/')"
										class="w-[100px] h-[100px] relative"
									>
										<video
											:src="file.url"
											class="w-full h-full object-cover rounded-md"
											controls
										/>
									</div>
									<div
										v-else-if="file.type.startsWith('audio/')"
										class="w-[100px] h-[100px] relative"
									>
										<audio
											:src="file.url"
											class="w-full h-full object-cover rounded-md"
											controls
										/>
									</div>
								</template>
							</div>

							<TextComponent
								ref="textRef"
								:inversion="item.role == 'user'"
								:error="item.error"
								:text="item.content"
								:loading="item.loading"
								:as-raw-text="!item.isShowRaw"
							/>
							 <!-- 占位符 -->
					
							<!-- 右下角工具栏 -->
							<div
    class="ml-3 space-x-2 h-5 transition-opacity duration-300"
    :class="{ 'opacity-0 invisible': !(index === messages.length - 1 || item.showTools), 'opacity-100': index === messages.length - 1 || item.showTools }"
							>
								<button
								class="mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300"
								@click="copyText({ text: item.content})"
							>
								<SvgIcon icon="ri:clipboard-line" />
								</button>
								<button
									class="mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300"
									@click="handleFavorite(index)"
								>
									<SvgIcon icon="ep:collection-tag" />
								</button>
								<button
								v-if="item.role != 'user'"
								class="mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300"
								@click="handleRegenerate(index)"
								>
								<SvgIcon icon="ri:restart-line" />
								</button>
								<NDropdown
								:trigger="isMobile ? 'click' : 'hover'"
								:placement="item.role != 'user' ? 'right' : 'left'"
								:options="data.opt.options(item)"
								@select="(val) => handleSelect(val, item, index)"
								>
								<button
									class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200"
								>
									<SvgIcon icon="lucide:ellipsis" />
								</button>
								</NDropdown>
							</div>

						</div>
					</div>
				</div>
			</template>

			<!-- 停止加载 -->
			<div class="sticky bottom-0 left-0 flex justify-center">
				<NButton v-if="data.loading" type="warning" @click="handleStop">
					<template #icon>
						<SvgIcon icon="ri:stop-circle-line" />
					</template>
					Stop Responding
				</NButton>
			</div>
		</div>
	</div>

  <!-- 底部输入栏 -->
  <div class="p-4 w-full max-w-screen-xl m-auto flex items-end justify-between space-x-2">
	<!-- 清空上下文 -->
    <n-button text @click="handleClear">
      <Icon icon="ph:trash" width="24" style="margin-bottom: 0.5rem" />
    </n-button>
    <ChatInput
      :placeholder="data.opt.placeholderChatInput"
      :showUpload="true"
      :showMic="true"
      @send="handleSend"
    />
  </div>
</template>

<script setup lang="ts">
import { useUserStore, useChatStore } from "@/store";
import { computed, onMounted, reactive, watch, ref, defineProps } from "vue";
import { fetchChatAPI } from "@/api";
import { Icon } from "@iconify/vue";
import TextComponent from "@/views/chat/components/Text.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { SvgIcon } from "@/components/common";
import { useIconRender } from "@/hooks/useIconRender";
import { copyText } from "@/utils/format";
import { useDialog } from "naive-ui";
import { useScroll } from "../hooks/useScroll";
import { useCopyCode, copyCodeBlock } from "../hooks/useCopyCode";
import { t } from "@/locales";
import { ChatInput } from "@/components/common";



const props = defineProps({
	messages: {
		type: Array as () => Chat.Message[],
		required: true,
	},
	conversation_id: {
		type: String,
		required: true,
	}
});

const { scrollRef, scrollToBottom, scrollToBottomIfAtBottom } = useScroll();
const decoder = new TextDecoder("utf-8");
const userStore = useUserStore();
const chatStore = useChatStore();
const { isMobile } = useBasicLayout();
const { iconRender } = useIconRender();
const dialog = useDialog();

useCopyCode();

const defaultAvatar = "/avatar.jpg"; // replace with actual path

const data = reactive({
	userInfo: computed(() => userStore.$state.userInfo),
	isInputing: false,
	loading: false,
	agent: computed(() => chatStore.currentAgent()),
	// 左边下拉菜单
	opt: {
		placeholderChatInput: computed(() =>
			isMobile.value ? t("chat.placeholderMobile") : t("chat.placeholderPC")
		),
		options: computed(() => (item: any) => {
			const common = [
				{
					label: t("common.delete"),
					key: "delete",
					icon: iconRender({ icon: "ri:delete-bin-line" }),
				},
			];

			if (item.role != "user") {
				common.unshift({
					label: item.isShowRaw ? t("chat.showRawText") : t("common.preview"),
					key: "toggleRenderType",
					icon: iconRender({
						icon: item.isShowRaw ? "ic:outline-code-off" : "ic:outline-code",
					}),
				});
			}

			return common;
		}),
	},
});

let controller = new AbortController();
// 发送
const handleSend = (txtInput: string, fileData: Chat.FileData) => {
	if (data.loading) return;

	// 消息内容
	const message: Chat.Message = {
		dateTime: new Date().toLocaleString(),
		content: txtInput,
		role: "user",
		error: false,
		loading: false,
		avatar: data.userInfo?.avatar || defaultAvatar,
		showTools: false,
		fileData: fileData,
	};
	// 添加到消息列表
	props.messages.push(message);
	const index = props.messages.length;

	scrollToBottom();

	generate(index);
};

// 对话处理
async function generate(index: number) {
	if (data.loading) return;

	// 获取上下文数量
	const contextCount = data.agent?.context.n; // 假设 agent 有 contextCount 属性
	let contextMessages; // 在外部定义 contextMessages

	if (contextCount) {
		const messagesToRetrieve = Math.min(contextCount, props.messages.length); // 取较小值
		contextMessages = props.messages.slice(-messagesToRetrieve); // 获取最近的上下文消息
	} else {
		// 没有限制
		contextMessages = props.messages; // 直接使用所有消息
	}

	props.messages[index] = {
		dateTime: new Date().toLocaleString(),
		content: '',
		role: "assistant",
		error: false,
		loading: true,
		avatar: data.agent?.avatar,
		isShowRaw: true,
		showTools: false,
	};

	// 显示加载中
	data.loading = true;
	// 添加可中断控制
	controller = new AbortController();
	// 滚动到到底部
	scrollToBottom();
	scrollToBottomIfAtBottom();
	// 获取数据
	const access_token = userStore.$state.userInfo?.access_token;
	if (!access_token) {
		props.messages[index].content = t("common.unlogin");
		props.messages[index].loading = false;
		data.loading = false;
		return;
	}



	try {
		const { body, status } = await fetchChatAPI(
			{ 
				messages: contextMessages, 
				stream: true, 
				conversation_id: props.conversation_id,
				config: data.agent 
			},
			data.agent.id,
			access_token,
			controller.signal
		);

		if (status === 200) {
			const reader = body?.getReader();
			await readStream(reader, status, index);
		} else {
			console.log("error", status);
			// const json = await body
			// const content = json.error?.message ?? "";
			// props.messages[index].content = content;
		}
	} catch (error: any) {
		console.log(error);
	} finally {
		props.messages[index].loading = false;
		controller.abort();
		data.loading = false;
	}
}

const readStream = async (
	reader: ReadableStreamDefaultReader<Uint8Array>,
	status: number,
	index: number
) => {
	let partialLine = "";

	while (true) {
		const { value, done } = await reader.read();
		if (done) break;

		const decodedText = decoder.decode(value, { stream: true });

		if (status !== 200) {
			const json = JSON.parse(decodedText);
			const content = json.error?.message ?? decodedText;
			console.log(content);

			requestAnimationFrame(() => {
				//
			});
			props.messages[index].content = content;

			return;
		}

		const chunk = partialLine + decodedText;
		const newLines = chunk.split(/\r?\n/);

		partialLine = newLines.pop() ?? "";

		for (const line of newLines) {
			if (line.length === 0) continue; // ignore empty message
			if (line.startsWith(":")) continue; // ignore sse comment message
			if (line === "data: [DONE]") return; //
			const json = JSON.parse(line.substring(6)); // start with "data: "

			if (json.choices[0].delta.content.length > 0)
				if (props.messages[index].loading == true) {
					props.messages[index].loading = false;
					props.messages[index].content = "";
				}

			const content =
				status === 200
					? (json.choices &&
							json.choices[0] &&
							json.choices[0].delta &&
							json.choices[0].delta.content) ||
					  ""
					: json.error.message;
			appendLastMessageContent(content, index);
		}
	}
};

const appendLastMessageContent = (content: string, index: number) => {
	props.messages[index].content += content;
	scrollToBottomIfAtBottom();
};

// 中止
const handleStop = () => {
	if (data.loading) {
		controller.abort();
		data.loading = false;
	}
};

// 重新生成
const handleRegenerate = (index: number) => {
	generate(index);
};

// 删除
const handleDelete = (index: number) => {
	if (data.loading) return;

	dialog.warning({
		title: t("chat.titleDeleteMessage"),
		content: t("chat.comfirmDeleteMessage"),
		positiveText: t("common.confirm"),
		negativeText: t("common.cancel"),
		onPositiveClick: () => {
			props.messages.splice(index, 1);
		},
	});
};

// 点击下拉列表 (更多操作)
const handleSelect = (
	key: "delete" | "toggleRenderType",
	item: any,
	index: number
) => {
	switch (key) {
		// 切换显示原文
		case "toggleRenderType":
			if (item.isShowRaw == undefined) return (item.isShowRaw = true);
			item.isShowRaw = !item.isShowRaw;
			return;
		// 删除
		case "delete":
			handleDelete(index);
	}
};

// 清空聊天记录
const handleClear = () => {
	dialog.warning({
		title: t("chat.clearChat"),
		content: t("chat.comfirmClearChat"),
		positiveText: t("common.confirm"),
		negativeText: t("common.cancel"),
		onPositiveClick: () => {
			props.messages.splice(0, props.messages.length);
		},
	});
};

const handleMouseEnter = (index: number) => {
	props.messages[index].showTools = true;
};

const handleMouseLeave = (index: number) => {
	if (index !== props.messages.length - 1) {
		props.messages[index].showTools = false;
	}
};

onMounted(() => {
	scrollToBottom();
});

// 请求完毕后为赋值代码按钮添加点击事件
watch(
	() => data.loading,
	() => {
		if (!data.loading) copyCodeBlock();
	}
);
</script>

<style lang="less">
</style>