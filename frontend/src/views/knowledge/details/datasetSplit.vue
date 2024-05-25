<template>
	<div class="w-full h-full flex flex-col gap-4 py-6 px-8">
		<div class="flex-1 w-full h-full flex gap-4">
			<!-- 左侧表单 -->
			<div class="flex-1 flex flex-col overflow-auto">
				<!-- 标题 -->
				<p class="flex items-center gap-1 mb-2">
					<Icon icon="uil:setting" width="22" />
					<span class="font-bold text-[16px]">{{
						$t("knowledge.DataProcessingParams")
					}}</span>
				</p>

				<!-- 处理方式 -->
				<n-form-item
					:label="$t('knowledge.contentSplit')"
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<!-- 处理方式 单选 -->
					<n-radio-group
						v-model:value="data.formDataHandle.curSplitType"
						name="searchType"
						style="width: 100%"
					>
						<div class="flex flex-col gap-4">
							<template
								v-for="item in data.formDataHandle.opt.splitType"
								:key="item.value"
							>
								<div
									@click="changeSplitType(item)"
									class="flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
									:style="{
										'border-color':
											data.formDataHandle.curSplitType == item.value
												? globalColors.btnActive
												: '',
										'box-shadow':
											data.formDataHandle.curSplitType == item.value
												? '0 0 3px 0 #0653FF'
												: '',
									}"
								>
									<div class="w-full flex gap-4">
										<n-radio :value="item.value"></n-radio>
										<div class="w-full flex flex-col">
											<span>{{ item.label }}</span>
											<span class="text-[grey] text-[12px]">{{
												item.desc
											}}</span>

											<!-- 更多 表单 -->
											<div
												v-show="
													item.hasForm &&
													data.formDataHandle.curSplitType == 'custom'
												"
												class="flex flex-col gap-4 mt-4"
											>
												<!-- 理想分块长度 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														{{ $t("knowledge.idealBlockLength") }}
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<p>
																{{ $t("knowledge.idealBlockLengthDesc") }}
															</p>
															<p>
																{{
																	$t("knowledge.idealBlockLengthDescCN", {
																		msg: 400,
																		msg2: 1000,
																	})
																}}
															</p>
															<p>
																{{
																	$t("knowledge.idealBlockLengthDescCN", {
																		msg: 600,
																		msg2: 1200,
																	})
																}}
															</p>
														</n-popover>
													</span>
													<n-input-number
														v-model:value="
															data.formDataHandle.splitterParams.chunk_size
														"
														:step="100"
													/>
												</div>

												<!-- 自定义分隔符 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														{{ $t("knowledge.customDelimiter") }}
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<span>{{
																$t("knowledge.customDelimiterDesc")
															}}</span>
														</n-popover>
													</span>
													<n-input
														v-model:value="
															data.formDataHandle.splitterParams.separator
														"
														type="text"
														placeholder="\n;======;==SPLIT=="
														clearable
													/>
												</div>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
					</n-radio-group>
				</n-form-item>

				<!-- 处理方式 -->
				<n-form-item
					:label="$t('knowledge.informationExtraction')"
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<!-- 处理方式 单选 -->
					<n-radio-group
						v-model:value="data.formDataHandle.curDrillMode"
						name="searchType"
						style="width: 100%"
					>
						<div class="flex flex-col gap-4">
							<template
								v-for="item in data.formDataHandle.opt.extractInfo"
								:key="item.value"
							>
								<div
									@click="changeDrillMode(item)"
									class="flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
									:style="{
										'border-color':
											data.formDataHandle.curDrillMode == item.value
												? globalColors.btnActive
												: '',
										'box-shadow':
											data.formDataHandle.curDrillMode == item.value
												? '0 0 3px 0 #0653FF'
												: '',
									}"
								>
									<div class="w-full flex gap-4">
										<n-radio :value="item.value"></n-radio>
										<div class="w-full flex flex-col">
											<span>{{ item.label }}</span>
											<span class="text-[grey] text-[12px]">{{
												item.desc
											}}</span>

											<!-- 更多 表单 -->
											<div
												v-show="
													item.hasForm &&
													data.formDataHandle.curDrillMode == 'custom'
												"
												class="flex flex-col gap-4 mt-4"
											>
												<!-- 理想分块长度 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														{{ $t("knowledge.idealBlockLength") }}
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<p>
																{{ $t("knowledge.idealBlockLengthDesc") }}
															</p>
															<p>
																{{
																	$t("knowledge.idealBlockLengthDescCN", {
																		msg: 400,
																		msg2: 1000,
																	})
																}}
															</p>
															<p>
																{{
																	$t("knowledge.idealBlockLengthDescCN", {
																		msg: 600,
																		msg2: 1200,
																	})
																}}
															</p>
														</n-popover>
													</span>
													<n-input-number
														v-model:value="
															data.formDataHandle.splitterParams.chunk_size
														"
														:step="100"
													/>
												</div>

												<!-- 自定义分隔符 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														{{ $t("knowledge.customDelimiter") }}
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<span>{{
																$t("knowledge.customDelimiterDesc")
															}}</span>
														</n-popover>
													</span>
													<n-input
														v-model:value="
															data.formDataHandle.splitterParams.separator
														"
														type="text"
														placeholder="\n;======;==SPLIT=="
														clearable
													/>
												</div>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
					</n-radio-group>
				</n-form-item>

				<!-- step2 左侧 底部tag -->
				<n-form-item
					label=" "
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<div class="w-full flex gap-4 items-center">
						<div
							class="py-[2px] px-3 bg-[#F7F8FA] border rounded-lg text-[12px] text-[#383F50]"
						>
							{{ $t("knowledge.totalSegmentation") }}:
							{{ data.formDataHandle.totalSegment }}
						</div>
						<div
							class="py-[2px] px-3 bg-[#F7F8FA] border rounded-lg text-[12px] text-[#383F50]"
						>
							{{ $t("knowledge.totalLength") }}:
							{{ data.formDataHandle.totalLength }}
						</div>
					</div>
				</n-form-item>

				<!-- 底部按钮栏 -->
				<div class="flex justify-end gap-4">
					<n-button style="border-radius: 8px" @click="regenerate">
						<span class="px-1"> {{ $t("knowledge.regeneratePreview") }} </span>
					</n-button>

					<n-button
						:color="globalColors.btnActive"
						style="border-radius: 8px"
						@click="handleNextStep"
					>
						<span class="px-1"> {{ $t("common.nextStep") }} </span>
					</n-button>
				</div>
				<div></div>
			</div>

			<!-- step2 右侧预览 -->
			<div class="h-full flex-1 flex flex-col">
				<!-- 预览切换 -->
				<div class="max-w-[24rem]">
					<n-tabs
						type="segment"
						animated
						:on-update:value="(val) => (data.formDataHandle.curPreview = val)"
						default-value="segment"
					>
						<!-- 分段预览 -->
						<n-tab name="segment">
							<Icon
								icon="mdi:eye-outline"
								width="12"
								:color="
									data.formDataHandle.curPreview === 'segment'
										? globalColors.btnActive
										: ''
								"
							/>
							<span
								class="ml-1"
								:style="{
									color:
										data.formDataHandle.curPreview === 'segment'
											? globalColors.btnActive
											: '',
								}"
								>{{ $t("knowledge.segmentedPreview") }}</span
							>
						</n-tab>
						<!-- 来源列表 -->
						<n-tab name="source">
							<Icon
								icon="ri:file-list-2-line"
								width="12"
								:color="
									data.formDataHandle.curPreview === 'source'
										? globalColors.btnActive
										: ''
								"
							/>
							<span
								class="ml-1"
								:style="{
									color:
										data.formDataHandle.curPreview === 'source'
											? globalColors.btnActive
											: '',
								}"
								>{{ $t("knowledge.extractPreview") }}</span
							>
						</n-tab>
					</n-tabs>
				</div>

				<!-- 分段预览 -->
				<template v-if="data.formDataHandle.curPreview === 'segment'">
					<n-scrollbar style="flex: 1 0 0">
						<div class="flex flex-col mt-3 overflow-auto">
							<!-- 单个文件预览 -->
							<template
								v-for="(item, index) in data.formDataHandle.segmentPreview
									.txtPreview"
								:key="item?.id"
							>
								<div class="w-full border mb-3 p-4 shadow rounded-lg">
									<div class="flex items-center gap-2 text-[12px]">
										<!-- 排序标号 -->
										<n-tag type="info" size="small" style="border-radius: 6px">
											# {{ index + 1 }}
										</n-tag>
										<div class="flex items-center">
											<!-- 文件类型 图标 -->
											<Icon icon="bxs:file" width="18" color="#99B7D2" />
											<!-- 标题 -->
											<span class="font-bold">{{
												item.metadata.file_name
											}}</span>
										</div>
									</div>

									<div
										v-text="item.page_content"
										class="whitespace-pre-line text-[12px]"
									></div>
									<div class="mt-3">
										<n-tag
											size="tiny"
											type="success"
											class="font-bold text-[12px]"
										>
											{{ $t("knowledge.length") }}:
											{{ item.page_content.length }}
										</n-tag>
									</div>
								</div>
							</template>
						</div>
					</n-scrollbar>
				</template>

				<!-- 抽取预览 -->
				<template v-else>
					<div class="flex flex-col">
						<template
							v-for="item in data.formDataHandle.segmentPreview.extractPreview"
							:key="item?.id"
						>
							<div class="gap-2 mt-3 p-3 border shadow-sm rounded-lg">
								<div class="flex items-center mb-2">
									<!-- 文件类型 图标 -->
									<Icon icon="bxs:file" width="18" color="#99B7D2" />
									<!-- 标题 -->
									<span>{{ item.file_name }}</span>
								</div>

								<div v-if="item.summary">
									{{ $t("knowledge.abstract") }}: {{ item.summary }}
								</div>
								<div v-if="item.qa" class="p-6 bg-gray-50 rounded-lg shadow-md">
									<h2 class="text-xl font-semibold mb-4">
										{{ $t("knowledge.qa") }}:
									</h2>
									<div class="space-y-4">
										<div
											v-for="qa in item.qa.qa_list"
											:key="qa.id"
											class="p-4 bg-white rounded-md border border-gray-200"
										>
											<div class="font-bold text-gray-800">
												{{ $t("knowledge.question") }}: {{ qa.question }}
											</div>
											<div class="mt-2 text-gray-600">
												{{ $t("knowledge.answer") }}: {{ qa.answer }}
											</div>
										</div>
									</div>
								</div>
							</div>
						</template>
					</div>
				</template>
			</div>
		</div>
	</div>

	<div
		v-if="data.loading"
		style="
			position: fixed;
			inset: 0;
			background-color: rgba(255, 255, 255, 0.5);
			z-index: 1000;
			display: flex;
			justify-content: center;
			align-items: center;
		"
	>
		<n-spin :show="data.loading">
			<template #description> {{ $t("knowledge.indexCreating") }} </template>
		</n-spin>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { globalColors } from "@/hooks/useTheme";
import { Icon } from "@iconify/vue";
import { api } from "@/api/common";
import { useKnowledgeStore } from "@/store";
import { onMounted } from "vue";
import { t } from "@/locales";

const route = useRoute();
const router = useRouter();
const KnowledgeStore = useKnowledgeStore();

// 获取知识库id
const knowledgeId = route.params?.id;
// 获取文档id
const nodeId = route.params?.nodeId;

const data = reactive({
	docs: [],
	loading: false,
	btnNextDisabled: true,
	formDataHandle: {
		curDrillMode: "summary", // 当前信息抽取模式
		curSplitType: "auto", // 当前字符切分处理方式

		splitterParams: {
			// 自定义规则
			chunk_size: 512, // 理想分块长度
			chunk_overlap: 0, // 分块重叠
			separator: "\n\n", // 自定义分隔符
		},
		extracParams: {},

		splitChar: "", // 自定义分隔符

		// 左侧底部
		// 总分段
		totalSegment: 0,
		// 总字数
		totalLength: 0,
		// todo 计算消耗积分
		needPoint: 0, // 预估消耗积分

		// 右侧预览
		curPreview: "segment", // 当前预览
		segmentPreview: {
			txtPreview: [],
			extractPreview: [],
		},

		opt: {
			// 训练模式
			drillMode: [
				{
					label: t("knowledge.characterTextSplitter"),
					value: "CharacterTextSplitter",
					desc: t("knowledge.characterTextSplitterDesc"),
				},
				{
					label: t("knowledge.enhance"),
					value: "enhance",
					desc: t("knowledge.enhanceDesc"),
				},
				{
					label: t("knowledge.qaSplit"),
					value: "split",
					desc: t("knowledge.qaSplitDesc"),
				},
			],
			// 处理方式
			splitType: [
				{
					label: t("knowledge.auto"),
					value: "auto",
					desc: t("knowledge.autoDesc"),
				},
				{
					label: t("knowledge.customRule"),
					value: "custom",
					desc: t("knowledge.customRuleDesc"),
					hasForm: true,
				},
			],
			// 信息抽取
			extractInfo: [
				{
					label: t("knowledge.extractSummary"),
					value: "summary",
					desc: t("knowledge.extractSummaryDesc"),
				},
				{
					label: t("knowledge.qaExtraction"),
					value: "qa",
					desc: t("knowledge.qaExtractionDesc"),
				},
			],
		},
	},
});

// 切换信息抽取模式
const changeDrillMode = (item) => {
	data.formDataHandle.curDrillMode = item.value;
};

// 切换文本分割处理方式
const changeSplitType = (item) => {
	data.formDataHandle.curSplitType = item.value;
};

// 重新生成预览
const regenerate = () => {
	const spliter_name = "CharacterTextSplitter";
	api
		.split_document({
			documents: data.docs,
			handler_name: spliter_name,
			params: data.formDataHandle.splitterParams,
		})
		.then((res) => {
			// 更新预览数据
			data.formDataHandle.segmentPreview.txtPreview = res?.splited_texts;
			data.formDataHandle.totalSegment = res?.metadata?.total_segment;
			data.formDataHandle.totalLength = res?.metadata?.total_length;
		});

	api
		.extract_document({
			documents: data.docs,
			handler_name: data.formDataHandle.curDrillMode,
			params: {},
		})
		.then((res) => {
			data.formDataHandle.segmentPreview.extractPreview = res;
		});
};

// 下一步
const handleNextStep = async () => {
	// 上传数据
	if (data.docs.length === 0) {
		console.error("No documents to upload.");
		return;
	} else {
		const docsDictionary = {};

		// 遍历docs数组，为每个文档创建字典条目
		data.docs.forEach((doc) => {
			// 使用文档名称作为键
			const key = doc.name;
			console.log(data.formDataHandle.segmentPreview);
			// 查找与当前文档名称匹配的split和extract数据
			const splits = data.formDataHandle.segmentPreview.txtPreview?.filter(
				(item) => item.metadata.file_name === key
			);
			const extract = data.formDataHandle.segmentPreview.extractPreview?.find(
				(item) => item.file_name === key
			);

			console.log(splits, extract);
			// 创建字典项内容
			const dictionaryItem = {
				name: doc.name,
				type: "file",
				content_split: splits.map((split) => split.page_content), // 只提取分段的内容
				summary: extract ? extract.summary : "", // 如果extract信息存在，就添加摘要
				qa: extract ? extract.qa : "", // 如果extract信息存在，就添加qa
				content: doc.content,
			};
			if (doc.node_id) {
				dictionaryItem.node_id = doc.node_id;
			}

			// 将字典项添加到字典对象中
			docsDictionary[key] = dictionaryItem;
		});

		// 转成列表
		const docsList = Object.values(docsDictionary);
		console.log(docsList);
		data.loading = true;

		api
			.upload_data({
				data: docsList,
				knowledge_id: route.params?.id,
			})
			.then((res) => {
				console.log(res);
				data.loading = false;
				// 回到知识库数据集列表
				router.push({
					name: "KnowledgeDetails_dataset",
					params: { id: route.params?.id },
				});
			})
			.finally(() => {
				data.loading = false;
			});
	}
};

onMounted(async () => {
	if (nodeId) {
		const res = await api.get_node_data({ node_id: nodeId });
		const doc = {
			name: res.name,
			content: res.content,
			length: res.content.length,
			node_id: res.node_id,
		};
		data.docs = [doc];
	} else {
		data.docs = KnowledgeStore.$state.docList;
	}
	console.log(data.docs);
	regenerate();
});
</script>

<style lang="less" scoped></style>
