<template>
	<div ref="scrollRef" class="h-full overflow-hidden overflow-y-auto flex-1">
		<div
			class="w-full max-w-screen-xl m-auto dark:bg-[#101014] py-[24px] px-[36px]"
		>
		    <!-- 消息列表 -->
			<template v-for="(item, index) in data.messages" :key="item.time">
				<div
					class="flex w-full mb-6 overflow-hidden items-start"
					:class="[item.role == 'assistant' ? 'flex-row' : 'flex-row-reverse']"
				>
					<!-- 头像 -->
					<div
						class="flex items-center justify-center overflow-hidden rounded-full flex-none relative"
						:class="[item.role == 'assistant' ? 'mr-2' : 'ml-2']"
					>
						<n-avatar round size="medium" :src="item.avatar" />
					</div>
					<!-- 聊天区 -->
					<div class="overflow-hidden text-[15px] items-start">
						<!-- 聊天内容 -->
						<div
							class="flex items-end gap-1 mt-2"
							:class="[item.role == 'user' ? 'flex-row-reverse' : '']"
						>
							<TextComponent
								ref="textRef"
								:inversion="item.role == 'user'"
								:error="item.error"
								:text="item.content"
								:loading="item.loading"
								:as-raw-text="!item.isShowRaw"
							/>

							<!-- 右下角工具栏 -->
							<div class="flex flex-col">
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
										<SvgIcon icon="ri:more-2-fill" />
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
	  :data=data
      @send="handleSend"
    />
  </div>
</template>

<script setup lang="ts">
import { useUserStore, useChatStore } from "@/store";
import { computed, onMounted, reactive, watch } from "vue";
import { fetchChatAPI } from "@/api";
import { Icon } from "@iconify/vue";
import TextComponent from "@/views/chat/components/Text.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { SvgIcon } from "@/components/common";
import { useIconRender } from "@/hooks/useIconRender";
import { copyText } from "@/utils/format";
import { useDialog } from "naive-ui";
import { useScroll } from "../hooks/useScroll";
import { useCopyCode, copyCodeBlock } from "@/views/chat/hooks/useCopyCode.ts";
import { t } from "@/locales";
import { ChatInput } from "@/components/common";

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
	txtInput: "",
	isInputing: false,
	loading: false,
	messages: computed(() => chatStore.getMessages()),
	agent: computed(() => chatStore.currentAgent()),
	opt: {
		placeholderChatInput: computed(() =>
			isMobile.value ? t("chat.placeholderMobile") : t("chat.placeholderPC")
		),
		options: computed(() => (item: any) => {
			const common = [
				{
					label: t("common.copy"),
					key: "copyText",
					icon: iconRender({ icon: "ri:file-copy-2-line" }),
				},
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
const handleSend = () => {
	if (data.txtInput.trim() === "") return;
	if (data.loading) return;
	if (data.messages == null) {
		chatStore.addChat();
	}
	// 消息内容
	const message = {
		dateTime: new Date().toLocaleString(),
		content: data.txtInput,
		role: "user",
		error: false,
		loading: false,
		avatar: data.userInfo?.avatar || defaultAvatar,
	};
	// 添加到消息列表
	data.messages.push(message);
	// 清空输入框
	data.txtInput = "";
	const index = data.messages.length;

	scrollToBottom();

	generate(index);
};

// 对话处理
async function generate(index: number) {
	if (data.loading) return;

	data.messages[index] = {
		dateTime: new Date().toLocaleString(),
		content: `${t("chat.thinking")}...`,
		role: "assistant",
		error: false,
		loading: true,
		avatar: data.agent?.avatar,
		isShowRaw: true,
	};

	// 显示加载中
	data.loading = true;
	// 添加可中断控制
	controller = new AbortController();
	// 滚动到到底部
	// scrollToBottom();
	scrollToBottomIfAtBottom();
	// 获取数据
	// Add the object to the dataSources array
	const access_token = userStore.$state.userInfo?.access_token;
	if (!access_token) {
		data.messages[index].content = t("common.unlogin");
		data.messages[index].loading = false;
		data.loading = false;
		chatStore.setMessages();
		return;
	}

	console.log(access_token);
	try {
		const { body, status } = await fetchChatAPI(
			{ messages: data.messages.slice(0, index), stream: true },
			data.agent.id,
			access_token,
			controller.signal
		);

		if (body) {
			const reader = body.getReader();
			await readStream(reader, status, index);
		}
	} catch (error: any) {
		console.log(error);
	} finally {
		data.messages[index].loading = false;
		controller.abort();
		data.loading = false;
		chatStore.setMessages();
	}
}

const readStream = async (
	reader: ReadableStreamDefaultReader<Uint8Array>,
	status: number,
	index: number
) => {
	let partialLine = "";

	while (true) {
		// eslint-disable-next-line no-await-in-loop
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

			// 弹出付费框

			// 添加到消息列表
			data.messages[index].content = content;

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

			// 有内容返回后，取消输入中状态，否则不会渲染内容
			if (json.choices[0].delta.content.length > 0)
				if (data.messages[index].loading == true) {
					data.messages[index].loading = false;
					data.messages[index].content = "";
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
	data.messages[index].content += content;
	// 在这里执行依赖于 DOM 更新的操作，比如滚动
	// scrollToBottom();
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
			// 删除当前消息
			chatStore.deleteChatMessage(index);
		},
	});
};

// 点击下拉列表 (更多操作)
const handleSelect = (
	key: "copyText" | "delete" | "toggleRenderType",
	item: any,
	index: number
) => {
	switch (key) {
		// 切换显示原文
		case "toggleRenderType":
			if (item.isShowRaw == undefined) return (item.isShowRaw = true);
			item.isShowRaw = !item.isShowRaw;
			return;

		// 复制
		case "copyText":
			copyText({ text: item.content ?? "" });
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
			// 删除当前消息
			chatStore.clearMessages();
		},
	});
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

<style lang="less"></style>
