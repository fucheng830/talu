<template>
	<!-- 创建 agent -->
	<div class="h-full w-full flex flex-col">
		<!-- 顶部栏 -->
		<div
			class="relative flex h-14 w-full items-center justify-between gap-2 border-b border-token-border-medium px-3 flex-shrink-0 bg-[white]"
		>
			<!-- 左侧 -->
			<div class="flex items-center gap-2">
				<div @click="() => router.replace('/createai')">
					<Icon icon="icon-park-outline:left" width="24" />
				</div>

				<!-- 未选择头像时 -->
				<template v-if="data.form.avatar === null">
					<div
						class="flex w-[34px] h-[34px] items-center justify-center rounded-full border-2"
						:class="[data.form.avatar === null ? '' : 'border-dashed']"
					></div>
				</template>
				<!-- 已选择头像时 -->
				<template v-else>
					<n-avatar round :size="34" :src="data.form.avatar" />
				</template>

				<div class="flex flex-col">
					<!-- agent 名称 -->
					<span class="text-sm font-medium">{{ data.form.name }}</span>
					<div class="flex items-center gap-1">
						<!-- 左侧 小点 -->
						<div class="h-1.5 w-1.5 rounded-full bg-[#9B9B9B]"></div>
						<span class="text-xs text-[grey]">Draft</span>
					</div>
				</div>
			</div>

			<!-- 右侧按钮栏 -->
			<div class="flex items-center gap-2">
				<!-- 更多 -->
				<n-dropdown
					trigger="click"
					:options="data.opt.menu.more"
					@select="handleMoreSelect"
				>
					<n-button>
						<Icon icon="ri:more-fill" width="18" />
					</n-button>
				</n-dropdown>

				<!-- 更多 -->
				<n-popover :overlap="overlap" placement="bottom-end" trigger="click">
					<template #trigger>
						<n-button :color="theme.primaryColor">
							<div class="flex gap-1 items-center">
								{{ $t("common.save") }}
								<Icon icon="mingcute:down-fill" width="18" />
							</div>
						</n-button>
					</template>

					<SaveAgent @saveForm="updatePublish" @emitForm="emitRole" />
				</n-popover>
			</div>
		</div>

		<!-- 主要内容区 -->
		<div class="relative flex w-full grow overflow-hidden bg-[white]">
			<div class="flex w-full justify-center md:w-1/2">
				<div class="h-full grow overflow-hidden">
					<div
						v-if="!data.isShowAddAction"
						class="flex h-full flex-col pt-2 items-center"
					>
						<div class="w-[90%] max-w-[25rem] flex justify-center">
							<n-tabs v-model:value="data.curPage" type="segment" animated>
								<n-tab-pane name="create" :tab="$t('common.create')">
								</n-tab-pane>
								<n-tab-pane name="config" :tab="$t('common.config')">
								</n-tab-pane>
								<template v-if="isMobile">
									<n-tab-pane name="preview" :tab="$t('common.preview')">
									</n-tab-pane>
								</template>
							</n-tabs>
						</div>

						<!-- 对话页面 -->
						<template v-if="data.curPage == 'create'">
							<Chat
								:msgList="dataChat.builder.msgList"
								@deleteMsg="handleDeleteBuilderMsg"
								:agent="dataChat.builder.agent"
							/>
						</template>

						<!-- 配置页面 -->
						<template v-else-if="data.curPage == 'config'">
							<div class="w-full grow overflow-hidden">
								<n-scrollbar style="width: 100%">
									<div
										class="h-full grow flex flex-col gap-4 px-4 py-6 text-sm"
									>
										<!-- 头像 -->
										<div class="flex w-full items-center justify-center gap-4">
											<n-dropdown
												trigger="click"
												size="huge"
												:options="data.opt.menu.avatar"
												@select="handleSelect"
											>
												<div
													class="flex w-[74px] h-[74px] items-center justify-center rounded-full border-2"
													:class="[
														data.form.avatar === null ? '' : 'border-dashed',
													]"
												>
													<!-- 未选择头像时 -->
													<template v-if="data.form.avatar === null">
														<Icon icon="ic:round-plus" width="34" />
													</template>
													<!-- 已选择头像时 -->
													<template v-else>
														<n-avatar
															round
															:size="74"
															:src="data.form.avatar"
														/>
													</template>
												</div>
											</n-dropdown>
										</div>

										<!-- 名称 -->
										<div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">{{
															$t("createai.name")
														}}</span>
													</template>
													<span> {{ $t("createai.nameDesc") }} </span>
												</n-tooltip>
											</div>

											<n-input
												v-model:value="data.form.name"
												type="text"
												clearable
												:placeholder="$t('createai.placeholderName')"
											/>
										</div>

										<!-- 描述 -->
										<div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">{{
															$t("createai.desc")
														}}</span>
													</template>
													{{ $t("createai.descDesc") }}
												</n-tooltip>
											</div>

											<n-input
												v-model:value="data.form.description"
												type="text"
												clearable
												:placeholder="$t('createai.placeholderDesc')"
											/>
										</div>

										<!-- 介绍 -->
										<div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">{{
															$t("createai.instructions")
														}}</span>
													</template>
													{{ $t("createai.instructionsDesc") }}
												</n-tooltip>
											</div>

											<n-input
												v-model:value="data.form.system_prompt"
												type="textarea"
												:autosize="{
													minRows: 4,
													maxRows: 12,
												}"
												:placeholder="$t('createai.placeholderInstructions')"
											/>
										</div>

										<!-- 对话开头语 -->
										<div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">{{
															$t("createai.conversationStarters")
														}}</span>
													</template>
													{{ $t("createai.conversationStartersDesc") }}
												</n-tooltip>
											</div>

											<n-input
												v-model:value="data.form.opening_text"
												type="textarea"
												:autosize="{
													minRows: 3,
													maxRows: 7,
												}"
												:placeholder="
													$t('createai.placeholderConversationStarters')
												"
											/>
										</div>

										<!-- 对话开头 问题 -->
										<div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">{{
															$t("createai.startQuestion")
														}}</span>
													</template>
													{{ $t("createai.startQuestionDesc") }}
												</n-tooltip>
											</div>

											<template
												v-for="(item, i) in data.form.opening_question"
												:key="`question-${i}`"
											>
												<n-input-group>
													<n-input
														v-model:value="data.form.opening_question[i]"
														placeholder=""
														@input="(val) => handleStarterInput(val, i)"
													/>
													<n-button
														v-if="data.form.opening_question.length > 1"
														ghost
														@click="deleteStarters(i)"
													>
														<Icon icon="material-symbols:close" />
													</n-button>
												</n-input-group>
											</template>
										</div>

										<!-- 自动建议 -->
										<div class="mt-4">
											<n-collapse>
												<n-collapse-item
													:title="$t('createai.autoSuggestion')"
													name="autoSuggestion"
												>
													<!-- 右侧按钮 -->
													<template #header-extra>
														<div @click.stop="() => {}">
															<n-popselect
																v-model:value="
																	data.form.autoSuggestion.useAutoSuggestion
																"
																:options="[
																	{ label: $t('common.enable'), value: true },
																	{
																		label: $t('common.disabled'),
																		value: false,
																	},
																]"
																trigger="click"
															>
																<n-button quaternary>
																	{{
																		data.form.autoSuggestion.useAutoSuggestion
																			? $t("common.enable")
																			: $t("common.disabled")
																	}}

																	<div class="ml-1">
																		<Icon icon="mingcute:down-fill" />
																	</div>
																</n-button>
															</n-popselect>
														</div>
													</template>

													<div class="text-[#1c1d2399]">
														<!-- 关闭自动建议 -->
														<span
															v-if="!data.form.autoSuggestion.useAutoSuggestion"
														>
															{{ $t("createai.autoSuggestionDescDisabled") }}
														</span>

														<!-- 开启自动建议 -->
														<div v-else class="flex flex-col gap-2">
															<span>
																{{ $t("createai.autoSuggestionDescEnabled") }}
															</span>

															<!-- 是否用户自定义prompt -->
															<n-checkbox
																v-model:checked="
																	data.form.autoSuggestion.isCustom
																"
																:label="$t('createai.customPrompt')"
															/>

															<!-- prompt -->
															<n-input
																v-model:value="
																	data.form.autoSuggestion.txtCustom
																"
																type="textarea"
																:autosize="{
																	minRows: 4,
																	maxRows: 16,
																}"
																:placeholder="
																	$t('createai.placeholderCustomPrompt')
																"
															/>
														</div>
													</div>
												</n-collapse-item>
											</n-collapse>
										</div>

										<!-- 知识库 -->
										<n-collapse>
											<n-collapse-item
												:title="$t('createai.knowledge')"
												name="knowledge"
											>
												<div class="flex flex-col gap-1.5">
													<div class="cursor-default">
														<n-tooltip trigger="hover">
															<template #trigger>
																<span class="font-medium">{{
																	$t("createai.knowledgeSubtitle")
																}}</span>
															</template>
															{{ $t("createai.knowledgeDesc") }}
														</n-tooltip>
													</div>

													<div class="rounded-lg text-[#9B9B9B]">
														{{ $t("createai.knowledgeDesc") }}
													</div>

													<n-button @click="changeModalSelectKnowledgeShow">
														{{ $t("createai.selectKnowledge") }}
													</n-button>

													<!-- 已引用知识库 -->
													<div class="flex flex-col gap-1">
														<!-- 单个知识库 -->
														<template
															v-for="item in data.form.knowledge"
															:key="item.uuid"
														>
															<div
																class="flex justify-between items-center gap-2 px-3 py-1 hover:bg-[#ECECF0] rounded-xl"
															>
																<div class="flex-1 flex items-center gap-4">
																	<!-- 图标 -->
																	<Icon icon="tdesign:data" width="18" />

																	<!-- 中间信息 -->
																	<div class="flex-1 flex flex-col">
																		<span
																			class="text-[13px] font-bold overflow-hidden text-ellipsis whitespace-nowrap"
																			>{{ item.name }}</span
																		>
																	</div>
																</div>

																<!-- 添加按钮 -->
																<n-button
																	text
																	size="small"
																	@click="deleteKnowledge(i)"
																>
																	<Icon icon="lets-icons:remove" width="16" />
																</n-button>
															</div>
														</template>
													</div>
												</div>
											</n-collapse-item>
										</n-collapse>

										<!-- 功能 -->
										<div class="flex flex-col gap-1.5">
											<!-- <div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">能力</span>
													</template>
													该Agent拥有的功能
												</n-tooltip>
											</div> -->
											<!-- 能力设置 -->
											<div v-if="data.formActions.list.length > 0" class="mt-4">
												<n-collapse>
													<n-collapse-item
														:title="$t('createai.capabilities')"
														name="additionalSettings"
													>
														<n-checkbox
															v-model:checked="data.form.improveOurModels"
															:label="$t('createai.webBrowsing')"
														/>
														<n-checkbox
															v-model:checked="data.form.improveOurModels"
															:label="$t('createai.DALLEImageGeneration')"
														/>
													</n-collapse-item>
												</n-collapse>
											</div>

											<!-- <div class="mt-4">
												<n-collapse>
													<n-collapse-item title="工作流" name="flow">
														<n-checkbox
															v-model:checked="data.form.improveOurModels"
															label="使用Agent中的会话数据来改进我们的模型"
														/>
													</n-collapse-item>
												</n-collapse>
											</div> -->

											<!-- <n-space vertical>
												<n-checkbox
													v-model:checked="data.form.webBrowsing"
													label="浏览网页"
												/>
												<n-checkbox
													v-model:checked="data.form.DALLE"
													label="DALL·E 图片生成"
												/>
												<div class="flex items-center">
													<n-checkbox
														v-model:checked="data.form.codeInterpreter"
														label="代码解释器"
													/>
													<IconTip
														msg="允许该Agent运行代码，启用后，该Agent可以分析数据、处理您上传的文件、进行数学运算等等。当开启代码解释器时，文件将允许被下载"
													/>
												</div>
											</n-space> -->
										</div>

										<!-- 网络请求 -->
										<!-- <div class="flex flex-col gap-1.5">
											<div class="cursor-default">
												<n-tooltip trigger="hover">
													<template #trigger>
														<span class="font-medium">网络请求</span>
													</template>
													该Agent能使用的API
												</n-tooltip>
											</div>

											<div class="flex flex-col gap-1">
												<template
													v-for="(item, i) in data.formActions.list"
													:key="`${item?.name}-${i}`"
												>
													<div
														@click="changeModalAuthShow(true, i, item)"
														class="flex rounded-lg border border-token-border-medium text-sm hover:cursor-pointer"
													>
														<div class="h-9 grow px-3 py-2">
															<span>{{ item.name }}</span>
														</div>
														<div class="border-l flex items-center px-3">
															<Icon icon="uil:setting" width="18" />
														</div>
													</div>
												</template>

												<div>
													<n-button
														@click="
															changeModalAuthShow(
																true,
																data.formActions.list.length
															)
														"
													>
														创建新请求
													</n-button>
												</div>
											</div>
										</div> -->
									</div>
								</n-scrollbar>
							</div>
						</template>

						<!-- 预览 选自页面右侧代码部分，如有修改需重新覆盖 -->
						<template v-else-if="data.curPage == 'preview'">
							<Chat
								:msgList="dataChat.preview.msgList"
								@deleteMsg="handlePreviewBuilderMsg"
								:agent="dataChat.preview.agent"
							/>

							<template v-if="dataChat.preview.msgList.length <= 0">
								<div
									class="absolute w-full top-[50%] -translate-y-[50%] flex justify-center items-center"
								>
									<div class="w-full flex flex-col items-center gap-2">
										<div
											v-if="data.form.avatar === null"
											class="w-[48px] h-[48px] flex justify-center items-center border-2 rounded-full bg-white"
										>
											<Icon icon="lucide:box" width="32" color="#B4B4B4" />
										</div>

										<template v-else>
											<n-avatar round :size="48" :src="data.form.avatar" />
										</template>

										<span class="font-bold">{{ data.form.name }}</span>
									</div>
								</div>
							</template>
						</template>
					</div>
					<!-- 添加请求 表单 -->
					<template v-else>
						<AddAction
							:curIndex="data.formActions.curIndex"
							:curAction="data.formActions.list[data.formActions.curIndex]"
							@changeShowAddAction="data.isShowAddAction = false"
							@saveForm="saveAddActionForm"
							@deleteAction="deleteAction"
						/>
					</template>
				</div>
			</div>

			<!-- 右侧预览 -->
			<div
				class="relative w-1/2 flex flex-col justify-center border-l pt-2 bg-[#F9F9F9]"
				:class="[isMobile && 'hidden']"
			>
				<div class="flex justify-center py-1">
					<div class="group flex items-center gap-2 text-lg font-medium">
						{{ $t("common.preview") }}
					</div>
				</div>

				<Chat
					:msgList="dataChat.preview.msgList"
					@deleteMsg="handlePreviewBuilderMsg"
					:agent="dataChat.preview.agent"
				/>

				<template v-if="dataChat.preview.msgList.length <= 0">
					<div
						class="absolute w-full top-[50%] -translate-y-[50%] flex justify-center items-center"
					>
						<div class="w-full flex flex-col items-center gap-2">
							<div
								v-if="data.form.avatar === null"
								class="w-[48px] h-[48px] flex justify-center items-center border-2 rounded-full bg-white"
							>
								<Icon icon="lucide:box" width="32" color="#B4B4B4" />
							</div>

							<template v-else>
								<n-avatar round :size="48" :src="data.form.avatar" />
							</template>

							<span class="font-bold">{{ data.form.name }}</span>
						</div>
					</div>
				</template>
			</div>
		</div>

		<SelectKnowledge
			ref="refSelectKnowledge"
			:knowledgeList="data.form.knowledge"
			@saveForm="updateKnowledge"
		/>
	</div>
</template>

<script lang="ts" setup>
import { h, onMounted, reactive, ref, watch } from "vue";
import { Icon } from "@iconify/vue";
import { useRoute, useRouter } from "vue-router";
import { useIconRender } from "@/hooks/useIconRender";
import {
	DropdownOption,
	NButton,
	NUpload,
	useDialog,
	useMessage,
} from "naive-ui";
import SaveAgent from "@/views/createai/components/SaveAgent.vue";
import { useStateStore, useUserStore } from "@/store";
import AddAction from "@/views/createai/components/AddAction.vue";
import Chat from "@/views/createai/chat/Chat.vue";
import { getFormattedDate } from "@/utils/functions";
import { useBasicLayout } from "@/hooks/useBasicLayout";
// import { createAgent } from "@/views/createai/langChainUtils.ts";
import { api } from "@/api/common";
import { v4 as uuidv4 } from "uuid";
import SelectKnowledge from "@/views/createai/components/SelectKnowledge.vue";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();

const { iconRender } = useIconRender();
const { isMobile } = useBasicLayout();

const route = useRoute();
const router = useRouter();
const dialog = useDialog();
const userStore = useUserStore();
const stateStore = useStateStore();
const msg = useMessage();

const refSelectKnowledge = ref();

const data = reactive({
	form: {
		name: "New Agent", // 名称
		description: "", // 描述
		system_prompt: "", // 介绍
		avatar: "", // 头像
		// avatar: "https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg",
		// author: "Author", // 作者
		opening_text: "", // 开头语
		// todo 用户可点击发送
		opening_question: [""], // 对话初始化时引导式问题
		autoSuggestion: {
			useAutoSuggestion: true,
			isCustom: true,
			txtCustom: "",
		},
		knowledge: [], // 知识库
		webBrowsing: true, // 网页浏览
		DALLE: true, // DALL·E 生成
		codeInterpreter: false, // 代码解释器
		improveOurModels: true, // 使用GPT中的会话数据来改进我们的模型
		permission: "temp", // 如果没有点击保存，默认是temp将不展示在我的智能体列表
	},
	// 请求列表
	formActions: {
		curIndex: undefined, // 当前请求下标
		// 请求列表
		list: [
			// !DELETE 对接接口后删除
			{
				name: "http",
				txtAuth: "无",
			},
			{
				name: "web",
				txtAuth: "无",
			},
		],
	},
	curPage: "create", // 当前左侧页面 ( create | config )
	isShowAvatarDropdown: false,
	isShowAddAction: false,
	opt: {
		curID: route.params.id || uuidv4(), // 当前ID
		menu: {
			more: [
				{
					label: t("createai.deleteAgent"),
					key: "delete",
					icon: iconRender({
						icon: "material-symbols:delete-outline",
						fontSize: "18",
					}),
				},
			],
			avatar: [
				{
					label: t("createai.uploadPic"),
					key: "upload",
					type: "render",
					render: () =>
						// 上传组件
						h(
							NUpload,
							{
								// todo 替换为上传接口地址
								action: "https://site.123qiming.com/upload_image",
								headers: {
									Authorization: `Bearer ${userStore.$state.userInfo?.access_token}`,
								},
								"show-file-list": false,
								max: 1,
								onFinish: handleUploadAvatar,
							},
							// 子组件
							// 按钮
							[
								h(
									NButton,
									{
										block: true,
										quaternary: true,
										size: "large",
									},
									t("createai.uploadPic")
								),
							]
						),
				},
				{
					label: `DALL·E ${t("createai.generate")}`,
					key: "dall_e",
				},
			],
		},
	},
});

// 上传头像
const handleUploadAvatar = (opt) => {
	const res = JSON.parse(opt.event.target.response);
	console.log(res.data.image_url);
	data.form.avatar = res.data.image_url;
};

// 对话数据
const dataChat = reactive({
	// gpt生成器
	builder: {
		// 对话记录
		msgList: [
			{
				avatar: '/chatbot.png',
				content: t("createai.defaultStarter"),
				dateTime: new Date().toLocaleString(),
				error: false,
				loading: false,
				role: "assistant",
			},
		],
		agent: {
			id: data.opt.curID,
			defaultPath: "/v1/chat/agent_create_compilot",
		},
	},
	// 预览
	preview: {
		msgList: [],
		// todo 数据替换为 gpt生成器，主要是id
		agent: {
			id: data.opt.curID,
			avatar: "",
		},
	},
});

// 生成器 删除消息
const handleDeleteBuilderMsg = (index: Number) => {
	if (!dataChat.builder.msgList[index]) return;
	dataChat.builder.msgList.splice(index, 1);
};

// 预览 删除消息
const handlePreviewBuilderMsg = (index: Number) => {
	if (!dataChat.preview.msgList[index]) return;
	dataChat.preview.msgList.splice(index, 1);
};

// 顶部栏 右侧 更多 选中时
const handleMoreSelect = (key: string | number, option: DropdownOption) => {
	switch (key) {
		// 删除
		case "delete":
			dialog.info({
				title: "删除角色",
				content: "是否删除当前角色?",
				positiveText: "确认",
				negativeText: "取消",
				positiveButtonProps: {
					size: "large",
				},
				negativeButtonProps: {
					size: "large",
				},
				onPositiveClick: () => {
					// todo 删除接口
					console.log("delete");
					msg.success("删除成功");
				},
				style: {
					position: "fixed",
					top: "15%",
					left: "50%",
					transform: "translate(-50%, -50%)",
				},
			});
			break;
	}
};

// 删除开头语
const deleteStarters = (i: number) => {
	if (data.form.opening_question.length <= 1)
		return (data.form.opening_question[0] = "");

	data.form.opening_question.splice(i, 1);
};

const goBack = () => {
	router.go(-1);
};

// 开头语输入时
const handleStarterInput = (val, i) => {
	// 空值 且 非最后一个 时，删除
	if (val.length < 1 && data.form.opening_question.length > 1)
		data.form.opening_question.splice(i, 1);

	// 有值 且 没有下一个 时，添加
	if (val.length > 0 && !data.form.opening_question[i + 1])
		data.form.opening_question[i + 1] = "";
};

// 改变身份模态框显示
const changeModalAuthShow = (
	show: boolean = undefined,
	curIndex: Number = undefined
) => {
	// todo 创建新请求
	// 改变当前请求的下标，用于同步添加请求页数据
	// !TIP 0会被视为false，不能直接使用 !curIndex判断
	if (curIndex !== undefined) data.formActions.curIndex = curIndex;

	if (show !== undefined) return (data.isShowAddAction = show);

	data.isShowAddAction = !data.isShowAddAction;
};

// 删除当前请求
const deleteAction = (curIndex: Number) => {
	data.formActions.list.splice(curIndex, 1);
	msg.success("删除成功");
};

// 保存请求配置
const saveAddActionForm = (curIndex, curForm) => {
	data.formActions.list[curIndex] = {
		...data.formActions.list[curIndex],
		...curForm,
	};
	// data.formActions.list.push(curForm);
};

const updateConfig = () => {
	const {
		name,
		description,
		opening_text,
		opening_question,
		autoSuggestion,
		system_prompt,
		knowledge,
		avatar,
		permission,
	} = data.form;

	// 确保 opening_question 是数组
	const validOpeningQuestions = Array.isArray(opening_question)
		? opening_question.filter((item) => item.length > 0)
		: [];

	// 请求体
	const params = {
		id: data.opt.curID,
		name,
		description: description,
		opening_text: opening_text,
		opening_question: validOpeningQuestions,
		system_prompt: system_prompt,
		knowledge: knowledge,
		avatar,
		suggestion: {
			is_enable: autoSuggestion.useAutoSuggestion,
			custom_prompt:
				autoSuggestion.useAutoSuggestion && autoSuggestion.isCustom
					? autoSuggestion.txtCustom
					: undefined,
		},
		permission: permission,
	};

	console.log("params", params);
	api.agent_edit(params);
};

const requestAgentConfig = () => {
	api
		.agent({
			id: dataChat.builder.agent.id,
		})
		.then((res) => {
			console.log(res);
			// 更新data.form前确认res不为空
			if (res) {
				for (const key in res) {
					if (res[key] !== undefined && res[key] !== null) {
						data.form[key] = res[key];
					}
				}
			}
		});
};

// 更新已引用知识库
const updateKnowledge = (arrList) => {
	data.form.knowledge = arrList;
};

const deleteKnowledge = (i) => {
	data.form.knowledge.splice(i, 1);
};

// 改变模态框显示 选择知识库
const changeModalSelectKnowledgeShow = () => {
	refSelectKnowledge.value.changeModalShow();
};

// 更新发布状态
const updatePublish = (form) => {
	// 更新权限 permission
	data.form.permission = form.permission;
};

// 最终保存、确认时 发布角色
const emitRole = () => {
	// 更新配置
	stateStore.updateMyAgents();
	// 跳转到我的智能体
	router.replace("/createai");
};

onMounted(async () => {
	// 原计划前端做agent创建，引入部分已注释
	// const res = await createAgent();
	// console.log(res);

	if (!route.params.id) {
		const agentId = uuidv4();
		route.params.id = agentId;
		data.opt.curID = agentId;
	} else {
		// 获取agent信息
		api
			.agent({
				id: data.opt.curID,
			})
			.then((res) => {
				// 遍历数据，赋值给data.form
				Object.keys(res).forEach((key) => {
					if (data.form[key] !== undefined) data.form[key] = res[key];
				});
				console.log(data.form);
			});
	}
});

// 监听是否为移动端
watch(
	() => isMobile.value,
	(val) => {
		// 变为非移动端，且当前为预览时，转为创建
		if (data.curPage == "preview" && !val) data.curPage = "create";
	}
);

// 防抖，监听表单变化，更新agent配置
let timerUpdateConfig;
watch(
	() => data.form,
	() => {
		clearTimeout(timerUpdateConfig);

		timerUpdateConfig = setTimeout(() => {
			updateConfig();
		}, 2000);
	},
	{ deep: true }
);

watch(
	() => dataChat.builder.msgList,
	() => {
		clearTimeout(timerUpdateConfig);

		timerUpdateConfig = setTimeout(() => {
			requestAgentConfig();
		}, 2000);
	},
	{ deep: true }
);
</script>

<style lang="less">
// tabs 标签背景色 (创建/配置)
.n-tabs-rail {
	background-color: #f9f9f9 !important;
}

// 自定义上传按钮 包围样式
.n-upload-trigger {
	width: 100% !important;
	padding: 0 0.3rem;
}
</style>
