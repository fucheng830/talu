<template>
	<div class="w-full h-full flex">
		<!-- 左侧 文本测试区 -->
		<div
			v-show="!isMobile || (isMobile && !data.mobile?.showHistoryDetails)"
			class="flex-1 flex flex-col max-w-[500px] border-r py-4 overflow-hidden"
		>
			<div
				class="mx-4 p-2 border-2"
				:style="{
					'border-color': globalColors.btnActive,
					'border-radius': globalConfig.btnRadius,
				}"
			>
				<div class="flex justify-between items-center mx-2">
					<n-select
						v-model:value="data.curTestType"
						:options="data.opt.testType"
						:style="{
							color: '#485264',
							'max-width': '10rem',
							'font-weight': 'bold',
						}"
						size="small"
					/>

					<n-button
						size="small"
						:style="{
							'border-radius': globalConfig.btnRadius,
						}"
						@click="changeModalTestOptShow"
					>
						<Icon
							:icon="data.curTestSearchType.icon"
							:color="globalColors.btnActive"
						/>
						<span></span>
						<span class="ml-2">{{ data.curTestSearchType.label }}</span>
					</n-button>
				</div>

				<div class="px-2 mt-2">
					<n-input
						v-model:value="data.txtTest"
						type="textarea"
						:placeholder="$t('knowledge.placeholderInputTest')"
						:autosize="{
							minRows: 7,
							maxRows: 7,
						}"
					/>
				</div>

				<div class="flex justify-end items-center mt-2 px-2">
					<n-button
						:loading="data.isSearching"
						:color="globalColors.btnActive"
						:style="{
							'border-radius': globalConfig.btnRadius,
						}"
						@click="handleTestSearch"
					>
						{{ $t("knowledge.test") }}
					</n-button>
				</div>
			</div>

			<!-- 下半部分 测试历史 -->
			<div class="grow h-full flex flex-col mt-4 px-4">
				<span class="flex items-center gap-1">
					<Icon icon="mdi:clock-outline" width="18" />
					<span class="text-[18px]">{{ $t("knowledge.testHistory") }}</span>
				</span>

				<div class="grow h-full overflow-y-auto">
					<!-- <n-scrollbar> -->
					<div class="flex flex-col gap-2">
						<template v-for="item in data.testHistoryList" :key="item.id">
							<div
								@click="changeCurTestHistory(item)"
								class="history-item flex items-center border py-1 px-2 rounded-lg cursor-pointer gap-3 text-[12px]"
								:style="{
									'background-color':
										data.curTestHistory == item ? '#F0F4FF' : '',
								}"
							>
								<!-- 图标 类型 -->
								<Icon
									:icon="
										data.opt.searchType.find((e) => e.value == item.type)?.icon
									"
									:color="globalColors.btnActive"
								/>
								<!-- 类型 -->
								<span>{{
									data.opt.searchType.find((e) => e.value == item.type)?.label
								}}</span>
								<!-- 搜索内容 -->
								<span
									class="grow overflow-hidden text-ellipsis whitespace-nowrap"
								>
									{{ item.content }}
								</span>
								<!-- 时间 -->
								<span>{{ item.time }}</span>
								<!-- 删除 -->
								<div
									@click.stop="deleteTestHistory(item)"
									class="btn-delete opacity-0"
								>
									<Icon
										icon="material-symbols-light:delete-outline"
										width="18"
									/>
								</div>
							</div>
						</template>
					</div>
					<!-- </n-scrollbar> -->
				</div>
			</div>
		</div>

		<!-- 右侧 结果区 -->
		<div
			v-if="!isMobile || data.mobile?.showHistoryDetails"
			class="flex-1 flex flex-col gap-4 p-4 text-[18px] overflow-y-auto"
			:class="[data.curTestHistory?.type ? '' : 'justify-center items-center']"
		>
			<!-- 已选中历史 -->
			<template v-if="data.curTestHistory?.type">
				<!-- 测试参数 -->
				<div class="flex items-center gap-1">
					<Icon icon="flowbite:adjustments-vertical-outline" width="20" />
					<span>{{ $t("knowledge.testParams") }}</span>
				</div>

				<!-- :bordered="false" -->
				<n-table
					size="small"
					:single-line="true"
					:single-column="true"
					:style="{
						background: '#f0f4ff',
						borderRadius: '10px',
						overflow: 'hidden',
						border: `1px solid #e2e8f0`,
						textAlign: 'center',
					}"
				>
					<thead>
						<tr class="text-[#4A5568] text-[12px] font-bold overflow-x-auto">
							<th>{{ $t("knowledge.testParams") }}</th>
							<th>{{ $t("knowledge.searchPattern") }}</th>
							<th>{{ $t("knowledge.referLimit") }}</th>
							<th>{{ $t("knowledge.minRelevance") }}</th>
							<th>{{ $t("knowledge.resultResort") }}</th>
							<th>{{ $t("knowledge.problemOptimization") }}</th>
						</tr>
					</thead>
					<tbody>
						<tr class="text-[12px]">
							<!-- 搜索模式 -->
							<td class="flex justify-center items-center gap-1">
								<Icon
									:icon="getSearchType().icon"
									:color="globalColors.btnActive"
									width="14"
								/>
								{{ getSearchType().label }}
							</td>
							<!-- 引用上限 -->
							<td>{{ data.curTestHistory.referenceLimit || "-" }}</td>
							<!-- 最低相关度 -->
							<td>{{ data.curTestHistory.minRelevance || "0" }}</td>
							<!-- 结果重排 -->
							<td>
								<div class="flex justify-center items-center">
									<Icon
										:icon="
											data.curTestHistory?.resultResort
												? `noto-v1:check-mark`
												: `streamline-emojis:cross-mark`
										"
										:color="globalColors.btnActive"
										width="16"
									/>
								</div>
							</td>
							<!-- 问题优化 -->
							<td>
								<div class="flex justify-center items-center">
									<Icon
										:icon="
											data.curTestHistory?.problemOptimization
												? `noto-v1:check-mark`
												: `streamline-emojis:cross-mark`
										"
										:color="globalColors.btnActive"
										width="16"
									/>
								</div>
							</td>
						</tr>
					</tbody>
				</n-table>

				<!-- 测试结果 -->
				<div class="flex items-center gap-1">
					<Icon icon="pajamas:review-list" width="18" />
					<span>{{ $t("knowledge.testRes") }}</span>

					<IconPopover color="#485264">
						<p>
							{{ $t("knowledge.testResDesc") }}
						</p>
					</IconPopover>

					<span v-if="data.curTestHistory?.searchDuration" class="text-[14px]"
						>({{ data.curTestHistory?.searchDuration }}s)</span
					>
				</div>

				<!-- 测试结果列表 -->
				<template
					v-for="(item, i) in data.curTestHistory?.data"
					:key="item?.id"
				>
					<div class="flex flex-col gap-2 bg-[#f4f4f7] rounded-xl py-2 px-4">
						<!-- 排序、搜索类型、搜索时长 -->
						<div>
							<span
								class="py-1 px-3 rounded-lg bg-[#f0f4ff] border border-[#c5d7ff] text-[13px]"
								:style="{
									color: globalColors.btnActive,
								}"
							>
								#{{ i + 1 }} | {{ getSearchType().label }}
								<span class="text-[12px]">{{ item.point }}</span>
							</span>
						</div>

						<!-- 内容 -->
						<div class="text-[13px]" v-html="item?.content"></div>

						<!-- 底部栏 -->
						<div class="flex items-center gap-4 text-[12px]">
							<!-- 内容长度 -->
							<IconPopover
								icon="solar:text-square-outline"
								width="14"
								color="#485264"
							>
								<template #text>
									<span class="ml-1 text-[#667085]">
										{{ item?.content?.length }}
									</span>
								</template>

								<p>{{ $t("knowledge.referLength") }}</p>
							</IconPopover>

							<!-- 类型 -->
							<IconPopover
								:icon="searchTestIcon[item?.type]?.icon"
								width="14"
								color="#485264"
							>
								<template #text>
									<span class="ml-1 font-bold">{{
										searchTestIcon[item?.type]?.label
									}}</span>
								</template>

								<p>{{ $t("common.type") }}</p>
							</IconPopover>

							<!-- 类型 -->
							<!-- <div class="flex items-center gap-1">
								<Icon
									:icon="searchTestIcon[item?.type]"
									color="#485264"
									width="14"
								/>

								<span class="font-bold">{{ item.from }}</span>
							</div> -->
						</div>
					</div>
				</template>
			</template>

			<!-- 未选中历史，无数据 -->
			<div v-else class="flex flex-col justify-center items-center gap-2">
				<div
					class="flex justify-center items-center p-2 rounded-full border border-dashed border-[#E2E8F0]"
				>
					<Icon
						icon="fluent:database-search-20-regular"
						width="34"
						color="#485264"
					/>
				</div>
				<span> {{ $t("knowledge.testResShow") }} </span>
			</div>
		</div>

		<!-- 搜索选项 弹窗 -->
		<ModalTestOpt ref="refModalTestOpt" :searchType="data.opt.searchType" />
	</div>
</template>

<script setup lang="ts">
import { globalColors, globalConfig } from "@/hooks/useTheme";
import { Icon } from "@iconify/vue";
import { computed, reactive, ref } from "vue";
import ModalTestOpt from "@/views/knowledge/details/components/ModalTestOpt.vue";
import { useKnowledgeStore } from "@/store";
import { api } from "@/api/common";
import { useRoute } from "vue-router";
import IconPopover from "@/components/common/IconPopover/index.vue";
import {
	datasetTypeIcon,
	searchTestIcon,
} from "@/views/knowledge/knowledgeConfig.ts";
import { useDialog } from "naive-ui";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { t } from "@/locales";

const { isMobile } = useBasicLayout();
const knowledgeStore = useKnowledgeStore();
const route = useRoute();
const dialog = useDialog();
const knowledge_id = route.params.id;

const refModalTestOpt = ref();
const data = reactive({
	mobile: {
		showHistoryDetails: false,
	},
	isSearching: false, // 正在搜索
	txtTest: "", // 测试文本 输入框
	curTestType: "singleText", // 测试类型
	curTestSearchType: computed(() =>
		data.opt.searchType.find(
			(item) => item.value == knowledgeStore.searchPattern.curSearchType
		)
	), // 当前测试 搜索类型
	searchFilter: computed(() => knowledgeStore.searchFilter), // 搜索过滤
	searchQuestionComplement: computed(() => knowledgeStore.questionComplement), // 问题补全
	curTestHistory: {}, // 当前查看 测试历史
	// 测试历史列表
	testHistoryList: computed(
		() => knowledgeStore.listHistory[knowledge_id]?.list
	),
	// [
	// {
	// 	// id: 1,
	// 	type: "semantic",
	// 	content: "搜索的内容搜索的内容搜索的内容搜索的内容搜索的内容搜索的内容",
	// 	time: "2022-12-12 12:12:12",
	// 	referenceLimit: 5000, // 引用上限
	// 	minRelevance: 0, // 最低相关度
	// 	resultResort: false, // 结果重排
	// 	problemOptimization: true, // 问题优化
	// 	searchDuration: 0.561, // 搜索花费时长
	// 	data: [
	// 		{
	// 			point: 0.8293, // 获取得分
	// 			content: "这是一条数据",
	// 			type: "summary",
	// 			// from: "手动录入",
	// 		},
	// 	],
	// },
	// ],
	opt: {
		// 搜索类型，name，description，content
		testType: [
			{
				label: "name",
				value: "name",
			},
			{
				label: "description",
				value: "description",
			},
			{
				label: "content",
				value: "content",
			},
		],
		// 搜索类型
		searchType: [
			{
				label: t("knowledge.semantic"),
				value: "semantic",
				icon: "devicon-plain:networkx",
				desc: t("knowledge.semanticDesc"),
			},
			{
				label: t("knowledge.fullText"),
				value: "fullText",
				icon: "streamline:wifi-horizontal",
				desc: t("knowledge.fullTextDesc"),
			},
			{
				label: t("knowledge.hybrid"),
				value: "hybrid",
				icon: "material-symbols-light:component-exchange",
				desc: t("knowledge.hybridDesc"),
			},
		],
	},
});

// 测试搜索
const handleTestSearch = () => {
	// todo 替换字段名
	let curConfig = {
		// 搜索过滤 部分
		referenceLimit: data.searchFilter?.referenceLimit, // 引用上限
		minRelevancy: data.searchFilter?.minRelevancy, // 最低相关度
	};

	// todo 替换字段名
	// 问题补全 部分
	if (data.searchQuestionComplement?.useQuestionComplement) {
		curConfig = {
			...curConfig,
			curAIModel: data.searchQuestionComplement?.curAIModel, // AI 模型
			desc: data.searchQuestionComplement?.desc, // 对话背景描述
		};
	}

	// 搜索模式 部分
	switch (data.curTestSearchType.value) {
		case "semantic":
			curConfig = {
				...curConfig,
				embedding_ratio: 1, // AI 模型
				bm25_ratio: 0, // 对话背景描述
			};
			break;

		case "fullText":
			curConfig = {
				...curConfig,
				embedding_ratio: 0, // AI 模型
				bm25_ratio: 1, // 对话背景描述
			};
			break;

		case "hybrid":
			curConfig = {
				...curConfig,
				embedding_ratio: 0.5, // AI 模型
				bm25_ratio: 0.5, // 对话背景描述
			};
			break;
	}

	// 搜索开始时间，用于计算搜索时长
	const startTime = new Date().getTime();

	data.isSearching = true; // 搜索中
	api
		.search_node({
			query: data.txtTest,
			knowledge_id,
			search_config: curConfig,
		})
		.then((res) => {
			// 搜索结束时间，用于计算搜索时长
			const endTime = new Date().getTime();

			// 最终数据结构
			const oRes = {
				type: data.curTestSearchType.value, // 搜索类型
				content: data.txtTest, // 搜索内容
				time: new Date()
					.toLocaleString("zh-cn", { hour12: false })
					.replace(/\//g, "-"), // 搜索时间
				referenceLimit: data.searchFilter?.referenceLimit, // 引用上限
				minRelevancy: data.searchFilter?.minRelevancy, // 最低相关度
				problemOptimization:
					data.searchQuestionComplement?.useQuestionComplement, // 问题优化
				searchDuration: (endTime - startTime) / 1000, // 搜索时长
				data: res.map((item) => ({
					id: item?.metadata?.doc_id, // id
					// point: item?.point, // 向量之间的距离获取得分
					content: item?.page_content, // 结果内容
					type: item?.metadata?.index_type, // 类型 summary/qa/content
				})),
			};

			// 加入测试历史
			// data.testHistoryList.unshift(oRes);
			knowledgeStore.setSearchTestHistory(knowledge_id, oRes);
			// 激活当前测试历史
			data.curTestHistory = oRes;
		})
		.finally(() => {
			data.isSearching = false; // 取消搜索中
		});
};

// 改变当前测试历史 激活
const changeCurTestHistory = (item) => {
	data.curTestHistory = item;

	// 移动端 查看详情
	data.mobile.showHistoryDetails = true;
};

// 删除测试历史
const deleteTestHistory = (item) => {
	// data.testHistoryList = data.testHistoryList.filter(
	// 	(cur) => cur.id != item.id
	// );

	dialog.info({
		title: t("common.delete"),
		content: t("knowledge.comfirmDeleteTestHistory"),
		positiveText: t("common.confirm"),
		negativeText: t("common.cancel"),
		onPositiveClick: () => {
			// 执行删除
			knowledgeStore.deleteSearchTestSingleHistory(knowledge_id, item);
			// 重新设置当前激活的测试历史
			if (data.testHistoryList.length <= 0)
				return (data.curTestHistory = undefined);

			data.curTestHistory = data.testHistoryList[0];
		},
	});
};

// 打开 搜索选项 弹窗
const changeModalTestOptShow = () => {
	refModalTestOpt.value.changeModalShow();
};

// 获取搜索类型对应的配置
const getSearchType = () => {
	return data.opt.searchType.find((e) => e.value == data.curTestHistory?.type);
};

// 点击左上角返回时，因返回按钮在此页面外，使用传值给router-view外的布局组件
// 对应 @/views/knowledge/details/index.vue
const onClickBack = () => {
	if (data.mobile.showHistoryDetails) {
		data.mobile.showHistoryDetails = false;
		// 返回true，则不继续执行父组件的返回知识库
		return true;
	}
	return false;
};

defineExpose({
	onClickBack,
});
</script>

<style lang="less" scoped>
table {
	* {
		background: transparent !important;
	}

	// th 继承 表头 tr 的 属性，手动重写默认不继承的属性
	th {
		color: inherit;
		font-weight: inherit;
	}
}

/* 测试历史 鼠标悬浮 */
.history-item:hover {
	border-color: v-bind("globalColors.btnActive");
}

/* 测试历史 删除按钮 */
.history-item:hover .btn-delete {
	opacity: 1;
}
</style>
