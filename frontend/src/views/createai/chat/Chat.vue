<template>
	<div class="relative w-full h-full flex flex-col">
		<div class="w-full h-full overflow-hidden overflow-y-auto flex-1 pb-[30px]">
			<div
				class="w-full max-w-screen-xl m-auto dark:bg-[#101014] py-[24px] px-[36px]"
			>
				<template v-for="(item, index) in data.messages" :key="item.time">
					<div
						class="flex w-full mb-6 overflow-hidden items-start"
						:class="[
							item.role == 'assistant' ? 'flex-row' : 'flex-row-reverse',
						]"
					>
						<!-- 头像 -->
						<div
							class="flex items-center justify-center overflow-hidden rounded-full flex-none relative"
							:class="[item.role == 'assistant' ? 'mr-2' : 'ml-2']"
						>
							<n-avatar
								round
								size="medium"
								:src="(item?.avatar?.length > 0 && item?.avatar) || iconLogo"
							/>
						</div>
						<!-- 聊天区 -->
						<div class="overflow-hidden text-[15px] items-start">
							<!-- 日期 时间 -->
							<span class="text-xs text-[#b4bbc4] text-left">{{
								item.time
							}}</span>
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
		<div
			class="sticky bottom-0 p-4 w-full max-w-screen-xl m-auto flex items-end justify-between space-x-2"
		>
			<!-- <div
			class="h-[40px] flex items-center hover:cursor-pointer active:scale-95 overflow-hidden rounded-full transition-all duration-300 flex-none flex items-center justify-center px-3"
			:style="{ backgroundColor: globalColors.btnActive }"
		>
			<Icon
				icon="la:brush"
				width="28"
				color="white"
				style="transform: rotate(180deg)"
			/>
			<span
				class="ml-1 duration-300 transition-all text-white whitespace-nowrap overflow-hidden"
				:class="[data.isInputing ? 'w-0' : 'w-[48px]']"
			>
				新话题
			</span>
		</div> -->
			<!-- <n-button text @click="handleClear">
				<Icon icon="ph:trash" width="24" style="margin-bottom: 0.5rem" />
			</n-button> -->
			<div class="flex flex-col flex-1 h-full">
				<n-input
					v-model:value="data.txtInput"
					type="textarea"
					round
					size="large"
					:autosize="{
						minRows: 1,
						maxRows: 5,
					}"
					:placeholder="
						isMobile ? $t('chat.placeholderMobile') : $t('chat.placeholderPC')
					"
					@focus="handleInputFocus"
					@blur="handleInputBlur"
					@keypress.prevent.enter="handleInputEnter"
					style="border-radius: 20px"
				>
					<!-- 左侧 前缀 -->
					<template #prefix>
						<div
							class="h-full border-r pr-1 cursor-pointer flex flex-col justify-center"
							@click.stop="handleUpload"
						>
							<!-- 上传按钮 -->
							<Icon icon="tabler:upload" width="22" color="#7e7e7e" />
						</div>
					</template>

					<!-- 发送按钮 -->
					<template #suffix>
						<div class="h-full flex items-center">
							<div class="pr-2 cursor-pointer flex flex-col justify-center">
								<Icon icon="material-symbols:mic" width="22" color="#7e7e7e" />
							</div>
							<div
								class="pl-[2px] border-l cursor-pointer flex flex-col justify-center"
								@click="handleSend"
							>
								<Icon
									icon="entypo:paper-plane"
									width="28"
									:color="
										data.txtInput.length > 0
											? globalColors.btnActive
											: `#d2c4fc`
									"
								/>
							</div>
						</div>
					</template>
				</n-input>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useUserStore, useChatStore } from "@/store";
import { computed, reactive, watch } from "vue";
import { fetchChatAPI } from "@/api";
import { Icon } from "@iconify/vue";
import TextComponent from "@/views/chat/components/Text.vue";
import { globalColors } from "@/hooks/useTheme";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { SvgIcon } from "@/components/common";
import { useIconRender } from "@/hooks/useIconRender";
import { copyText } from "@/utils/format";
import { useDialog } from "naive-ui";
import iconLogo from "@/assets/logo.png";
import { t } from "@/locales";

const emits = defineEmits(["updateMessages", "deleteMsg"]);
const props = defineProps({
	msgList: {
		type: Array,
		default: () => [],
	},
	agent: {
		type: Object,
		default: () => ({}),
	},
});

const decoder = new TextDecoder("utf-8");
const userStore = useUserStore();
const chatStore = useChatStore();
const { isMobile } = useBasicLayout();
const { iconRender } = useIconRender();
const dialog = useDialog();

const defaultAvatar = "/avatar.jpg"; // replace with actual path

const data = reactive({
	userInfo: computed(() => userStore.$state.userInfo),
	txtInput: "",
	isInputing: false,
	loading: false,
	messages: computed(() => props.msgList),
	agent: computed(() => props.agent),
	opt: {
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

// 输入框激活
const handleInputFocus = () => {
	data.isInputing = true;
};

//输入框失焦
const handleInputBlur = () => {
	data.isInputing = false;
};

// 发送
const handleSend = () => {
	if (!data.txtInput) return;
	if (data.loading) return;
	// if (data.messages == null) {
	// 	chatStore.addChat();
	// }
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
		avatar: (data.agent?.avatar?.length > 0 && data.agent?.avatar) || iconLogo,
		isShowRaw: true,
	};

	// 显示加载中
	data.loading = true;
	// 添加可中断控制
	controller = new AbortController();
	// 滚动到到底部
	// scrollToBottom();
	// 获取数据
	// Add the object to the dataSources array
	const defaultPath = data.agent.defaultPath || "/v1/chat/completions";
	try {
		const { body, status } = await fetchChatAPI(
			{ messages: data.messages.slice(0, index), stream: true },
			data.agent.id,
			userStore.$state.userInfo.access_token,
			controller.signal,
			defaultPath
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
		// chatStore.setMessages();
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

			requestAnimationFrame(() => {
				//
			});
			// 弹出付费框
			if (status === 401) {
				// 弹出付费框
			}
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

// 聊天输入框 按回车时
const handleInputEnter = (event: KeyboardEvent) => {
	// 移动端
	if (isMobile.value) {
		if (event.key === "Enter" && event.ctrlKey) {
			handleSend();
		}
		return;
	}

	// 非移动端
	// shift + enter 换行
	if (event.key === "Enter" && event.shiftKey) {
		data.txtInput += "\n";
		return;
	}
	handleSend();
};

const appendLastMessageContent = (content: string, index: number) => {
	data.messages[index].content += content;
	// 在这里执行依赖于 DOM 更新的操作，比如滚动
	//   scrollToBottom();
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
			// chatStore.deleteChatMessage(index);
			emits("deleteMsg", index);
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
</script>

<style lang="less"></style>
