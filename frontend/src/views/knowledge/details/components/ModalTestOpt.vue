<template>
	<div>
		<mModal
			ref="refModal"
			:title="$t('knowledge.searchConfigTitle')"
			footerBtnSize="medium"
			footerComfirmBtnType="primary"
			:autoFocus="false"
			:txtCancel="$t('common.close')"
			:txtConfirm="$t('common.complete')"
			@onPositiveClick="handleComfirm"
			@onShowChange="handleModalShowChange"
			style="
				width: 80%;
				max-width: 550px;
				position: fixed;
				top: 10%;
				left: 50%;
				transform: translate(-50%, 0);
			"
		>
			<n-tabs type="segment" animated>
				<!-- 搜索模式 -->
				<n-tab-pane name="searchPattern" :tab="$t('knowledge.searchPattern')">
					<div class="flex flex-col gap-2">
						<template v-for="(item, index) in props.searchType" :key="index">
							<!-- 单选 -->
							<n-radio-group
								v-model:value="data.searchPattern.curSearchType"
								name="searchType"
							>
								<!-- 单个选项 -->
								<div
									@click="changeSearchType(item)"
									class="search-type flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
									:style="{
										'background-color':
											data.searchPattern.curSearchType == item.value
												? '#F0F4FF'
												: '',
										'border-color':
											data.searchPattern.curSearchType == item.value
												? theme.primaryColor
												: '',
									}"
								>
									<div class="flex-1 flex items-center gap-4">
										<!-- 图标 类型 -->
										<Icon
											:icon="item.icon"
											:color="theme.primaryColor"
											width="18"
										/>
										<div class="flex flex-col">
											<span>{{ item.label }}</span>
											<span class="text-[#667085] text-xs">{{
												item.desc
											}}</span>
										</div>
									</div>
									<n-radio :value="item.value"></n-radio>
								</div>
							</n-radio-group>
						</template>
					</div>

					<n-divider />

					<!-- 结果重排 -->
					<div
						@click="changeResultResort(item)"
						class="flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none"
						:style="{
							'border-color': data.searchPattern.resultResort
								? theme.primaryColor
								: '',
						}"
					>
						<div class="flex-1 flex items-center gap-4">
							<!-- 图标 类型 -->
							<Icon
								icon="tabler:exchange"
								:color="theme.primaryColor"
								width="18"
							/>
							<div class="flex flex-col">
								<span>{{ $t("knowledge.resResort") }}</span>
								<span class="text-[#667085] text-xs">{{
									$t("knowledge.resResortDesc")
								}}</span>
							</div>
						</div>
						<n-checkbox v-model:checked="data.searchPattern.resultResort">
						</n-checkbox>
					</div>
				</n-tab-pane>

				<!-- 搜索过滤 -->
				<n-tab-pane name="searchFilter" :tab="$t('knowledge.searchFilter')">
					<div class="flex flex-col gap-8 mt-4 pr-4">
						<div class="flex items-center">
							<div class="flex items-center gap-1 w-[10rem]">
								{{ $t("knowledge.referLimit") }}
								<n-popover
									trigger="hover"
									placement="bottom"
									:keep-alive-on-hover="false"
								>
									<template #trigger>
										<Icon icon="ph:question" color="#111824" width="18" />
									</template>
									<p>{{ $t("knowledge.referLimitDesc") }}</p>
								</n-popover>
							</div>
							<n-slider
								v-model:value="data.searchFilter.referenceLimit"
								:step="50"
								:min="100"
								:max="20000"
								:marks="{
									100: '100',
									20000: '20000',
								}"
							/>
						</div>

						<div class="flex items-center">
							<div class="flex items-center gap-1 w-[10rem]">
								{{ $t("knowledge.minRelevance") }}
								<n-popover
									trigger="hover"
									placement="bottom"
									:keep-alive-on-hover="false"
								>
									<template #trigger>
										<Icon icon="ph:question" color="#111824" width="18" />
									</template>
									<p>{{ $t("knowledge.minRelevanceDesc") }}</p>
								</n-popover>
							</div>
							<n-slider
								v-model:value="data.searchFilter.minRelevancy"
								:step="0.01"
								:min="0"
								:max="1"
								:marks="{
									0: '0',
									1: '1',
								}"
							/>
						</div>
					</div>
				</n-tab-pane>

				<!-- 问题优化 -->
				<n-tab-pane
					name="questionComplement"
					:tab="$t('knowledge.problemOptimization')"
				>
					<div class="flex flex-col gap-4">
						<span class="text-[grey] text-[12px]">
							{{ $t("knowledge.problemOptimizationDesc") }}
						</span>

						<div class="flex justify-between mt-4">
							<span>{{ $t("knowledge.useProblemComplete") }}</span>
							<n-switch
								v-model:value="data.questionComplement.useQuestionComplement"
							/>
						</div>

						<div v-if="data.questionComplement.useQuestionComplement">
							<div class="flex justify-between items-center gap-[4rem]">
								<span class="min-w-[4rem]">{{ $t("knowledge.AIModel") }}</span>
								<n-select
									v-model:value="data.questionComplement.curAIModel"
									:options="data.questionComplement.opt.AIList"
								/>
							</div>
							<!-- <n-form-item label="AI 模型" label-placement="left"> -->
							<!-- </n-form-item> -->
							<div></div>

							<div class="mt-4">
								<div class="flex items-center gap-1">
									{{ $t("knowledge.chatBgDesc") }}
									<n-popover
										trigger="hover"
										placement="bottom"
										:keep-alive-on-hover="false"
									>
										<template #trigger>
											<Icon icon="ph:question" color="#111824" width="18" />
										</template>
										<p>{{ $t("knowledge.chatBgDescDesc") }}</p>
									</n-popover>
								</div>

								<!-- 输入框 -->
								<n-input
									v-model:value="data.questionComplement.desc"
									type="textarea"
									:autosize="{
										minRows: 9,
										maxRows: 18,
									}"
									:placeholder="$t('knowledge.placeholderChatBgDescDesc')"
								/>
							</div>
						</div>
					</div>
				</n-tab-pane>
			</n-tabs>
		</mModal>
	</div>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { computed, onActivated, onMounted, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useKnowledgeStore } from "@/store";
import { useMessage } from "naive-ui";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();

const knowledgeStore = useKnowledgeStore();
const msg = useMessage();

const props = defineProps({
	searchType: {
		type: Array,
		default: [],
	},
});

const refModal = ref();
const data = reactive({
	// 搜索模式
	searchPattern: {
		curSearchType: "semantic",
		resultResort: false,
	},
	// 搜索过滤
	searchFilter: {
		referenceLimit: 5000, // 引用上限
		minRelevancy: 0, // 最低相关度
	},
	// 问题补全
	questionComplement: {
		useQuestionComplement: false, // 使用问题补全
		curAIModel: "FastAI-4k",
		desc: "",
		opt: {
			AIList: computed(() => knowledgeStore.questionComplement.opt.AIList),
		},
	},
});

// 切换搜索模式
const changeSearchType = (item) => {
	data.searchPattern.curSearchType = item.value;
};

// 切换结果重排选择
const changeResultResort = () => {
	data.searchPattern.resultResort = !data.searchPattern.resultResort;
};

// 确认
const handleComfirm = () => {
	// todo 请求接口? (或本地存储) 保存配置
	saveForm();
	changeModalShow();
	msg.success(t("common.saveSuccess"));
};

// 保存配置表单
const saveForm = () => {
	knowledgeStore.setSearchPattern(data.searchPattern);
	knowledgeStore.setSearchFilter(data.searchFilter);
	knowledgeStore.setQuestionComplement({
		curAIModel: data.questionComplement.curAIModel,
		useQuestionComplement: data.questionComplement.useQuestionComplement,
		desc: data.questionComplement.desc,
	});
};

// 恢复原配置
const resetForm = () => {
	const { searchPattern, searchFilter, questionComplement } = knowledgeStore;
	// 搜索模式
	const { curSearchType, resultResort } = searchPattern;
	// 搜索过滤
	const { referenceLimit, minRelevancy } = searchFilter;
	// 问题补全
	const { useQuestionComplement, curAIModel, desc } = questionComplement;

	// 搜索模式
	data.searchPattern.curSearchType = curSearchType;
	data.searchPattern.resultResort = resultResort;

	// 搜索过滤
	data.searchFilter.referenceLimit = referenceLimit;
	data.searchFilter.minRelevancy = minRelevancy;

	// 问题补全
	data.questionComplement.useQuestionComplement = useQuestionComplement;
	data.questionComplement.curAIModel = curAIModel;
	data.questionComplement.desc = desc;
};

// 加载配置
const loadForm = () => {
	data.searchPattern = {
		...data.searchPattern,
		...knowledgeStore.searchPattern,
	};
	data.searchFilter = {
		...data.searchFilter,
		...knowledgeStore.searchFilter,
	};
	data.questionComplement = {
		...data.questionComplement,
		...knowledgeStore.questionComplement,
	};
};

// 当模态框显示变化时
const handleModalShowChange = (isShow) => {
	// 未保存，恢复原配置
	if (!isShow) {
		resetForm();
		return;
	}

	// 打开模态框时
	// 加载配置
	loadForm();
};

// 改变模态框显示
const changeModalShow = () => {
	refModal.value.toggleModal();
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
